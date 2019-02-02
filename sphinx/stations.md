# Stations

Stations are the places where you will buy, sell, and trade resources. When you get in range, you can 
use your action for the turn to [trade](trading.html) with the station.
The stations will take the primary imports and use them to produce the stated output.
In addition, the amount of secondary product will help speed up the production.

Note: the Black Market Stations have imports or produce anything; they only trade modules.

[](_static/simple_station.png)
## Station API

- `name` - name of station
- `position` - x,y of station

- `primary_import` - the station's primary import
- `secondary_import` - the station's secondary import
- `primary_consumption_qty` - quantity of primary import that is consumed in one tick
- `secondary_consumption_qty` - quantity of secondary import that is consumed in one tick
- `primary_max` - The total amount of the station's primary import that a station can store
- `secondary_max` - The total amount of the station's secondary import that a station can store

- `production_frequency` - how often to consume inputs for creating output
- `production_material` - what is produced
- `production_qty` - how much is stored
- `production_max` - max amount of produced stuff to store

- `base_sell_price` - The base selling price for the produced item.
- `base_primary_price` - The base price the station will pay for the primary import.
- `base_secondary_price` - The base price the station will pay for the secondary import.

- `sell_price` - The station's current sell price for the produced item.
- `primary_price` - The station's current buy price for the primary import.
- `secondary_price` - The station's current buy price for the secondary import.

## Stats

Listed below are the stats for each station.
```
+-------------------------+----------------+----------------------+-----------+
| Station Name            | Position (x,y) | Import (Secondary)   | Produced  |
+=========================+================+======================+===========+
| Wire Station            | 400, 70        | Copper (N/A)         | Wire      |
+-------------------------+----------------+----------------------+-----------+
| Computers Station       | 630, 56        | Circuitry (N/A)      | Computers | 
+-------------------------+----------------+----------------------+-----------+
| Circuitry Station       | 900, 266       | Gold (Wire)          | Circuitry | 
+-------------------------+----------------+----------------------+-----------+
| Drones Station          | 960, 665       | Weaponry (N/A)       | Drones    |
+-------------------------+----------------+----------------------+-----------+
| Pylon Station           | 25, 420        | Circuitry (N/A)      | Pylons    | 
+-------------------------+----------------+----------------------+-----------+
| Machinery Station       | 85, 280        | Steel (Pylons)       | Machinery | 
+-------------------------+----------------+----------------------+-----------+
| Copper Station          | 50, 630        | Cuprite (Drones)     | Copper    |
+-------------------------+----------------+----------------------+-----------+
| Steel Station           | 920, 21        | Iron (Drones)        | Steel     |
+-------------------------+----------------+----------------------+-----------+
| Iron Station            | 600, 560       | Goethite (Machinery) | Iron      | 
+-------------------------+----------------+----------------------+-----------+
| Weaponry Station        | 150, 406       | Computers (N/A)      | Weaponry  | 
+-------------------------+----------------+----------------------+-----------+
| `Black Market 1`        | 880, 175       | None                 | None      | 
+-------------------------+----------------+----------------------+-----------+
| `Black Market 2`        | 100, 560       | None                 | None      | 
+-------------------------+----------------+----------------------+-----------+
| Station Authority       | 500, 350       | None                 | None      |
+-------------------------+----------------+----------------------+-----------+
```
