# Writing Your AI

There is a base AI that will have a structure of how the AI should work. 
 
## Functions to Use

Functions that can be utilized by the ship: (further indented ones are helper methods)

### Ship Actions 
Your ship may perform up to one action each turn, and one move each turn.


 * `self.mine()` - Sets action to mine.
 * `self.repair(hull_to_repair)` - Repair `hull_to_repair` amount of hull for the current market rate.
 * `self.attack(target)` - Sets ship action to attack `target`.
 * `self.sell_material(material_type, amount)` - Sell `amount` of `material_type` to the station in range.
 * `self.buy_module (module, upgrade_level, ship_slot)` - Attempt to buy module `module` at level `upgrade_level` in slot `ship_slot`.
 * `self.drop_cargo(material_type, amount)` - Drop `amount` of `material_type` as illegal salvage (amount must be more than 10).
 * `self.collect_illegal_salvage()` - Attempt to collect some illegal salvage in the area.
 * `self.unlock_module()` - Spend credits to unlock a module slot, fails if you do not have enough credits. 
 * `self.pay_off_bounty()` - Pay off your bounty if you can afford to pay off all of it.

### Ship Movement
 Your ship may perform one movement per turn

 * `self.move(x, y)` - Move to position (x,y).


### Helper Methods

#### Getting Objects of a certain type
 * `self.get_ships (universe, callback)` - Get list of the ships in the area, of which callback allows for checking specific ships (ship, police, enforcer).
 * `self.get_asteroid_fields(universe)` - Get list of asteroid fields in the universe.
 * `self.get_stations(universe)` - Get list of stations in the universe.

#### Finding Distances / Checking if in radius
 * `self.distance_to_object(your_ship, target)` - Return distance between your ship and `target`.
 * `self.distance_to_coordinate(your_ship, xy_coords)` - Return distance between your ship and `xy_coords`.
 * `self.in_radius_of_asteroid_field(your_ship, field)` - Determines if your ship is in range of asteroid field. Returns `True` if mining would yield results.
 * `self.in_radius_of_station(your_ship, station)` - Returns `True` if in range of `station`. If `True`, can do the following actions:
 * `in_radius_of_illegal_salvage(your_ship, salvage)` - Returns `True` if your ship can gather from the pile of salvage.
 * `in_secure_zone(check)` - Returns `True` if `check` is in secure zone.
 * `self.ships_in_attack_range(universe)` - Return list of ships in attack range.
 * `self.in_weapons_range(self, your_ship, target_ship)` - Returns `True` if `target_ship` is in range.

##### Finding Prices
 * `get_repair_price(median_price)` - get the price to repair your ship.
 * `self.buy_material(amount)` - Buy `amount` of the production material of the station in range.
 * `self.get_median_price_info(universe)` - ONLY USE THIS ONCE A TURN - returns dictionary with sell_prices, buy_prices, best_import_prices, and best_export_prices.
 * `self.get_median_material_price(material_prices)` - Provide 
 * `self.get_module_price(median_price, ship_slot)` - Return module price at `ship_slot` with `median_price`
 * `self.get_module_unlock_price(median_price, ship_slot)` - Return module slot price at `ship_slot` with `median_price`

#### Other
 * `self.get_material_name(material_type)` - Return name of `material_type`.
 * `get_material_to_scrap_conversion(quantity, value)` - Given `quantity` of `material_value`, returns amount of illegal scrap created by destroying a ship with this amount of `material_value`.

### Enumeration Values
#### `ObjectType`
* `ObjectType.ship`
* `ObjectType.station`
* `ObjectType.black_market_station`
* `ObjectType.secure_station`
* `ObjectType.goethite_field`
* `ObjectType.cuprite_field`
* `ObjectType.gold_field`
* `ObjectType.material`
* `ObjectType.police`
* `ObjectType.enforcer`
* `ObjectType.illegal_salvage`

#### `MaterialType`
* `MaterialType.iron`
* `MaterialType.steel`
* `MaterialType.copper`
* `MaterialType.circuitry`
* `MaterialType.pylons`
* `MaterialType.weaponry`
* `MaterialType.machinery`
* `MaterialType.computers`
* `MaterialType.drones`
* `MaterialType.gold`
* `MaterialType.goethite`
* `MaterialType.cuprite`
* `MaterialType.wire`
* `MaterialType.salvage`

#### `ShipSlot`
* `ShipSlot.zero`
* `ShipSlot.one`
* `ShipSlot.two`
* `ShipSlot.three`

#### `ModuleType`
* `ModuleType.locked`
* `ModuleType.empty`
* `ModuleType.hull`
* `ModuleType.engine_speed`
* `ModuleType.weapons`
* `ModuleType.cargo_and_mining`
* `ModuleType.sensors`


## Imports and Rules

ONLY the following imports are allowed:
  * `math`
  * `itertools`
  * `collections`
  * `random`
  * `game.common.enums`
  * `game.client.user_client`
  
Any other import statements will prevent the AI from running.


There are some [rules that your AI must follow](rules.html).

## Related Links
* [Using the Visualizer](using_the_visualizer.html)
