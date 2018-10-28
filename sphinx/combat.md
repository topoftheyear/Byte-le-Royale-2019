# Combat

Combat is a common occurrence in space, whether you initiate it or get attacked. Fighting has a simple step-by-step of actions:

* Step 1: ```Ship 1``` declares ```Ship 2``` as Target.
* Step 2: ```Ship 1``` determines if ```Ship 2``` is in range.
  * if in range, Step 3; otherwise, exit combat.
* Step 3: ```Ship 1``` fires at ```Ship 2```.
  * Step 3a: ```Ship 1``` deals damage to ```Ship 2```.
  * Step 3b: If ```Ship 2``` is Police or Enforcer, increase notoriety.
  * Step 3c: If ```Ship 2```'s hull is 0, destroy ship and set respawn timer.
  * Step 3d: Update `Ship 1`'s notoriety dependent on type of ship ```Ship 2``` wsa and the standing of ``Ship 1``.

## Related Links

[Ships](ships.md)
[Notoriety](notoriety.md) #CHANGE THIS LINE