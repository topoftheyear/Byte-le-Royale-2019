Document:

A what properties a station object has: see game/common/station.py
A blank section for the station object's api.
Each of the station's stats in a table: see game/universe_config.py
For an example of how to do the tables see: byte-le 2018 docs Note it has to be viewed as raw text otherwise github tries to render the markdown
document how supplemental materials work to speed the production speed of new materials.
Done When:

New documentation file should go in sphinx/stations.md and a new link to the page needs to be added to the index page
Build the documentation using one of the build scripts in the sphinx directory, then cd to the docs directory and run python -m http.server to view the documentation in a browser (requires python 3, if you don't have it get it).

#Station

Stations are the places that you will buy, sell, and trade resources at.

##API:

##Stats (Subject to Change)

Listed below is the stations' stats:
+------------+------+-----------+
| Station ID | Station Name | Position | Import (Secondary) | Produced |
| s6 | Copper Station | 0.05, 0.9 | Cuprite (Drones) | Copper |
| s4 | Pylon Station | 0.025, 0.6 | Circuitry (N/A) | Pylons | 
| s9 | Weaponry Station | 0.15, 0.58 | Computers (N/A) | Weaponry | 
| s5 | Machinery Station | 0.085, 0.40 | Steel (Pylons) | Machinery | 
| s0 | Wire Station | 0.4, 0.10 | Copper (N/A) | Wire | 
| s8 | Iron Station | 0.6, 0.80 | Goethite (Machinery)| Iron | 
| s1 | Computers Station | 0.63, 0.08 | Circuitry (N/A) | Computers | 
| s2 | Circuitry Station | 0.90, 0.38 | Gold (Wire) | Circuitry | 
| s3 | Drones Station | 0.96, 0.95 | Weaponry (N/A) | Drones |
| s7 | Steel Station | 0.92, 0.03 | Iron (Drones) | Steel |
| s▓ | ▓▓▓▓▓ ▓▓▓▓▓▓ ▓ | 0.▓, 0.▓▓ | ▓▓▓ | ▓▓▓ | 
| s▓ | ▓▓▓▓▓ ▓▓▓▓▓▓ ▓ | 0.▓, 0.▓▓ | ▓▓▓▓ | ▓▓▓▓ | 
| s911 | Station Authority | 0.5, 0.5 | None | None | None |