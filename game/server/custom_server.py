import json
import random

from game.server.server_control import ServerControl
from game.common.enums import *
from game.common.npc.mining_npc import MiningNPC
from game.common.npc.combat_npc import CombatNPC
from game.common.npc.module_npc import ModuleNPC
from game.common.npc.unlock_npc import UnlockNPC
from game.common.ship import Ship
from game.utils.generate_game import load

from game.server.station_controller import StationController
from game.server.mining_controller import MiningController
from game.server.notoriety_controller import NotorietyController
from game.server.combat_controller import CombatController
from game.server.death_controller import DeathController
from game.server.police_controller import PoliceController
from game.server.module_controller import ModuleController


class CustomServer(ServerControl):

    def __init__(self, verbose=False, wait_on_client=False):
        super().__init__(wait_on_client, verbose)

        self.verbose = verbose

        self.started = False
        self.turn_log = None

        self.teams = {} #client id to team data
        self.npc_teams = {}

        self.universe = load()


        # Set up controllers
        stations = self.filter_universe(ObjectType.station)
        self.station_controller = StationController(stations)
        self.station_controller.init(stations)

        self.mining_controller = MiningController()
        self.notoriety_controller = NotorietyController.get_instance()
        self.combat_controller = CombatController()
        self.death_controller = DeathController()
        self.police_controller = PoliceController()
        self.module_controller = ModuleController()



        # prep police
        self.police = self.police_controller.setup_police(self.universe)
        self.ships = [s for s in self.universe if s.object_type in [ ObjectType.ship, ObjectType.police, ObjectType.enforcer ]]

        self.claim_npcs()




    def pre_turn(self):
        self.print("#"*70)
        self.print("SERVER PRE TURN")

        # reset turn result
        self.turn_log = {
            "events":[],
            "stats": {}
        }

        if not self.started:
            # first turn, ask for client config, e.g. team name
            return # purposefully short circuit to get to send data

        # update police state
        new_police, police_to_remove = self.police_controller.assess_universe(self.universe)

        self.universe = [ obj for obj in self.universe if obj not in police_to_remove ]
        self.universe.extend(new_police)

        self.ships = [ obj for obj in self.ships if obj not in police_to_remove ]
        self.ships.extend(new_police)

        self.police = [ obj for obj in self.police if obj not in police_to_remove ]
        self.police.extend(new_police)

    def send_turn_data(self):
        # send turn data to clients
        self.print("SERVER SEND DATA")
        payload = {}

        serialized_universe = self.serialize_universe(security_level=SecurityLevel.player_owned)

        for i in self._client_ids:
            #print(f"Pinging {i}")
            #payload[i] = { "message_type": MessageType.ping}

            if not self.started:
                # request team registration info
                payload[i] = {
                        "message_type":  MessageType.team_name
                }

            else:
                # send game specific data in payload
                pass
                payload[i] = {
                    "message_type": MessageType.take_turn,
                    "ship": self.teams[i]["ship"].to_dict(),
                    "universe": serialized_universe # TODO refactor to use serialize_visible_objects()
                }

        # actually send the data to the client
        self.send({
            "type": "server_turn_prompt",
            "payload": payload
        })



    def post_turn(self):
        self.print("SERVER POST TURN")

        self.deserialize_turn_data()

        if self.started:
            # reset team actions to prevent accidental repeat actions
            for k in self.teams.keys():
                self.teams[k]["action"] = PlayerAction.none
                self.teams[k]["action_param_1"] = None
                self.teams[k]["action_param_2"] = None
                self.teams[k]["action_param_3"] = None

                self.teams[k]["move_action"] = None

        # handle response if we got one
        for data in self.turn_data:
            if "message_type" not in data:
                return # bad turn
            else:
                message_type = data["message_type"]

            if not self.started:
                if message_type == MessageType.team_name:

                    client_id = data["client_id"]
                    team_name = data["team_name"]

                    ship = Ship()
                    ship.init(team_name)

                    self.universe.append(ship)
                    self.ships.append(ship)

                    self.teams[client_id] = {
                        "team_name": team_name,
                        "ship": ship
                    }

                    # TODO refactor so we don't start till all teams have had a chance to give a name
                    self.started = True
            else:

                if message_type == MessageType.take_turn:
                    if "action_type" in data:
                        # get action
                        self.teams[client_id]["action_type"] = data["action_type"]

                        # get action params
                        for i in range(1, 4):
                            param = f"action_param{i}"
                            if param in data:
                                self.teams[client_id][param] = data[param]

                    if "move_action" in data:
                        self.teams[client_id]["move_action"] = data["move_action"]

        # queue npc actions
        if self.started:
            # reset team actions to prevent accidental repeat actions
            for k in self.npc_teams.keys():
                self.npc_teams[k]["ship"].action = PlayerAction.none
                self.npc_teams[k]["ship"].action_param_1 = None
                self.npc_teams[k]["ship"].action_param_2 = None
                self.npc_teams[k]["ship"].action_param_3 = None

                self.npc_teams[k]["ship"].move_action = None

            for npc in self.npc_teams.keys():
                result = self.npc_teams[npc]["controller"].reset_actions()
                result = self.npc_teams[npc]["controller"].take_turn(self.universe)

                self.npc_teams[npc]["ship"].action = result["action_type"]
                self.npc_teams[npc]["ship"].action_param_1 = result["action_param_1"]
                self.npc_teams[npc]["ship"].action_param_2 = result["action_param_2"]
                self.npc_teams[npc]["ship"].action_param_3 = result["action_param_3"]

                self.npc_teams[npc]["ship"].move_action = result["move_action"]


            for police in self.police:
                actions = self.police_controller.take_turn(police, self.universe)
                police.move_action = actions["move_action"]
                police.action = actions["action"]
                police.action_param_1 = actions["action_param_1"]
                police.action_param_2 = actions["action_param_2"]
                police.action_param_3 = actions["action_param_3"]


        self.process_actions()

        self.process_move_actions()


        # update station market / update BGS
        self.station_controller.tick(
            self.filter_universe(ObjectType.station))

        self.turn_log["stats"]["market"] = self.station_controller.get_stats()

        self.turn_data = []
        self.turn_log["universe"] = self.serialize_universe(security_level=SecurityLevel.engine)




    def log(self):
        # saves the turn log to this turn's log file.
        # This is what the visualizer reads
        return {
            "turn_result": self.turn_log
        }


    def deserialize_turn_data(self):
        # Deserialize a message from a client

        # if we have recieved a message, then turn data will not be none
        for idx, data in enumerate(self.turn_data):
            if data["message_type"] != MessageType.demo:
                # Deserialize message data, i.e. load ship data
                pass

    def check_end(self):
        # Detect if we have reached a stopping state
        # set self._quit to true to safely shutdown at end of turn
        #self._quit = True
        pass

    def print(self, msg):
        # Handles toggling print messages via verbose
        if self.verbose:
            print(msg)


    def game_over(self):

        # print game exit info

        self.turn_log["events"].append({
            "type": LogEvent.demo,
        })

        self._quit = True # die safely
        return

    def claim_npcs(self):
        self.npcs = []

        for ship in self.ships:
            npc_type = random.choice([CombatNPC, MiningNPC, ModuleNPC, UnlockNPC])
            new_npc_controller = npc_type(ship)

            self.npc_teams[ship.id] = {
                "controller": new_npc_controller,
                "ship": ship
            }


    def process_actions(self):

        # check if ships still alive
        living_ships = filter(lambda e: e.is_alive(), self.ships)

        # apply the results of any actions a player took if player still alive
        self.mining_controller.handle_actions(living_ships, self.universe, self.teams, self.npc_teams)
        self.combat_controller.handle_actions(living_ships, self.universe, self.teams, self.npc_teams)
        self.module_controller.handle_actions(living_ships, self.universe, self.teams, self.npc_teams)


        dead_ships = filter(lambda e: not e.is_alive(), self.ships)
        self.death_controller.handle_actions(dead_ships)

        self.notoriety_controller.update_standing_universe(self.ships)

        # log events and stats
        self.turn_log["events"].extend( self.mining_controller.get_events() )
        self.turn_log["stats"]["mining"] = self.mining_controller.get_stats()

        self.turn_log["events"].extend( self.combat_controller.get_events() )

        self.turn_log["events"].extend( self.death_controller.get_events() )

        self.turn_log["events"].extend( self.police_controller.get_events() )

        self.turn_log["events"].extend( self.notoriety_controller.get_events() )

        self.turn_log["events"].extend( self.module_controller.get_events() )



    def process_move_actions(self):

        for team, data in { **self.teams, **self.npc_teams}.items():
            ship = data["ship"]

            if ship.is_alive():
                if "move_action" in data:
                    ship.move_action = data["move_action"]
                self.move_ship(ship)

        for ship in self.police:
            self.move_ship(ship)


    def move_ship(self, ship):

        if ship.move_action is not None:

            target_x_difference  = ship.move_action[0] - ship.position[0]
            target_y_difference  = ship.move_action[1] - ship.position[1]

            x_direction = -1 if target_x_difference < 0 else 1
            x_magnitude = abs(target_x_difference)

            y_direction = -1 if target_y_difference < 0 else 1
            y_magnitude = abs(target_y_difference)

            x_move = min(ship.engine_speed, x_magnitude)
            y_move = min(ship.engine_speed, y_magnitude)

            ship.position = (
                x_direction*x_move + ship.position[0],
                y_direction*y_move + ship.position[1]
            )

            self.turn_log["events"].append({
                "type": LogEvent.ship_move,
                "ship_id": ship.id,
                "pos": ship.position,
                "target_pos": ship.move_action
            })


    def serialize_universe(self, security_level):
        serialized_universe = []
        for obj in self.universe:
            serialized_obj = obj.to_dict(security_level=security_level)
            serialized_universe.append(serialized_obj)
        return serialized_universe

    def serialize_visible_objects(self, pos, radius):
        pass # serialize only objects in visible range of player ship

    def filter_universe(self, object_type):

        return list(filter(lambda obj: obj.object_type==object_type, self.universe))


