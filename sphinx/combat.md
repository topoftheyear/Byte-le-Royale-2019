# Combat

Combat is a common occurrence in space, whether you initiate it or get attacked. 

Combat occurs simultaneously to allow
both ships to destroy each other in the same step. 

To attack another ship, call `self.attack(ship_to_attack)`, where `ship_to_attack` is the target.

While in battle, you can check your health by looking at the `self.current_hull`. If this is 0, your ship is dead.

If the target is in range, you will attack them.

## Respawning

When your ship dies, the following events happen:
* Your cargo is destroyed and converted to salvage.
* Your ship will respawn in the Secure Station in 10 turns.
* If you were a pirate, your notoriety is reduced to +4 (1 below Pirate threshold).
* Any illegal modules are removed from your ship.