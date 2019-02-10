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
 * `self.buy_material(amount)` - Buy `amount` of the production material of the station in range.

### Ship Movement
 Your ship may perform one movement per turn

 * `self.move(x, y)` - Move to position (x,y).


### Helper Methods

#### Loading useful info from the universe

At the top of your `take_turn()` method, call `self.update_cached_data(universe)`.
This method will load a bunch of useful information from the universe. This change (part of v1.2) introduced breaking changes that simplify the api of all of the methods that rely on `median_price`.

Properties loaded:
- `self.asteroid_fields`: list of the three asteroid fields.
- `self.stations`: List of all of the stations.
- `self.police`: List of all of the police ships.
- `self.ships`: List of all ships, excluding police.
- `self.sell_prices`: A dictionary of material types to sell price for the given material.
- `self.buy_prices`: A dictionary of material types to buy price for the given material.
- `self.best_export_prices`: A dictionary of material types to another dictionary containing the sell price and what station is offering that price.
- `self.best_import_prices`: A dictionary of material types to another dictionary containing the buy price and what station is offering that price.


**Best Export Prices example:**
```python
print(self.best_export_prices)
{
    3:{'export_price': 233, 'station': <Station: 161bc414-be02-4624-85e1-e8386b52fc80>}, 
    5: {'export_price': 217, 'station': <Station: 15835be7-c40a-439c-a134-0ab3c30424d4>}, 
    6: {'export_price': 282, 'station': <Station: 6387faa8-4d4b-4313-a5a4-c171e81c1c47>}, 
    7: {'export_price': 254, 'station': <Station: ef4a980a-44c4-41bc-b429-1557ccd329d9>}, 
    13: {'export_price': 163, 'station': <Station: 68a26979-fdf2-48e3-8677-53a4a665eeaa>}, 
    1: {'export_price': 190, 'station': <Station: 5b3d1e03-b037-4c29-80f6-2171901dc72d>}, 
    8: {'export_price': 266, 'station': <Station: 7ab9792f-7bb7-4a9c-a2d6-6fb9f4f7108b>}, 
    4: {'export_price': 263, 'station': <Station: 337683da-03a2-4c17-97ba-fe91af9098ff>}, 
    9: {'export_price': 289, 'station': <Station: 659e0226-1895-435f-8315-d10d9d8395a6>}, 
    2: {'export_price': 239, 'station': <Station: 1349ed91-79b4-4de4-b8a0-a6ff80034926>}
}
```



#### Getting Objects of a certain type
 * `universe.get(ObjectType.ship)` - Get list of the ships in the area, of which callback allows for checking specific ships (ship, police, enforcer).
 * `universe.get("asteroid_fields")` - Get list of asteroid fields in the universe.
 * `universe.get("all_stations")` - Get list of stations in the universe.

 Note: `universe.get()` takes any of the following object types and returns a list of objects.
 - `ObjectType.ship`
 - `ObjectType.cuprite_field`
 - `ObjectType.goethite_field`
 - `ObjectType.gold_field`
 - `ObjectType.secure_station`
 - `ObjectType.black_market_station`

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

 * `self.get_repair_price()` - get the price to repair your ship.
 * `self.get_module_price(ship_slot)` - Return module price for `ship_slot` 
 * `self.get_module_unlock_price(ship_slot)` - Return module slot price for `ship_slot` 

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
