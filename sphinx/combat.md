# Combat

Combat is a common occurrence in space, whether you initiate it or get attacked. 

Combat occurs simultaneously to allow
both ships to destroy each other in the same step. 

To attack another ship, call `self.attack(ship_to_attack)`, where `ship_to_attack` is the target.

While in battle, you can check your health by looking at the `ship.current_hull`. If this is 0, your ship is dead.

If the target is in range, you will attack them.

## Repair
After combat, ships it will be necessary for ships to repair their hulls.

The station authority provides passive repairing to ALL ships within its accessibility radius.
This can only occur while a ship is out of combat. Passive repair will provide a certain amount of hull back
after a certain amount of turns. To find these values, please refer to the game files.

All stations provide manual repair options. uUse the repair(hull_to_repair) action and provide the amount of hull you
want to get repaired. Manual repair comes at a fee: the price of repair is based on the median of all materials
on the market. Use the get_repair_price action for more information.

Note that the station authority is the only station that provides repair at its regular price. The black market
stations can provide repairs at a discounted price, while all other stations markup the price greatly.

## Respawning

When your ship dies, the following events happen:
* Your cargo is destroyed and converted to salvage.
* Your ship will respawn in the Secure Station in 10 turns.
* If you were a pirate, your notoriety is reduced to +4 (1 below Pirate threshold).
* Any illegal modules are removed from your ship.


## Abandoning the battlefield

Deserters will not be welcomed back! Leaving the bounds of the game area will immediately cause destruction of your
ship, which will cause you to drop all of your cargo and have you respawn. Note: this will also cause scrap to spawn
at the edges of the game area, so be wary while collecting scrap near the boundaries of space!