import sys
import os
from game.common.enums import *
from game.common.node_types import get_node
from game.common.unit_classes import get_unit
from game.common.monster_types import get_monster
from game.common.trap_types import get_trap

import sys

class ClientStorefront:
    def __init__(self, turn_data):
        self.items = turn_data["items"]
        self.purchases = []
        self.town_number = turn_data["town_number"]

    def get_town_number(self):
        return self.town_number


    def purchase(self, unit, item, item_level, item_slot=None):
        if item_slot:
            self.purchases.append( {
                "unit": unit.id,
                "slot": item_slot,
                "item": item,
                "item_level": item_level
            } )
        else:
            self.purchases.append( {
                "unit": unit.id,
                "item": item,
                "item_level": item_level
            } )

    def get_return_data(self):
        return {
            "message_type": MessageType.town,
            "purchases": self.purchases
        }

class ClientLogic:

    def __init__(self, verbose, player_client):
        self._loop = None
        self._socket_client = None
        self.verbose = verbose
        self.player_client = player_client

        # check to see if the client defiens the quit_in_game_over variable
        self.quit_on_game_over = getattr(self.player_client, "quit_on_game_over", True)

        # Public properties availiable to users

        self.started_game = False
        self.tick_no = 0

    def set_loop(self, loop):
        self._loop = loop

    def set_socket_client(self, socket_client):
        self._socket_client = socket_client

    def initialize(self):

        self.send({
            "type": "register"
        })

    def tick(self, turn_data):
        self.tick_no += 1

        turn_data = self.deserialize(turn_data)

        try:
            turn_result = self.turn(turn_data)
        except Exception as e:
            print()
            print("Exception:")
            print(e)
            raise e
            sys.exit(1)

        serialized_turn_result = self.serialize(turn_result)

        self.send({
            "type": "client_turn",
            "payload": serialized_turn_result
        })

    def turn(self, turn_data):

        if turn_data["message_type"] == MessageType.unit_choice:
            team_name = self.player_client.team_name()
            choices = self.player_client.unit_choice()
            return {
                "message_type": MessageType.unit_choice,
                "team_name": team_name,
                "units": choices
            }

        elif turn_data["message_type"] == MessageType.town:
            units = turn_data["units"]
            gold = turn_data["gold"]
            store = ClientStorefront(turn_data)
            self.player_client.town(units, gold, store)
            return store.get_return_data()

        elif turn_data["message_type"] == MessageType.room_choice:
            units = turn_data["units"]
            options = turn_data["options"]
            options = { int(k):v for k, v in options.items() }
            direction = self.player_client.room_choice(units, options)
            return { "message_type": MessageType.room_choice, "choice": direction }

        elif turn_data["message_type"] == MessageType.combat_round:
            monster = turn_data["monster"]
            units = turn_data["units"]
            self.player_client.combat_round(monster, units)
            return { "message_type": MessageType.combat_round, "units": units }

        elif turn_data["message_type"] == MessageType.trap_round:
            trap = turn_data["trap"]
            units = turn_data["units"]
            self.player_client.trap_round(trap, units)
            return {"message_type": MessageType.trap_round, "units": units}

    def send(self, data):
        self._socket_client.send(data)

    def notify_game_started(self):
        if self.verbose:
            print("Game Started")
        self.started_game = True

    def deserialize(self, turn_data):

        # load units
        units = []
        if "units" in turn_data:
            for u in turn_data["units"]:
                new_unit = get_unit(u["unit_class"])
                new_unit.from_dict(u)
                units.append(new_unit)

        turn_data["units"] = units

        # load message type specific data
        if turn_data["message_type"] == MessageType.room_choice:
            # deserialize rooms
            for direction, room in turn_data["options"].items():
               new_room = get_node(room["node_type"])
               new_room.from_dict(room)
               turn_data["options"][direction] = new_room

        elif turn_data["message_type"] == MessageType.combat_round:
            # deserialize monster
            monster = get_monster(turn_data["monster"]["monster_type"])
            monster.from_dict(turn_data["monster"])
            turn_data["monster"] = monster

        elif turn_data["message_type"] == MessageType.trap_round:
            # deserialize trap
            trap = get_trap(turn_data["trap"]["trap_type"])
            trap.from_dict(turn_data["trap"])
            turn_data["trap"] = trap

        return turn_data

    def serialize(self, turn_result):

        if turn_result["message_type"] == MessageType.combat_round:
            serialized_units = []

            for u in turn_result["units"]:
                serialized_units.append( u.to_dict() )

            turn_result["units"] = serialized_units

        elif turn_result["message_type"] == MessageType.trap_round:
            serialized_units = []

            for u in turn_result["units"]:
                serialized_units.append( u.to_dict() )

            turn_result["units"] = serialized_units


        return turn_result

    def notify_game_over(self):
        if callable(getattr(self.player_client, "game_over", None)):
            self.player_client.game_over()

        if self.quit_on_game_over:
            exit()



