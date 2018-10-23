#Asteroid Fields
Asteroid fields are where players can mine various resources which they can then sell to a ```station```. On our map there are three different types of fields, ```cuprite```, ```goethite```, and ```gold```.There are a few variables that players can view for each of the fields:
* Name: ```field.name```
* Position: ```field.position```
* Material Type: ```field.material_type```
* Mining Rate: ```field.mining_rate```
* Accessibility Radius: ```field.accessibility_radius```

The following shows what [Stations](stations.md) these fields resources can be used and the secondaries that boost the output:
* Cuprite
    * S6: makes Copper, secondary is Drones
* Goethite
    * S8: makes Iron,  secondary is Machinery
* Gold
    * S2: makes Circuitry, secondary is Wire
 
##Mining
When mining one of these fields players will get that resource added to their ships inventory. The amount of material that will be mined will be the ships ``mining_yield`` multiplied by the fields ``mining_rate``
##Stub for mining









