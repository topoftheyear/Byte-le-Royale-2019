# Bounty Hunting, Lawfulness, and Piracy

## Introduction

In the violent galaxy, people work hard and fight for their pay. Some of these jobs are more legal than others. 
This page outlines how bounty hunting and piracy are categorized, how to become a pirate or bounty hunter, and a helpful notoriety table and scale

## Bounty Hunting

Bounty hunters are the lawless law officers. They will go outside the law to stop pirates and are on the good side of the Notoriety Scale.
Bounty hunters can claim the bounties of the pirates they kill.
Bounty hunters have a notoriety of -5 or lower. They will appear as a light blue ship on the visualizer.

## Pirates and Piracy

Piracy is the way to gain money and ill-begotten gains for yourself, at the expense of the profits of others. 
While pirates can't return to the central station (unless they attempt to pay off their bounty),
they can sell salvage worth `150` credits per amount and get illegal - but powerful - modules at the Black Market Stations.
Pirates have a notoriety of 5 or higher. They will appear as an orange ship on the visualizer.
For each non-pirate ship that a pirate kills, they have a bounty added to themselves equal to 10% of the target's credits.
If a ship becomes a pirate, they gain a bounty on themselves equal to 10% of their credits.

## Police

The police are AI ships that are sent to take out pirates and other notorious vehicles.
If your notoriety is above the pirate threshold, the police will begin to attack if your ship is in range of the central station or is spotted by a patrol ship.
In addition, if your notoriety goes too high, enforcers will be sent out to destroy you. They are even more powerful police ships, and will give chase until you or themselves are destroyed.
  
## Lawfulness

Lawfulness is measured by the `ship.notoriety` statistic, showing how good or evil a player is. A higher notoriety means a player is less lawful and more aggressive.

If notoriety increases, police ships will chase the player when nearby the central station.
If your notoriety goes too high, you will be labeled a pirate.
Pirates are forbidden to access the Secure Station and a radius around the secure station UNLESS they pay off their bounty.
Any pirates within the Secure Zone will be fired upon by the police.
Additionally, citizens and bounty hunters are free to hunt down pirates without fear of reprisal from law enforcement.
Non-pirates will claim the bounties that the pirates rack up upon death of the pirate.
If private citizens, bounty hunters and police are unable to curb an especially menacing pirate, Enforcers may be sent out in waves to bring the pirate ship down.


```
+-----------------------------------+-----------+
| Action                            | Notoriety |
+===================================+===========+
| Destroying Pirate Ship            | - 2       |
+-----------------------------------+-----------+
| Paying Off Bounty                 | - 1       |
+-----------------------------------+-----------+
| Caught Carrying an Illegal Module | + 1       |
+-----------------------------------+-----------+
| Attacking Police Ship             | + 1       | 
+-----------------------------------+-----------+
| Destroying Civilian Ship          | + 2       | 
+-----------------------------------+-----------+
| Destroying Bounty Hunter Ship     | + 3       | 
+-----------------------------------+-----------+
| Destroying Police Ship            | + 4       |
+-----------------------------------+-----------+
| Destroying Enforcer Ship          | + 5       |
+-----------------------------------+-----------+
```

## Scale of Notoriety

```
-10         -5          0         +5        +10
<-|----------|----------|----------|----------|->
             |                     |
          Bounty                Pirate   
          Hunter              Notoriety
        -5 or less            +5 or more
```



## Related Links

[Combat](combat.html)
