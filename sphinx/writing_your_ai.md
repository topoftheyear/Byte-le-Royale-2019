# Writing Your AI

There is no inherently right or wrong way to write your AI. There are however a few things to take note of:

* Except for the built-in libraries, no imports.
* Do not attempt to collect information on your opponent's ship that can't be directly observed.
* Avoid processes and procedures that will take an abnormally long time per turn. If the time to take a turn becomes too long, your ship will automatically take a turn.

## Functions to Use

Functions that can be utilized by the ship:

* `move(x, y)` - Move to position (x,y)
* `mine()` - Set's action to mine
* `attack (target)` - Set ship action to target
* `buy_module (module, upgrade_level, ship_slot)` - buy module `module` at level `upgrade_level` in slot `ship_slot`
* `get_ships (universe, callback)` - get list of the ships in the area, of which callback allows for checking specific ships (ship, police, enforcer)
* `get_stations(universe)` - get list of stations in the universe
* `get_asteroid_fields(universe)` - get list of asteroid fields in the universe
* `ships_in_attack_range(universe)` - list of ships in attack range 
* `sell_material(material, amount)` - sell `amount` of `material` to the station in range
* `buy_material(material, amount)` - buy `amount` of `material` to the station in range
* `unlock_module()` - unlock the module slot

## Related Links
* [Using the Visualizer](using_the_visualizer.md)