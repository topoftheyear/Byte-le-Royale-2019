# Ships

The ship is the basis for all actions taken in the game. Each player's AI controls a ship that you command.

## Ship Interactions

Every turn, each ship gets 2 actions to do; a movement action, and a non-movement action
- Non-movement
  - `Combat`
  - `Mining`
  - `Buy module`
  - `Buy material`
  - `Sell material`
- Movement

## Ship Attributes

- Stats you get from **YOUR** ship:
  - **Ship stats:**
    - `engine_speed` - speed of the ship
    - `weapon_damage` - strength of ship's weapon
    - `weapon_range` - range of attack from weapon
    - `cargo_space` - amount of storage ship has
    - `mining_yield` - mining capability
    - `sensor_range` - range sensors can pick up
  - **Module stats:**
    - `module_(0,1,2,3)` - component in module 0, 1, 2, or 3
    - `module_(0,1,2,3)_level` - level of corresponding module
  - **Actions:**
    - `action` - action to be taken
    - `action_param_(1,2,3)` - parameter of action if needed
    - `move_action` - movement to be taken
  - **Other:**
    - `respawn_counter` - time until respawn
    - `credits` - total number of credits possessed
- Stats you get from **OTHER** ships:
  - `public_id` - Ship's Public ID
  - `is_npc` - Is the ship an NPC?
  - `max_hull` - Ship's max hull
  - `current_hull` - Ship's current hull
  - `cargo_space` - Ship's cargo space
  - `position` - Ship's position
  - `inventory` - Ship's inventory
  - `notoriety` - Notoriety of the ship
  - `legal_standing` - Legal standing of the ship
  
## Ship API
  
```
To add in future.
```

## Related Pages
* [Bounty Hunting / Piracy](bounty_hunting_lawfulness_and_piracy.md)
* [Combat](combat.md)
* [Mining](asteroid_fields_and_mining.md)
* [Ship Upgrades](ship_upgrades.md)
* [Trading](trading.md)