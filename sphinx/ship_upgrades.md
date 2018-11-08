# Ship Upgrades

Your ship has ability to improve through modules. These modules can enhance different facets of the ship
and can help your ship perform to the best of its capabilities.

Your ship will only have access to 4 total slots, and the unlock cost will increase per slot, so choose your modules wisely.

## List of Modules

There are 7 different modules a ship can have:
* `Hull Strength` - How much damage you can take
* `Engine Speed` - How fast your ship moves in one action
* `Weapon Damage` - How powerful the weapon is
* `Weapon Range` - How far away your ship can attack enemies
* `Cargo Space` - How much space your ship has to store items
* `Mining Yield` - How fast your ship can mine
* `Sensor Range` - How far your ship's sensors can detect ships

## How To Upgrade

In order to purchase a module you must specify the module slot to install it to.
The first module slot is free, however additional module slots must be purchased for additional modules to be installed.


To purchase modules, go to the center station and use the `buy_module` function.
For any modules, you must purchase an additional slot for the module from the selling [Stations](stations.md).
- For module levels 1 and 2, these are purchasable at the `Station Authority` [Station](stations.md).
- For module levels 3, these are purchasable at the `*Black Market 1/2` [Stations](stations.md).
  - Be warned, these are the illegal modules. They are lost on death and will cost you notoriety.

## Module Table

```eval_rst
+---------------+---------+---------+---------+---------+
| Module  Name  | Level 0 | Level 1 | Level 2 | Level 3 |
+===============+=========+=========+=========+=========+
| Hull Strength | 1000    | 2000    | 3000    | 8000    |
+---------------+---------+---------+---------+---------+
| Engine Speed  | 5       | 7       | 9       | 200     |
+---------------+---------+---------+---------+---------+
| Weapon Damage | 10      | 20      | 30      | 200     |
+---------------+---------+---------+---------+---------+
| Weapon Range  | 50      | 75      | 100     | 200     |
+---------------+---------+---------+---------+---------+
| Cargo Space   | 500000  | 650000  | 800000  | 1000000 |
+---------------+---------+---------+---------+---------+
| Mining Yield  | 50000   | 65000   | 80000   | 100000  |
+---------------+---------+---------+---------+---------+
| Sensor Range  | 75      | 100     | 125     | 150     |
+---------------+---------+---------+---------+---------+
```

## Related Links

* [Combat](combat.md)