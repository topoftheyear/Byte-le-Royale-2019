import sys
import math

from game.common.enums import *
from game.common.asteroid_field import AsteroidField
from game.common.ship import Ship
from game.common.stats import GameStats
from game.utils.helpers import *

class RepairController:

    def __init__(self):

        self.debug = False
        self.events = []
        self.stats = []

    def print(self, msg):
        if self.debug:
            print(str(msg))
            sys.stdout.flush()

    def get_events(self):
        e = self.events
        self.events = []
        return e

    def get_stats(self):
        s = self.stats
        self.stats = []
        return s


    def handle_actions(self, living_ships, universe, teams, npc_teams, combat_timeouts):

        self.median_sell_price = None
        self.sell_prices = None

        for team, data in { **teams, **npc_teams}.items():
            ship = data["ship"]

            if not ship.is_alive():
                continue

            # passive heal for ships near station
            ship_near_a_station = False
            for stations in universe.get(ObjectType.secure_station):

                #  determine if ship should start repairing
                ship_in_radius = in_radius(
                    stations,
                    ship,
                    lambda s, t: s.accessibility_radius,
                    lambda e: e.position)

                if ship_in_radius:
                    ship_near_a_station = True

                    # verify ship out of combat
                    ship_out_of_combat = combat_timeouts.get(ship.id, GameStats.healing_combat_cooldown) >= GameStats.healing_combat_cooldown
                    if ship_out_of_combat:
                        if ship.passive_repair_counter > 0:
                            self.print(f"ship passive repairing in progress... turns remaining: {ship.passive_repair_counter}")
                            # countdown to next heal
                            ship.passive_repair_counter -= 1
                        elif ship.current_hull != ship.max_hull:
                            ship.passive_repair_counter = GameStats.passive_repair_counter

                            # commence heal
                            if ship.max_hull - ship.current_hull < GameStats.passive_repair_amount:
                                ship.current_hull = ship.max_hull
                            else:
                                ship.current_hull += GameStats.passive_repair_amount

                            self.print(f"Ship successfully passive repaired. New Health: {ship.current_hull}")
                            self.events.append({
                                "type": LogEvent.passive_repair,
                                "ship_id": ship.id,
                                "new_health": ship.current_hull,
                            })

            if not ship_near_a_station:
                ship.passive_repair_counter = GameStats.passive_repair_counter

            # Check for ships that are performing the repair action
            if ship.action is PlayerAction.repair:

                self.print(f"Ship attempts to repair...")

                price_increase = False
                price_decrease = False

                # Create a list of stations that are in range
                in_range = []
                for station in universe.get("all_stations"):
                    ship_in_radius = in_radius(
                        station,
                        ship,
                        lambda s, t: s.accessibility_radius,
                        lambda e: e.position)
                    if ship_in_radius:
                        in_range.append(station)

                if len(in_range) == 0:
                    self.print(f"ship is not near a station.")
                    continue

                # determine closest station
                closest_station = next(
                    iter(sorted(
                        in_range,
                        key=lambda s:
                            distance_to(ship, station, lambda s: s.position))),
                    None)

                # no nearby stations
                if closest_station is None:
                    continue

                # determine what price modifer to apply
                if closest_station == ObjectType.station:
                    price_increase = True
                elif closest_station == ObjectType.black_market_station:
                    price_decrease = True


                # verify ship out of combat
                ship_out_of_combat = combat_timeouts.get(ship.id, GameStats.healing_combat_cooldown) >= GameStats.healing_combat_cooldown
                if not ship_out_of_combat:
                    self.print(f"Ship is in combat already. Please wait {GameStats.healing_combat_cooldown - combat_timeouts.get(ship.id, GameStats.healing_combat_cooldown)} turns.")
                    continue

                hull_to_repair = ship.action_param_1

                # apply adjustment
                if price_increase:
                    price_adjustment = GameStats.repair_markup
                elif price_decrease:
                    price_adjustment = GameStats.repair_discount
                else:
                    price_adjustment = 1.0

                if self.sell_prices is None:
                    self.sell_prices = get_material_sell_prices(universe)
                if self.median_sell_price is None:
                    self.median_sell_price = get_median_material_price(self.sell_prices)

                repair_cost = math.floor(get_repair_price(self.median_sell_price) * price_adjustment)

                payment = hull_to_repair * repair_cost

                #  cannot afford repair, set to most that ship can pay
                if payment > ship.credits:
                    payment = ship.credits
                    hull_to_repair = math.floor(payment / repair_cost)
                    payment = hull_to_repair * repair_cost

                #  cannot repair that much, decrease to match
                if hull_to_repair > ship.max_hull - ship.current_hull:
                    hull_to_repair = ship.max_hull - ship.current_hull
                    payment = hull_to_repair * repair_cost  # no need to check price again, price only drops

                ship.credits -= payment
                ship.current_hull += hull_to_repair

                self.print(f"Ship successfully repaired. Amount healed: {hull_to_repair} New Health: {ship.current_hull} Price: {payment}")
                self.events.append({
                    "type": LogEvent.manual_repair,
                    "ship_id": ship.id,
                    "repair_amount": hull_to_repair,
                    "payment": payment
                })

