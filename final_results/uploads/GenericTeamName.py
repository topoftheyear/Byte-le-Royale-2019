import math
import itertools
import collections
import random

from game.client.user_client import UserClient
from game.common.enums import *

STATE_DEFAULT = 0
STATE_MOVE    = 1
STATE_MINE    = 2
STATE_SELL    = 3
STATE_DUMP    = 4
STATE_UPGRADE = 5
STATE_CYCLE   = 6 # one full mine/sell cycle
STATE_RESPAWN = 7 # wait to go back to regular cycle

STATE_CURRENT = STATE_DEFAULT                

def get_station_buying(material_type, universe):
    stations = universe.get('all_stations')
    for st in stations:
        if (st.primary_import == material_type or st.secondary_import == material_type) and st.production_material != MaterialType.pylons:
            return st

    raise Exception('Material type does not exist for any stations')

def get_field_of_type(material_type, universe):
    fields = universe.get('asteroid_fields')
    for field in fields:
        if field.material_type == material_type:
            return field

    raise Exception('Material type does not exist for any asteroid fields')

def get_global_price_list(client, universe, reverse=True):
    import_list = []
    import_list.append(get_station_buying(MaterialType.cuprite,  universe))
    import_list.append(get_station_buying(MaterialType.gold,     universe))
    import_list.append(get_station_buying(MaterialType.goethite, universe))

    # sort the list from best prices to worst prices
    import_list.sort(key=lambda st : st.primary_buy_price, reverse=reverse)
    return import_list

# needed to give more procedural 
# functionality to state machine
DEFAULT_BEHAVIOR = 0

# when in doubt, go to this state
def STATE_default(state_info, client, ship, universe):
    global STATE_CURRENT
    global DEFAULT_BEHAVIOR
    client.print('STATE default : ' + str(DEFAULT_BEHAVIOR))

    if DEFAULT_BEHAVIOR == 0:
        # mine a load of cuprite
        state_info.mine_type = MaterialType.cuprite
        state_info.mine_amount = 100

        STATE_CURRENT = STATE_MINE
        DEFAULT_BEHAVIOR = 1

    elif DEFAULT_BEHAVIOR == 1:
        # sell to copper station
        state_info.sell_material_type = MaterialType.cuprite
        STATE_CURRENT = STATE_SELL
        DEFAULT_BEHAVIOR = 2
        #STATE_sell(state_info, client, ship, universe)

    elif DEFAULT_BEHAVIOR == 2:
        # purchase copper from copper station
        client.buy_material(ship.cargo_space)
        DEFAULT_BEHAVIOR = 3

    elif DEFAULT_BEHAVIOR == 3:
        # sell copper to wire station
        state_info.sell_material_type = MaterialType.copper
        STATE_CURRENT = STATE_SELL
        DEFAULT_BEHAVIOR = 4
        #STATE_sell(state_info, client, ship, universe)

    elif DEFAULT_BEHAVIOR == 4:
        # buy wire from wire station
        client.buy_material(ship.cargo_space)
        DEFAULT_BEHAVIOR = 5

    elif DEFAULT_BEHAVIOR == 5:
        # sell wire to circuitry station
        state_info.sell_material_type = MaterialType.wire
        STATE_CURRENT = STATE_SELL
        DEFAULT_BEHAVIOR = 6 # zero to shortcut back to mining again
        #STATE_sell(state_info, client, ship, universe)

    elif DEFAULT_BEHAVIOR == 6:
        # buy circuitry from the circuitry station
        client.buy_material(ship.cargo_space)
        DEFAULT_BEHAVIOR = 7

    elif DEFAULT_BEHAVIOR == 7:
        # sell circuitry to computer station
        state_info.sell_material_type = MaterialType.circuitry
        STATE_CURRENT = STATE_SELL
        DEFAULT_BEHAVIOR = 8
        #STATE_sell(state_info, client, ship, universe)

    elif DEFAULT_BEHAVIOR == 8:
        # buy computers from computer station
        client.buy_material(ship.cargo_space)
        DEFAULT_BEHAVIOR = 9

    elif DEFAULT_BEHAVIOR == 9:
        # sell computers to weaponry station
        state_info.sell_material_type = MaterialType.computers
        STATE_CURRENT = STATE_SELL
        DEFAULT_BEHAVIOR = 10
        #STATE_sell(state_info, client, ship, universe)

    elif DEFAULT_BEHAVIOR == 10:
        # buy weaponry from weaponry station
        client.buy_material(ship.cargo_space)
        DEFAULT_BEHAVIOR = 11

    elif DEFAULT_BEHAVIOR == 11:
        # sell weapnonry to drone station
        state_info.sell_material_type = MaterialType.weaponry
        STATE_CURRENT = STATE_SELL
        DEFAULT_BEHAVIOR = 0
        #STATE_sell(state_info, client, ship, universe)

    else:
        pass

    """
    if DEFAULT_BEHAVIOR == 0:
        # first thing we ever do is buy an engine upgrade
        client.buy_module(ModuleType.engine_speed, 1, ShipSlot.zero)
        DEFAULT_BEHAVIOR = 1

    elif DEFAULT_BEHAVIOR == 1:
        # second thing we do is buy the next upgrade slot
        client.unlock_module()
        ship.current_hull = 0

        # goto 3 to force FSM to think we died
        # goto 4 to continue regular operation
        DEFAULT_BEHAVIOR = 4

    elif DEFAULT_BEHAVIOR == 3:

        # small flag FSM uses to determine state 
        # transition on respawn
        client.is_dead = True

    elif DEFAULT_BEHAVIOR == 4:
        
        if ship.module_0_level != 3 and ship.credits >= client.get_module_price(3):
            # go purchase our module
            state_info.upgrade_level = 3
            state_info.upgrade_slot = ShipSlot.zero
            state_info.upgrade_type = ModuleType.engine_speed

            DEFAULT_BEHAVIOR = 5
            STATE_CURRENT = STATE_UPGRADE

        else:
            STATE_CURRENT = STATE_CYCLE

    elif DEFAULT_BEHAVIOR == 5:

        if ship.module_1_level != 3 and ship.credits >= client.get_module_price(3):
            client.buy_module(ModuleType.cargo_and_mining, 3, ShipSlot.one)
            DEFAULT_BEHAVIOR = 6
        else:
            STATE_CURRENT = STATE_CYCLE

    elif DEFAULT_BEHAVIOR == 6:

        if ship.credits >= client.get_module_unlock_price(2):
            client.unlock_module()
            DEFAULT_BEHAVIOR = 7

        else:
            STATE_CURRENT = STATE_CYCLE

    elif DEFAULT_BEHAVIOR == 7:

        if ship.credits >= client.get_module_price(3):
            client.buy_module(ModuleType.hull, 3, ShipSlot.two)
        DEFAULT_BEHAVIOR = 8

    elif DEFAULT_BEHAVIOR == 8:

        STATE_CURRENT = STATE_CYCLE
        # cycle and earn money forever

    else:
        pass
    """

# move to a desired location
def STATE_move(state_info, client, ship, universe):
    client.print('STATE move')
    client.print('    Moving to ' + str(state_info.move_position[0]) + ', ' + str(state_info.move_position[1]))
    global STATE_CURRENT

    if client.distance_to_coordinate(ship, state_info.move_position) > state_info.move_radius:
        client.move(*state_info.move_position)
    else:
        STATE_CURRENT = state_info.move_return_state

# find a field and collect resources
def STATE_mine(state_info, client, ship, universe):
    client.print('STATE mine')
    client.print('    Mining ' + client.get_material_name(state_info.mine_type))
    global STATE_CURRENT

    if not hasattr(STATE_mine, "should_move"):
        STATE_mine.should_move = True

    if STATE_mine.should_move:
        field = get_field_of_type(state_info.mine_type, universe)
        
        # setup the move state
        state_info.move_position = field.position
        #state_info.move_radius = field.accessibility_radius
        state_info.move_radius = 10
        state_info.move_return_state = STATE_MINE

        STATE_CURRENT = STATE_MOVE
        STATE_mine.should_move = False
        return
    else:
        if client.total_cargo(ship) < ship.cargo_space and state_info.mine_amount > 0:
            old_total = client.total_cargo(ship)
            client.mine()
            state_info.mine_amount -= (client.total_cargo(ship) - old_total)
        else:

            state_info.sell_material_type = state_info.mine_type

            STATE_CURRENT = STATE_DEFAULT
            STATE_mine.should_move = True # prep for next time this state is needed

# find stations buying what we have and sell sell sell!
def STATE_sell(state_info, client, ship, universe):
    client.print('STATE sell')
    client.print('    Selling ' + client.get_material_name(state_info.sell_material_type))
    global STATE_CURRENT

    if not hasattr(STATE_sell, "should_move"):
        STATE_sell.should_move = True

    if STATE_sell.should_move:
        station = get_station_buying(state_info.sell_material_type, universe)

        state_info.move_position = station.position
        state_info.move_radius = 0
        state_info.move_return_state = STATE_SELL

        STATE_CURRENT = STATE_MOVE
        STATE_sell.should_move = False
        return 
    else:
        # the actual sell routine
        #client.print('Printing inventory item: ' + str(ship.inventory[state_info.sell_material_type]))
        client.sell_material(state_info.sell_material_type, ship.inventory.get(state_info.sell_material_type, 0))
        STATE_sell.should_move = True

        if ship.inventory[state_info.sell_material_type] > 0:
            state_info.dump_type = state_info.sell_material_type
            STATE_CURRENT = STATE_DUMP
        else:
            STATE_CURRENT = STATE_DEFAULT

def STATE_dump(state_info, client, ship, universe):
    # just need to dump whatever we cant sell
    client.print('STATE dump')
    client.print('    Dumping ' + client.get_material_name(state_info.dump_type))
    global STATE_CURRENT

    client.drop_cargo(state_info, ship.inventory[state_info.sell_material_type])
    STATE_CURRENT = STATE_DEFAULT

def STATE_upgrade(state_info, client, ship, universe):
    client.print('STATE upgrade')
    client.print('    Upgrading...')
    global STATE_CURRENT

    if not hasattr(STATE_upgrade, "should_move"):
        STATE_upgrade.should_move = True

    if STATE_upgrade.should_move:
        state_info.move_position = [500, 350] # location of Secure Station
        state_info.move_radius = 0
        state_info.move_return_state = STATE_UPGRADE

        STATE_CURRENT = STATE_MOVE
        STATE_upgrade.should_move = False
    else:
        client.buy_module(state_info.upgrade_type, state_info.upgrade_level, state_info.upgrade_slot)
        STATE_CURRENT = STATE_DEFAULT
        STATE_upgrade.should_move = True

# STATE_cycle needs some prcedural behavior
CYCLE_BEHAVIOR = 0
def STATE_cycle(state_info, client, ship, universe):
    client.print('STATE cycle')
    global STATE_CURRENT
    global CYCLE_BEHAVIOR
    client.print('    Cycling : ' + str(CYCLE_BEHAVIOR))

    if CYCLE_BEHAVIOR == 0:

        state_info.mine_type = get_global_price_list(client, universe)[1].primary_import

        #import_list = get_global_price_list(client, universe)
        field = get_field_of_type(state_info.mine_type, universe)

        state_info.move_position = field.position
        state_info.move_return_state = STATE_CYCLE
        state_info.move_radius = 0
        
        STATE_CURRENT = STATE_MOVE
        CYCLE_BEHAVIOR = 1

    elif CYCLE_BEHAVIOR == 1:
        # actually mine material
        if client.total_cargo(ship) < ship.cargo_space:
            #client.print('Mining...')
            client.mine()
        else:
            # cargo is full or we have enough
            state_info.sell_material_type = state_info.mine_type
            CYCLE_BEHAVIOR = 2
    
    elif CYCLE_BEHAVIOR == 2:
        # go to the proper station to offload
        station = get_station_buying(state_info.sell_material_type, universe)

        state_info.move_position = station.position
        state_info.move_radius = 0
        state_info.move_return_state = STATE_CYCLE
        STATE_CURRENT = STATE_MOVE
        CYCLE_BEHAVIOR = 3

    elif CYCLE_BEHAVIOR == 3:
        # we are at the station. offload materials
        client.sell_material(state_info.sell_material_type, ship.inventory[state_info.sell_material_type])
        if ship.inventory[state_info.sell_material_type] > 0:
            state_info.dump_type = state_info.sell_material_type
            STATE_CURRENT = STATE_DUMP

        CYCLE_BEHAVIOR = 0 # reset this state for the next mine/sell cycle
        STATE_CURRENT = STATE_DEFAULT

    else:
        pass

def STATE_respawn(state_info, client, ship, universe):
    client.print('STATE respawn')

    # do not modify anything. wait for respawn period to bo over
    return

class StateInformation:
    def __init__(self):
        self.mine_type = None
        self.mine_amount = 0
        self.mine_location = None

        # used by sell state to find a station
        self.sell_station = None
        self.sell_material_type = None
        self.sell_material_amt  = 0
        self.sell_dump_excess = True

        # used by move state
        self.move_position = None
        self.move_return_state = None # when ship arrives, switch to this state (mine, sell, etc.)
        self.move_radius = None

        # just need to know what to dump
        self.dump_type = None

        # which module should be upgraded and where should it go
        self.upgrade_type = None
        self.upgrade_slot = None
        self.upgrade_level = None

# simple AI: try to collect materials of any kind
class CustomClient(UserClient):
    def __init__(self):
        self.purchase_station = None
        self.sell_station = None
        self.destination = None
        self.material = None

        self.debug = False
        self.current_round = 0        # assists in tracking number of deaths

        self.is_dead = False
        self.num_deaths = 0

        self.state_lut = [
            STATE_default, STATE_move, STATE_mine, STATE_sell, 
            STATE_dump, STATE_upgrade, STATE_cycle, STATE_respawn
        ]
        self.state_info = StateInformation()

    def team_name(self):
        self.print("Sending Team Name")
        return "Generic Team Name"

    def team_color(self):
        self.print("Sending Team Color")

        # list of [ red, green, blue ] values
        return [255, 255, 255] # generic Team Color

    def get_ship_list(self, universe):
        ships = []
        for obj in universe.dump():
            if obj.object_type is ObjectType.ship:
                ships.append(obj)
        return ships

    def total_cargo(self, ship):
        cargo_amount = 0
        for k,v in ship.inventory.items():
            cargo_amount = cargo_amount + v
        return cargo_amount

    def take_turn(self, ship, universe):
        #ship.credits = 1000000000 # 1 billion credits
        self.current_round = self.current_round + 1
        self.print('\n' + str(self.current_round))

        self.update_cached_data(universe)

        global STATE_CURRENT
        global DEFAULT_BEHAVIOR
        global CYCLE_BEHAVIOR
        
        if ship.respawn_counter != -1 and self.is_dead == False:
            self.is_dead = True
            STATE_CURRENT = STATE_RESPAWN

        # end of the respawn period
        if ship.respawn_counter == -1 and self.is_dead == True:
            STATE_CURRENT = STATE_DEFAULT
            DEFAULT_BEHAVIOR = 0
            CYCLE_BEHAVIOR = 0
            self.is_dead = False
            self.num_deaths += 1

        self.state_lut[STATE_CURRENT](self.state_info, self, ship, universe)

        if self.debug:
            
            # print some information about ourselves
            self.print('  X: ' + str(ship.position[0]) + ', Y: ' + str(ship.position[1]))
            self.print('  Credits:       ' + str(ship.credits))
            self.print('  Engine speed:  ' + str(ship.engine_speed))
            self.print('  Weapon damage: ' + str(ship.weapon_damage))
            self.print('  Weapon range:  ' + str(ship.weapon_range))
            self.print('  Cargo space:   ' + str(ship.cargo_space))
            self.print('  Mining yield:  ' + str(ship.mining_yield))
            self.print('  Sensor range:  ' + str(ship.sensor_range))
            self.print('  Hull:          ' + str(ship.current_hull) + ' / ' + str(ship.max_hull))

            self.print('  Prices:')
            self.print('    Module 1 price: ' + str(self.get_module_price(1)))
            self.print('    Module 2 price: ' + str(self.get_module_price(2)))
            self.print('    Module 3 price: ' + str(self.get_module_price(3)))
            self.print('    Module Slot 1 price: ' + str(self.get_module_unlock_price(1)))
            self.print('    Module Slot 2 price: ' + str(self.get_module_unlock_price(2)))
            self.print('    Module Slot 3 price: ' + str(self.get_module_unlock_price(3)))

            self.print('\n  Module Slot 0: ' + str(ship.module_0_level))
            self.print('  Module Slot 1: ' + str(ship.module_1_level))
            self.print('  Module Slot 2: ' + str(ship.module_2_level))
            
            self.print('\n  Number of deaths: ' + str(self.num_deaths))
            self.print('  Respawn counter:  ' + str(ship.respawn_counter))

            # find what we have in the inventory
            self.print('\n  Total cargo: ' + str(self.total_cargo(ship)))
            for k,v in ship.inventory.items():
                self.print('    ' + self.get_material_name(k) + ' : ' + str(ship.inventory[k]))
            #self.print(ship.inventory)

    def print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)
