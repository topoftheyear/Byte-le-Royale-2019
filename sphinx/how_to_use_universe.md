# How to Use Universe
`universe.get()` is the main command to get information on the universe. You are able to do the following with it:
* Stations:
    * `universe.get(ObjectType.secure_station)` - returns a 1-element list of Secure Stations. (using `universe.get(ObjectType.secure_station)[0]` to access the secure station)
    * `universe.get(ObjectType.station)` - returns a list of trading stations (no black market or secure stations)
    * `universe.get(ObjectType.black_market_station)` - returns the list of black market stations.
    * `universe.get("all_stations")` - This list contains all stations, including the `ObjectType.secure_station` and `ObjectType.black_market_station`.

* Ships:
    * `universe.get(ObjectType.ship)` - List of ships in the universe (not police or enforcers)
    * `universe.get("police")` - This is how to receive a list of police and enforcers in the universe.
    * `universe.get("ships")` -  This returns a list of ships in the universe, including the police and enforcer ships.

* Additional Spots:
    * `universe.get(ObjectType.illegal_salvage)` - Returns the list of illegal salvage spots around the map
    * `universe.get("asteroid_fields")` - Using this command returns a list of asteroid fields.
    
## How to Convert to the New Format
* Initializing station and ship lists
  * Instead of
  ```python3
      for obj in universe.dump():
          if obj.object_type is ObjectType.station and obj.object_type not in [ObjectType.secure_station, ObjectType.black_market_station]:
              [list_of_trade_stations].append(obj)
          elif obj.object_type is ObjectType.ship:
              [list_of_ships].append(obj)
  ```
  use
  ```python3
    [list_of_ships] = universe.get(ObjectType.ship)
    [list_of_trade_stations] = universe.get(ObjectType.station)
  ```
* For Loops
  * Instead of 
  ```python3
    for obj in universe.dump():
       if obj.object_type is [Some_Object_Type]:
        [list_of_Some_Object_Type].append(obj)
  ```
  use
  ```python3
    for obj in universe.get([Some_Object_Type]):
        [list_of_Some_Object_Type].aplpend(obj)
  ```