import math

from game.config import *
from game.common.enums import *
from game.utils.projection import *

STATION_DEFINITIONS = [
    {
        #s6 Copper
        "type": ObjectType.station,
        "coords": percent_world(0.05, 0.9),

        "primary_import": MaterialType.cuprite,
        "primary_consumption_qty": 1,
        "primary_max": 20,

        "secondary_import": MaterialType.drones,
        "secondary_consumption_qty": 1,
        "secondary_max": 10,

        "production_material": MaterialType.copper,
        "production_frequency": 1,
        "production_qty": 1,
        "production_max": 10,

        "cargo": {
            MaterialType.cuprite: 20,
            MaterialType.drones: 10
        }
    },
    {
        #s4 Pylons
        "type": ObjectType.station,
        "coords": percent_world(0.025, 0.6),

        "primary_import": MaterialType.circuitry,
        "primary_consumption_qty": 1,
        "primary_max": 20,

        "secondary_import": MaterialType.null,
        "secondary_consumption_qty": 1,
        "secondary_max": 10,

        "production_material": MaterialType.pylons,
        "production_frequency": 1,
        "production_qty": 1,
        "production_max": 100,

        "cargo": {

        }
    },
    {
        #s9 Weaponry
        "type": ObjectType.station,
        "coords": percent_world(0.15, 0.58),

        "primary_import": MaterialType.computers,
        "primary_consumption_qty": 1,
        "primary_max": 20,

        "secondary_import": MaterialType.null,
        "secondary_consumption_qty": 1,
        "secondary_max": 10,

        "production_material": MaterialType.weaponry,
        "production_frequency": 1,
        "production_qty": 1,
        "production_max": 100,

        "cargo": {

        }
    },
    {
        #s5 Machinery
        "type": ObjectType.station,
        "coords": percent_world(0.085, 0.40),

        "primary_import": MaterialType.steel,
        "primary_consumption_qty": 1,
        "primary_max": 20,

        "secondary_import": MaterialType.pylons,
        "secondary_consumption_qty": 1,
        "secondary_max": 10,

        "production_material": MaterialType.machinery,
        "production_frequency": 1,
        "production_qty": 1,
        "production_max": 100,

        "cargo": {

        }
    },
    {
        #s0 Wire
        "type": ObjectType.station,
        "coords": percent_world(0.4, 0.10),

        "primary_import": MaterialType.copper,
        "primary_consumption_qty": 1,
        "primary_max": 20,

        "secondary_import": MaterialType.null,
        "secondary_consumption_qty": 1,
        "secondary_max": 10,

        "production_material": MaterialType.wire,
        "production_frequency": 1,
        "production_qty": 1,
        "production_max": 100,

        "cargo": {

        }
    },
    {
        #s8 Iron
        "type": ObjectType.station,
        "coords": percent_world(0.6, 0.80),

        "primary_import": MaterialType.goethite,
        "primary_consumption_qty": 1,
        "primary_max": 20,

        "secondary_import": MaterialType.machinery,
        "secondary_consumption_qty": 1,
        "secondary_max": 10,

        "production_material": MaterialType.iron,
        "production_frequency": 1,
        "production_qty": 1,
        "production_max": 100,

        "cargo": {

        }
    },
    {
        #s1 Computers
        "type": ObjectType.station,
        "coords": percent_world(0.63, 0.08),

        "primary_import": MaterialType.circuitry,
        "primary_consumption_qty": 1,
        "primary_max": 20,

        "secondary_import": MaterialType.null,
        "secondary_consumption_qty": 1,
        "secondary_max": 10,

        "production_material": MaterialType.computers,
        "production_frequency": 1,
        "production_qty": 1,
        "production_max": 100,

        "cargo": {

        }
    },
    {
        #s2 Circuitry
        "type": ObjectType.station,
        "coords": percent_world(0.90, 0.38),

        "primary_import": MaterialType.gold,
        "primary_consumption_qty": 1,
        "primary_max": 20,

        "secondary_import": MaterialType.wire,
        "secondary_consumption_qty": 1,
        "secondary_max": 10,

        "production_material": MaterialType.circuitry,
        "production_frequency": 1,
        "production_qty": 1,
        "production_max": 100,

        "cargo": {

        }
    },
    {
        #s3 Drones
        "type": ObjectType.station,
        "coords": percent_world(0.96, 0.95),

        "primary_import": MaterialType.weaponry,
        "primary_consumption_qty": 1,
        "primary_max": 20,

        "secondary_import": MaterialType.null,
        "secondary_consumption_qty": 1,
        "secondary_max": 10,

        "production_material": MaterialType.drones,
        "production_frequency": 1,
        "production_qty": 1,
        "production_max": 100,

        "cargo": {

        }
    },
    {
        #s7 Steel
        "type": ObjectType.station,
        "coords": percent_world(0.92, 0.03),

        "primary_import": MaterialType.iron,
        "primary_consumption_qty": 1,
        "primary_max": 20,

        "secondary_import": MaterialType.drones,
        "secondary_consumption_qty": 1,
        "secondary_max": 10,

        "production_material": MaterialType.steel,
        "production_frequency": 1,
        "production_qty": 1,
        "production_max": 100,

        "cargo": {

        }
    },
    {
        # black market 2
        "type": ObjectType.black_market_station,
        "coords": percent_world(0.1, 0.8)
    },
    {
        # black market 1
        "type": ObjectType.black_market_station,
        "coords": percent_world(0.88, 0.25)
    },
    {
        "type": ObjectType.secure_station,
        "coords": percent_world(0.5, 0.5)
    }
]

ASTEROID_FIELD_DEFINITIONS = [
    {
        "type": ObjectType.goethite_field,
        "coords": percent_world(0.05, 0.05)
    },
    {
        "type": ObjectType.gold_field,
        "coords": percent_world(0.85, 0.85)
    },
    {
        "type": ObjectType.cuprite_field,
        "coords": percent_world(0.5, 0.85)
    }
]
