# Asteroid Fields

## Mining

Asteroid fields are where players can mine various resources which they can then sell to a ```station```. On our map there are three different types of fields, ```cuprite```, ```goethite```, and ```gold```.There are a few variables that players can view for each of the fields:
* Name: ```field.name```
* Position: ```field.position```
* Material Type: ```field.material_type```
* Mining Rate: ```field.mining_rate```
* Accessibility Radius: ```field.accessibility_radius```

The following shows what [Stations](stations.html) these fields resources can be used and the secondaries that boost the output:
* Cuprite
    * S6: makes Copper, secondary is Drones
* Goethite
    * S8: makes Iron, secondary is Machinery
* Gold
    * S2: makes Circuitry, secondary is Wire
 

To mine from an asteroid field, approach the field and call `self.mine()` in the client to obtain the resources.


Listed below are the stats for each asteroid field.
```
+---------------------+----------------+-------------+-------------+
| Field Name          | Position (x,y) |  Produces   | Mining Rate |
+=====================+================+=============+=============+
| Gold Field          | 850, 595       | Gold        | 0.4         |
+---------------------+----------------+-------------+-------------+
| Goethite Field      |  50,  35       | Goethite    | 0.55        |
+---------------------+----------------+-------------+-------------+
| Cuprite Field       | 500, 850       | Cuprite     | 0.7         |
+---------------------+----------------+-------------+-------------+