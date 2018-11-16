# Ship Upgrades

Your ship has ability to improve through modules. These modules can enhance different facets of the ship
and can help your ship perform to the best of its capabilities.

Your ship will only have access to 4 total slots, and the unlock cost will increase per slot, so choose your modules wisely.

## List of Modules

There are 5 groupings of modules for the ship:
* `Hull Strength` - How much damage you can take
* `Engine Speed` - How fast your ship can move in one tick
* `Weapon Damage and Range` - How powerful the weapon is and what range you can attack enemies
* `Cargo Space and Mining Yield` - How much space your ship has to store items, and at what speed your ship can mine for resources
* `Sensor Range` - How far your ship's sensors can detect ships

## How To Upgrade

Your ship starts at level 0 for all categories. In order to purchase a module you must specify which module slot to place the module in.

To purchase modules, go to the center station and use the `buy_module` function. If you already have the module of the type you wish to upgrade, 
it will upgrade that module in the slot. If you do not already own that module type, you will need to purchase the module itself and the module slot.
Keep in mind, only 4 total slots for modules can be obtained (1 of which is provided for you), so choose your modules wisely.
For any modules, you must purchase an additional slot for the module from the selling [Stations](stations.md).
- For module levels 1, 2, and 3, these are purchasable at the `Station Authority` and `Black Market 1 & 2` [Station](stations.md).
- For the Illegal Module Level, these are purchasable at the `Black Market 1 & 2` [Stations](stations.md).
  - Be warned, these are the illegal modules. They are lost on death and will cost you notoriety.

## Module Table (Revise Illegal Numbers When Completed)

```eval_rst
+---------------+---------+---------+---------+---------+---------+
| Module Name   | Level 0 | Level 1 | Level 2 | Level 3 | Illegal |
+===============+=========+=========+=========+=========+=========+
| Hull Strength | 1000    | 2000    | 3000    | 4000    | 5000    |
+---------------+---------+---------+---------+---------+---------+
| Engine Speed  | 5       | 7       | 9       | 11      | 666     |
+---------------+---------+---------+---------+---------+---------+
| Weapon Damage | 10      | 20      | 30      | 40      | 50      |
+---------------+---------+---------+---------+---------+---------+
| Weapon Range  | 50      | 75      | 100     | 125     | 150     |
+---------------+---------+---------+---------+---------+---------+
| Cargo Space   | 500000  | 600000  | 700000  | 800000  | 1000000 |
+---------------+---------+---------+---------+---------+---------+
| Mining Yield  | 50000   | 60000   | 70000   | 80000   | 100000  |
+---------------+---------+---------+---------+---------+---------+
| Sensor Range  | 75      | 100     | 125     | 150     | 175     |
+---------------+---------+---------+---------+---------+---------+
```

## Related Links

* [Combat](combat.md)