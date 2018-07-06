import json

from game.server.server_control import ServerControl
from game.common.enums import *
from game.common.npc.npc import NPC
from game.common.ship import Ship
from game.utils.generate_game import load


class CustomServer(ServerControl):

    def __init__(self, verbose=False, wait_on_client=False):
        super().__init__(wait_on_client, verbose)

        self.verbose = verbose

        self.started = False
        self.turn_log = None

        self.teams = {} #client id to team data
        self.npc_teams = {}

        self.universe = load()
        self.ships = [s for s in self.universe if s.object_type == ObjectType.ship]
        self.claim_npcs()




    def pre_turn(self):
        self.print("#"*70)
        self.print("SERVER PRE TURN")

        # reset turn result
        self.turn_log = { "events":[
                {
                    "type": LogEvent.demo
                }
            ],
        }

        if not self.started:
            # first turn, ask for client config, e.g. team name
            return # purposefully short circuit to get to send data

    def send_turn_data(self):
        # send turn data to clients
        self.print("SERVER SEND DATA")
        payload = {}

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
                    "message_type": MessageType.take_turn
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

                if message_type == MessageType.pong:
                    # TODO refactor to include id of sender
                    client_id = data["client_id"]
                    team_name = self.teams[ client_id ]["team_name"]
                    print(f"Pong from {team_name}({client_id})")

                elif message_type == MessageType.take_turn:
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
                self.npc_teams[k]["action"] = PlayerAction.none
                self.npc_teams[k]["action_param_1"] = None
                self.npc_teams[k]["action_param_2"] = None
                self.npc_teams[k]["action_param_3"] = None

                self.npc_teams[k]["move_action"] = None

            for npc in self.npc_teams.keys():
                result = self.npc_teams[npc]["controller"].take_turn(self.universe)

                self.npc_teams[npc]["action"] = result["action_type"]

                # get action params
                for i in range(1, 4):
                    param = f"action_param_{i}"
                    self.npc_teams[npc][param] = result[param]

                self.npc_teams[npc]["move_action"] = result["move_action"]

        self.process_actions()

        self.process_move_actions()

        # update station market / update BGS

        self.turn_data = []




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
            new_npc_controller = NPC(ship)

            self.npc_teams[ship.id] = {
                "controller": new_npc_controller,
                "ship": ship
            }


    def process_actions(self):

        # check if ships still alive
        living_ships = filter(lambda e: e.is_alive(), self.ships)

        # apply the results of any actions a player took if player still alive


    def process_move_actions(self):
        living_ships = filter(lambda e: e.is_alive(), self.ships)


        for team, data in { **self.teams, **self.npc_teams}.items():

            print(team)
            print(data)

            if "move_action" in data and data["move_action"] is not None:
                ship = data["ship"]

                target_x_difference  = data["move_action"][0] - ship.position[0]
                target_y_difference  = data["move_action"][1] - ship.position[1]

                x_direction = -1 if target_x_difference < 0 else 1
                x_magnitude = abs(target_x_difference)

                y_direction = -1 if target_y_difference < 0 else 1
                y_magnitude = abs(target_y_difference)

                x_move = min(ship.engine_speed, x_magnitude)
                y_move = min(ship.engine_speed, y_magnitude)

                print(f"Ship: {ship.id} moving")
                print(f"Original pos: {ship.position}")

                ship.position = (
                    x_direction*x_move + ship.position[0],
                    y_direction*y_move + ship.position[1]
                )

                print(f"New pos: {ship.position}")

