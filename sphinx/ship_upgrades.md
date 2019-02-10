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
For any modules, you must purchase an additional slot for the module from the selling [Stations](stations.html).
- For module levels 1, 2, and 3, these are purchasable at the `Station Authority` and `Black Market 1 & 2` [Station](stations.html).
- For the Illegal Module Level, these are purchasable at the `Black Market 1 & 2` [Stations](stations.html).
  - Be warned, these are the illegal modules. They are lost on death and will cost you notoriety.

## Module Table

```eval_rst
+---------------+---------+---------+---------+---------+---------+
| Module Name   | Level 0 | Level 1 | Level 2 | Level 3 | Illegal |
+===============+=========+=========+=========+=========+=========+
| Hull Strength | 1000    | 3645    | 4506    | 6243    | 10000   |
+---------------+---------+---------+---------+---------+---------+
| Engine Speed  | 5       | 7       | 9       | 11      | 15      |
+---------------+---------+---------+---------+---------+---------+
| Weapon Damage | 83      | 270     | 458     | 645     | 2081    |
+---------------+---------+---------+---------+---------+---------+
| Weapon Range  | 25      | 50      | 75      | 100     | 125     |
+---------------+---------+---------+---------+---------+---------+
| Cargo Space   | 500     | 600     | 700     | 800     | 1000    |
+---------------+---------+---------+---------+---------+---------+
| Mining Yield  | 5       | 6       | 7       | 8       | 10      |
+---------------+---------+---------+---------+---------+---------+
| Sensor Range  | 75      | 100     | 125     | 150     | 175     |
+---------------+---------+---------+---------+---------+---------+
```

## Module Price Table

Module and module slot prices are dependent on the median price of all the materials in the universe. To find the cost
of a module or a module slot, take the price listed below and multiply it by the median price in the universe.

Please note that all ships are outfitted with the level 0 modules, and all ships start with module slot 0.
+----------------+---------+---------+---------+---------+---------+
| Module Upgrade | Level 0 | Level 1 | Level 2 | Level 3 | Illegal |
+================+=========+=========+=========+=========+=========+
| Price          | base    | 100     | 400     | 900     | 1600    |
+----------------+---------+---------+---------+---------+---------+

+---------------+---------+---------+---------+---------+
| Module Slot   | Slot  0 | Slot 1  | Slot 2  | Slot 3  |
+===============+=========+=========+=========+=========+
| Price         | base    | 150     | 225     | 300     |
+---------------+---------+---------+---------+---------+

## Related Links

* [Combat](combat.html)