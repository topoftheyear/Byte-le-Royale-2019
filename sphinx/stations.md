# Stations

Stations are the places where you will buy, sell, and trade resources. When you get in range, you can 
use your action for the turn to [trade](trading.md) with the station.
The stations will take the primary imports and use them to produce the stated output.
In addition, the amount of secondary product will help speed up the production.

[](_static/simple_station.png)
## Station API

```
name - name of station
position - x,y of station

[primary/secondary]_import - the stations primary and (if applicable) secondary imports
[primary/secondary]_consumption_qty - quantity that is consumed in one tick
[primary/secondary]_max - total amount station can store

production_frequency - how often to consume inputs for creating output
production_material - what is produced
production_qty - how much is stored
production_max - max amount of produced stuff to store

base_sell_price - initial sell price
base_primary_price - initial primary resource buying price
base_secondary_price - initial secondary resource buying price

sell_price - current sell price
primary_price - current primary resource buying price
secondary_price - current secondary resource buying price

```

## Stats

Listed below is the stats for each station.
```
+----+-------------------------+----------------+----------------------+-----------+
| ID | Station Name            | Position (x,y) | Import (Secondary)   | Produced  |
+====+=========================+================+======================+===========+
| s0 | Wire Station            | 400, 70        | Copper (N/A)         | Wire      | 
+----+-------------------------+----------------+----------------------+-----------+
| s1 | Computers Station       | 630, 56        | Circuitry (N/A)      | Computers | 
+----+-------------------------+----------------+----------------------+-----------+
| s2 | Circuitry Station       | 900, 266       | Gold (Wire)          | Circuitry | 
+----+-------------------------+----------------+----------------------+-----------+
| s3 | Drones Station          | 960, 665       | Weaponry (N/A)       | Drones    |
+----+-------------------------+----------------+----------------------+-----------+
| s4 | Pylon Station           | 25, 420        | Circuitry (N/A)      | Pylons    | 
+----+-------------------------+----------------+----------------------+-----------+
| s5 | Machinery Station       | 85, 280        | Steel (Pylons)       | Machinery | 
+----+-------------------------+----------------+----------------------+-----------+
| s6 | Copper Station          | 50, 630        | Cuprite (Drones)     | Copper    |
+----+-------------------------+----------------+----------------------+-----------+
| s7 | Steel Station           | 920, 21        | Iron (Drones)        | Steel     |
+----+-------------------------+----------------+----------------------+-----------+
| s8 | Iron Station            | 600, 560       | Goethite (Machinery) | Iron      | 
+----+-------------------------+----------------+----------------------+-----------+
| s9 | Weaponry Station        | 150, 406       | Computers (N/A)      | Weaponry  | 
+----+-------------------------+----------------+----------------------+-----------+
| s! | `***** ****** !`        | **0, !&%       | `8Wo`                | ()$()     | 
+----+-------------------------+----------------+----------------------+-----------+
| s@ | `***** ****** @`        | !00, %^0       | `@&@`                | ()$()     | 
+----+-------------------------+----------------+----------------------+-----------+
| s# | Station Authority       | 500, 350       | None                 | None      |
+----+-------------------------+----------------+----------------------+-----------+
```
