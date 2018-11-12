# Ships

The ship is the basis for all actions taken in the game. Each player's AI controls a ship. The ship can
move around to the various points, 

[](_static/simple_ship.png)
## Ship Interactions

Every turn, each ship will first use their action, then they will move.
- Actions
  - `Combat` (more info [Here](combat.md))
  - `Mining` (more info [Here](asteroid_fields_and_mining.md))
  - `Buy module` (more info [Here](ship_upgrades.md))
  - `Buy material`
  - `Sell material` (more on buying and selling [Here](trading.md))
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
    - `module_0` - component in module 0
    - `module_1` - component in module 1
    - `module_2` - component in module 2
    - `module_3` - component in module 3
    
    - `module_0_level` - level of component in module 0
    - `module_1_level` - level of component in module 1
    - `module_2_level` - level of component in module 2
    - `module_3_level` - level of component in module 3
  - **Actions:**
    - `action` - action to be taken
    - `action_param_1` - First parameter for action to be taken.
    - `action_param_2` - Second parameter for action to be taken.
    - `action_param_3` - Third parameter for action to be taken.
    - `move_action` - movement to be taken
  - **Other:**
    - `respawn_counter` - time until respawn
    - `credits` - total number of credits possessed
    
- Stats you get from **OTHER AND YOUR** ships:
  - `public_id` - Ship's Public ID
  - `is_npc` - Is the ship an NPC?
  - `max_hull` - Ship's max hull
  - `current_hull` - Ship's current hull
  - `cargo_space` - Ship's cargo space
  - `position` - Ship's position
  - `inventory` - Ship's inventory
  - `notoriety` - Notoriety of the ship
  - `legal_standing` - Legal standing of the ship
