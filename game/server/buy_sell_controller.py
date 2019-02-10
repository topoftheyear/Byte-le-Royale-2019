import sys
import math

from game.common.enums import *
from game.common.name_helpers import *
from game.common.station import *
from game.common.ship import Ship
from game.utils.helpers import *
from game.common.stats import *
from game.utils.stat_utils import get_material_name
from game.server.accolade_controller import AccoladeController

class Bid:
    def __init__(self, ship, material, quantity):
        self.ship = ship
        self.material = material
        self.quantity = quantity


class BuySellController:

    def __init__(self):

        self.debug = False
        self.events = []
        self.stats = []
        self.station_bids = {}

        self.accolade_controller = AccoladeController.get_instance()

        self.buy_bids = {}
        self.sell_bids = {}

    def print(self, msg):
        if self.debug:
            print("Buy Sell Controller: " + str(msg))
            sys.stdout.flush()

    def get_events(self):
        e = self.events
        self.events = []
        return e

    def get_stats(self):
        s = self.stats
        self.stats = []
        return s

    def handle_actions(self, living_ships, universe, teams, npc_teams):
        self.print("#"*100)
        for team, data in { **teams, **npc_teams}.items():
            ship = data["ship"]

            # check if ship is alive
            if not ship.is_alive():
                continue

            if ship.action not in [PlayerAction.sell_material, PlayerAction.buy_material, PlayerAction.sell_salvage]:
                continue

            if ship.action in [PlayerAction.sell_material, PlayerAction.buy_material]:
                # check if station in range
                station = None
                for _station in universe.get(ObjectType.station):
                    # find station in range
                    if (in_radius(_station, ship, _station.accessibility_radius, lambda e:e.position)):
                        station = _station
                        break

                # if no station in range, continue on
                if not station:
                    continue

                # Check for ships that are performing the sell material action
                if ship.action is PlayerAction.sell_material:
                    self.process_sell_action(ship, station)

                elif ship.action is PlayerAction.buy_material:
                    self.process_buy_action(ship, station)
            else:
                # check if station in range
                station = None
                for thing in universe.get(ObjectType.black_market_station):
                    # find station in range
                    if (in_radius(thing, ship, thing.accessibility_radius, lambda e: e.position)):
                        station = thing
                        break

                # if no station in range, continue on
                if not station:
                    continue

                # Check for ships that are performing the sell material action
                self.print("selling salvage action")
                self.process_sell_salvage(ship, station)

        self.process_sell_bids()
        self.process_buy_bids()

        self.sell_bids = {}
        self.buy_bids = {}

    def process_sell_salvage(self, ship, station):

        self.print('Ship in range of a black market to sell salvage')
        material = MaterialType.salvage

        # Check if material is in ship's inventory
        if material not in ship.inventory:
            self.print("Ship does not have salvage in inventory")
            return
        amount = ship.inventory[material]
        ship.inventory[material] = 0
        sale = amount * ILLEGAL_SCRAP_VALUE
        ship.credits += sale
        self.print("Ship {} sold {} {}".format(
            ship.team_name,
            amount,
            get_material_name(material)
        ))
        self.accolade_controller.redeem_salvage(ship, amount)
        self.accolade_controller.all_credits_earned(ship, sale)

        # Apply bounty for selling scrap
        # TODO determine balanced value for this, current 1:1
        if ship.notoriety >= LegalStanding.pirate:
            ship.bounty_list.append({"bounty_type": BountyType.scrap_sold, "value": sale * ILLEGAL_SCRAP_NOTORIETY_RATIO, "age": 0})
            self.print(f"Bounty {BountyType.scrap_sold} given to ship {ship.id}")

        self.events.append({
            "type": LogEvent.salvage_sold,
            "station_id": station.id,
            "ship_id": ship.team_name,
            "amount": amount,
            "total_sale": sale
        })

    def process_sell_action(self, ship, station):

        self.print('Ship in range of a station to sell')
        material = ship.action_param_1
        amount = ship.action_param_2

        # Check if material and the amount is in ships inventory, if not set amount to max held in inventory
        if material not in ship.inventory:
            self.print("Ship does not have material {} in inventory".format(material))
            return  # don't submit a bid with no available material
        amount = min(amount, ship.inventory[material])

        # Check if station accepts material
        station_materials = [station.primary_import, station.secondary_import]
        if material not in station_materials:
            self.print('Improper material type {} for station {}'.format(material, station.id))
            return

        if station not in self.sell_bids:
            self.sell_bids[station] = []

        self.sell_bids[station].append(Bid(ship, material, amount))
        self.print("Ship {} submitted bid to sell {} {}".format(
            ship.team_name,
            amount,
            get_material_name(material)
        ))

    def process_buy_action(self, ship, station):
        quantity = ship.action_param_1
        material = station.production_material
        self.print("STATION CHOSEN:  " + str(material) + "    "+ str(station.cargo[material]))
        self.print("STATION PRIMARY:  " + str(station.primary_import) + "    "+ str(station.cargo[station.primary_import]))

        # verify station has enough material, reducing requested quantity to what the station has.
        quantity = min(station.cargo[material], quantity)

        # verify that the ship has enough credits for the requested materials, otherwise reduce order
        # to what the ship can afford
        cost = station.sell_price * quantity
        diff = ship.credits - cost
        if diff < 0:  # if cost > ship.credits
            to_remove = math.floor(diff/station.sell_price) #will be negative
            self.print(
                "cost greater than ship can afford. cost: {} ship credits: {}, reducing qty from {} to {}".format(
                cost, ship.credits, quantity, quantity-to_remove
            ))
            quantity += to_remove

        if quantity < 0:
            self.print("Ship could not afford any product.")
            return

        if station not in self.buy_bids:
            self.buy_bids[station] = []
        self.buy_bids[station].append(Bid(ship, material, quantity))

        self.print("Ship {} submitted bid to buy {} {} at price: {} current CR: {}".format(
            ship.team_name,
            quantity,
            get_material_name(material),
            station.sell_price * quantity,
            ship.credits
        ))

    def process_sell_bids(self):
        for station, bids in self.sell_bids.items():
            self.print("Processing sell bids for station {}".format(station.name))
            # get number of bids
            primary_bids =  [ bid for bid in bids if bid.material is station.primary_import ]
            secondary_bids = [ bid for bid in bids if bid.material is station.secondary_import ]

            num_primary_bids = len(primary_bids)
            num_secondary_bids = len(secondary_bids)

            # get total quantity requested
            primary_qty = sum(bid.quantity for bid in primary_bids)
            secondary_qty = sum(bid.quantity for bid in secondary_bids)

            # ### Process Primary Bids ###
            # determine if the station has enough room for the cargo
            new_cargo_size = primary_qty + station.cargo.get(station.primary_import, 0)
            self.print("Checking station primary cargo space. Current: {} projected: {} max: {}".format(
                station.cargo.get(station.primary_import, 0),
                new_cargo_size,
                station.primary_max
            ))
            if new_cargo_size > station.primary_max:
                # value to track already sold material as the loop goes
                num_bought = 0
                while len(primary_bids) > 0:
                    bid_min = min([bid.quantity for bid in primary_bids])
                    bid_len = len(primary_bids)

                    # enough room to buy the minimum of primary_bids from all the bids
                    if bid_min * bid_len + num_bought * bid_len + station.cargo.get(station.primary_import, 0) <= station.primary_max:
                        num_bought += bid_min
                        remove = []
                        for bid in primary_bids:
                            bid.quantity -= bid_min
                            if bid.quantity == 0:
                                remove.append(bid)
                                price = num_bought * station.primary_buy_price

                                # modify ship values
                                bid.ship.credits += price
                                bid.ship.inventory[bid.material] -= num_bought

                                # give material to station
                                if bid.material not in station.cargo:
                                    station.cargo[bid.material] = num_bought
                                else:
                                    station.cargo[bid.material] += num_bought

                                self.accolade_controller.credits_earned(bid.ship, price)
                                self.accolade_controller.all_credits_earned(bid.ship, price)

                                self.print("Processing sell bid from ship: {}. Quantity to sell: {} Price: {} ".format(
                                    bid.ship.team_name, num_bought, price
                                ))
                                self.events.append({
                                    "type": LogEvent.material_sold,
                                    "station_id": station.id,
                                    "ship_id": bid.ship.team_name,
                                    "material": bid.material,
                                    "amount": num_bought,
                                    "total_sale": price
                                })
                        # delete a fulfilled order
                        for rem_bid in remove:
                            primary_bids.remove(rem_bid)
                    else:
                        # equally distribute remaining space
                        distribute = math.floor((station.primary_max - (station.cargo.get(station.primary_import, 0) + num_bought * bid_len))/bid_len) + num_bought
                        price = distribute * station.primary_buy_price

                        for bid in primary_bids:
                            # modify ship values
                            bid.ship.credits += price
                            bid.ship.inventory[bid.material] -= distribute

                            # give material to station
                            if bid.material not in station.cargo:
                                station.cargo[bid.material] = distribute
                            else:
                                station.cargo[bid.material] += distribute

                            self.accolade_controller.credits_earned(bid.ship, price)
                            self.accolade_controller.all_credits_earned(bid.ship, price)

                            self.print("Processing sell bid from ship: {}. Quantity to sell: {} Price: {} ".format(
                                bid.ship.team_name, distribute, price
                            ))
                            self.events.append({
                                "type": LogEvent.material_sold,
                                "station_id": station.id,
                                "ship_id": bid.ship.team_name,
                                "material": bid.material,
                                "amount": distribute,
                                "total_sale": price
                            })
                        break
            else:
                for bid in primary_bids:
                    amount = bid.quantity
                    price = amount * station.primary_buy_price
                    # modify ship values
                    bid.ship.credits += price
                    bid.ship.inventory[bid.material] -= amount

                    # give material to station
                    if bid.material not in station.cargo:
                        station.cargo[bid.material] = amount
                    else:
                        station.cargo[bid.material] += amount

                    self.accolade_controller.credits_earned(bid.ship, price)
                    self.accolade_controller.all_credits_earned(bid.ship, price)

                    self.print("Processing sell bid from ship: {}. Quantity to sell: {} Price: {} ".format(
                        bid.ship.team_name, amount, price
                    ))
                    self.events.append({
                        "type": LogEvent.material_sold,
                        "station_id": station.id,
                        "ship_id": bid.ship.team_name,
                        "material": bid.material,
                        "amount": amount,
                        "total_sale": price
                    })

            # ### Process Secondary Bids ###
            # determine if the station has enough room for the cargo
            new_cargo_size = secondary_qty + station.cargo.get(station.secondary_import, 0)
            self.print("Checking station secondary cargo space. Current: {} projected: {} max: {}".format(
                station.cargo.get(station.secondary_import, 0),
                new_cargo_size,
                station.secondary_max
            ))
            if new_cargo_size > station.secondary_max:
                # value to track already sold material as the loop goes
                num_bought = 0
                while len(secondary_bids) > 0:
                    bid_min = min([bid.quantity for bid in secondary_bids])
                    bid_len = len(secondary_bids)

                    # enough room to buy the minimum of secondary_bids from all the bids
                    if bid_min * bid_len + num_bought * bid_len + station.cargo.get(station.secondary_import, 0) <= station.secondary_max:
                        num_bought += bid_min
                        remove = []
                        for bid in secondary_bids:
                            bid.quantity -= bid_min
                            if bid.quantity == 0:
                                remove.append(bid)
                                price = num_bought * station.secondary_buy_price

                                # modify ship values
                                bid.ship.credits += price
                                bid.ship.inventory[bid.material] -= num_bought

                                # give material to station
                                if bid.material not in station.cargo:
                                    station.cargo[bid.material] = num_bought
                                else:
                                    station.cargo[bid.material] += num_bought

                                self.accolade_controller.credits_earned(bid.ship, price)
                                self.accolade_controller.all_credits_earned(bid.ship, price)

                                self.print(
                                "Processing sell bid from ship: {}. Quantity to sell: {} Price: {} ".format(
                                    bid.ship.team_name, num_bought, price
                                ))
                                self.events.append({
                                    "type": LogEvent.material_sold,
                                    "station_id": station.id,
                                    "ship_id": bid.ship.team_name,
                                    "material": bid.material,
                                    "amount": num_bought,
                                    "total_sale": price
                                })
                        # delete a fulfilled order
                        for rem_bid in remove:
                            secondary_bids.remove(rem_bid)
                    else:
                        # equally distribute remaining space
                        distribute = math.floor((station.secondary_max - (
                                    station.cargo.get(station.secondary_import,
                                                      0) + num_bought * bid_len)) / bid_len) + num_bought
                        price = distribute * station.secondary_buy_price

                        for bid in secondary_bids:
                            # modify ship values
                            bid.ship.credits += price
                            bid.ship.inventory[bid.material] -= distribute

                            # give material to station
                            if bid.material not in station.cargo:
                                station.cargo[bid.material] = distribute
                            else:
                                station.cargo[bid.material] += distribute

                            self.accolade_controller.credits_earned(bid.ship, price)
                            self.accolade_controller.all_credits_earned(bid.ship, price)

                            self.print(
                            "Processing sell bid from ship: {}. Quantity to sell: {} Price: {} ".format(
                                bid.ship.team_name, distribute, price
                            ))
                            self.events.append({
                                "type": LogEvent.material_sold,
                                "station_id": station.id,
                                "ship_id": bid.ship.team_name,
                                "material": bid.material,
                                "amount": distribute,
                                "total_sale": price
                            })
                        break
            else:
                for bid in secondary_bids:
                    amount = bid.quantity
                    price = amount * station.secondary_buy_price
                    # modify ship values
                    bid.ship.credits += price
                    bid.ship.inventory[bid.material] -= amount

                    # give material to station
                    if bid.material not in station.cargo:
                        station.cargo[bid.material] = amount
                    else:
                        station.cargo[bid.material] += amount

                    self.accolade_controller.credits_earned(bid.ship, price)
                    self.accolade_controller.all_credits_earned(bid.ship, price)

                    self.print("Processing sell bid from ship: {}. Quantity to sell: {} Price: {} ".format(
                        bid.ship.team_name, amount, price
                    ))
                    self.events.append({
                        "type": LogEvent.material_sold,
                        "station_id": station.id,
                        "ship_id": bid.ship.team_name,
                        "material": bid.material,
                        "amount": amount,
                        "total_sale": price
                    })

    def process_buy_bids(self):

        for station, bids in self.buy_bids.items():
            self.print("Processing buy bids for station {}".format(station.name))

            num_primary_bids = len(bids)

            # get total quantity requested
            total_qty = sum(bid.quantity for bid in bids)

            available = station.cargo.get(station.production_material, 0)
            new_cargo_size = available - total_qty
            self.print("Checking station production cargo space. Current: {} projected: {}".format(
                available,
                new_cargo_size
            ))
            if new_cargo_size < 0 and available != 0:
                # we don't have enough to sell
                cargo_to_refuse = new_cargo_size * -1
                cargo_to_refuse_per_ship = math.floor(cargo_to_refuse / num_primary_bids)
            elif new_cargo_size < 0 and available == 0:
                self.print("This station does not have any {} to sell".format(
                    get_material_name(station.production_material)
                ))
                continue
            else:
                cargo_to_refuse_per_ship = 0
            self.print("Quantity to refuse per ship: {}".format(cargo_to_refuse_per_ship))

            for bid in bids:
                self.print("Process bid for ship: {} material: {} qty: {}".format(
                    bid.ship.team_name,
                    get_material_name(bid.material),
                    bid.quantity
                ))
                quantity = bid.quantity - cargo_to_refuse_per_ship

                # verify that new cargo fits
                total_cargo = sum(bid.ship.inventory.values())
                new_cargo = total_cargo + quantity

                if new_cargo > bid.ship.cargo_space:
                    # not enough room so only but as much as we can fit
                    self.print("Not enough room in ship. current: {} max: {} projected: {}".format(
                        total_cargo, bid.ship.cargo_space, new_cargo_size
                    ))
                    quantity -= new_cargo - bid.ship.cargo_space

                price = quantity * station.sell_price
                bid.ship.credits -= price
                self.print("Buy price: {} credits left: {}".format(
                    price, bid.ship.credits
                ))

                if bid.material not in bid.ship.inventory:
                    bid.ship.inventory[bid.material] = min(
                        quantity,
                        bid.ship.cargo_space - sum(bid.ship.inventory.values()))
                else:
                    bid.ship.inventory[bid.material] = min(
                        quantity+bid.ship.inventory[bid.material],
                        bid.ship.cargo_space - sum(bid.ship.inventory.values()))

                # remove quantity from station
                station.cargo[station.production_material] -= quantity

            # make sure we don't go below zero quantity
            station.cargo[station.production_material] = max(0, station.cargo[station.production_material])
