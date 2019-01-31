# Writing Your AI

There is a base AI that will have a structure of how the AI should work. 
 
## Functions to Use

Functions that can be utilized by the ship: (further indented ones are helper methods)

* `self.move(x, y)` - Move to position (x,y).
  * `distance_to_object(your_ship, target)` - Return distance between your ship and `target`.
  * `distance_to_coordinate(your_ship, xy_coords)` - Return distance between your ship and `xy_coords`.

* `get_asteroid_fields(universe)` - Get list of asteroid fields in the universe.
  * `in_radius_of_asteroid_field(your_ship, field)` - Determines if your ship is in range of asteroid field. Returns `True` if mining would yield results.
* `self.mine()` - Sets action to mine.

* `get_ships (universe, callback)` - Get list of the ships in the area, of which callback allows for checking specific ships (ship, police, enforcer).
  * `universt_by_object_type(flat_universe)` - Return a dictionary of object types ex: `({ ObjectType.ship: [<list of ships>], ObjectType.stations:[<list of stations>]})`

* `ships_in_attack_range(universe)` - Return list of ships in attack range.
  * `in_weapons_range(self, your_ship, target_ship)` - Returns `True` if `target_ship` is in range.
* `attack (target)` - Sets ship action to attack `target`.

* `get_stations(universe)` - Get list of stations in the universe.
  * `in_radius_of_station(your_ship, station)` - Returns `True` if in range of `station`. If `True`, can do the following actions:
* `repair(hull_to_repair)` - Repair `hull_to_repair` amount of hull for the current market rate.
  * `get_repair_price(median_price)` - get the price to repair your ship.
* `buy_material(material, amount)` - Buy `amount` of `material` to the station in range.
  * `get_median_price_info(universe)` - ONLY USE THIS ONCE A TURN - returns dictionary with sell_prices, buy_prices, best_import_prices, and best_export_prices.
* `sell_material(material, amount)` - Sell `amount` of `material` to the station in range.
  * `get_material_name(material_type)` - Return name of `material_type`.
  * `get_median_material_price(material_prices)` - Provide 
* `buy_module (module, upgrade_level, ship_slot)` - Attempt to buy module `module` at level `upgrade_level` in slot `ship_slot`.
  * `get_module_price(median_price, ship_slot)` - Return module price at `ship_slot` with `median_price`
* `unlock_module()` - Unlock a module slot.
  * `get_module_unlock_price(median_price, ship_slot)` - Return module slot price at `ship_slot` with `median_price`

* `drop_cargo(material_type, amount)` - Drop `amount` of `material_type` as illegal salvage (amount must be more than 10).
  * `get_material_to_scrap_conversion(quantity, value)` - Given `quantity` of `material_value`, returns amount of illegal scrap created by destroying a ship with this amount of `material_value`.
* `collect_illegal_salvage()` - Attempt to collect some illegal salvage in the area.
  * `in_radius_of_illegal_salvage(your_ship, salvage)` - Returns `True` if your ship can gather from the pile of salvage.
* `pay_off_bounty()` - Pay off your bounty if you can afford to pay off all of it.
  * `in_secure_zone(check)` - Returns `True` if `check` is in secure zone.

## Imports and Rules

ONLY the following imports are allowed:
  * math
  * itertools
  * collections
  * random
  * game.common.enums
  * game.client.user_client
  
Any other import statements will prevent the AI from running.


There are some [rules that your AI must follow](rules.md).

## Related Links
* [Using the Visualizer](using_the_visualizer.md)