import math

from game.config import *
from game.common.enums import *
from game.utils.projection import *

STATION_DEFINITIONS = [
    {
        #s6 Copper
        "type": ObjectType.station,
        "name": "Copper Station",
        "position": percent_world(0.05, 0.9),

        "primary_import": MaterialType.cuprite,
        "primary_consumption_qty": 3,
        "primary_max": 75,

        "secondary_import": MaterialType.drones,
        "secondary_consumption_qty": 1,
        "secondary_max": 5,

        "production_material": MaterialType.copper,
        "production_frequency": 1,
        "production_qty": 2,
        "production_max": 150,

        "sell_price": 73,
        "primary_buy_price": 53,
        "secondary_buy_price": 59,

        "base_sell_price": 67,
        "base_primary_buy_price": 15,
        "base_secondary_buy_price": 45,


        "cargo": {
            MaterialType.cuprite: 20,
            MaterialType.drones: 10
        }
    },
    {
        #s4 Pylons
        "type": ObjectType.station,
        "name": "Pylon Station",
        "position": percent_world(0.025, 0.6),

        "primary_import": MaterialType.circuitry,
        "primary_consumption_qty": 1,
        "primary_max": 35,

        "secondary_import": MaterialType.null,
        "secondary_consumption_qty": 0,
        "secondary_max": 0,

        "production_material": MaterialType.pylons,
        "production_frequency": 10,
        "production_qty": 5,
        "production_max": 45,

        "sell_price": 350,
        "primary_buy_price": 406,
        "secondary_buy_price": 0,

        "base_sell_price": 423,
        "base_primary_buy_price": 367,
        "base_secondary_buy_price": 0,

        "cargo": {
            MaterialType.circuitry: 100,
            MaterialType.pylons: 10
        }
    },
    {
        #s9 Weaponry
        "type": ObjectType.station,
        "name": "Weaponry Station",
        "position": percent_world(0.15, 0.58),

        "primary_import": MaterialType.computers,
        "primary_consumption_qty": 4,
        "primary_max": 5,

        "secondary_import": MaterialType.null,
        "secondary_consumption_qty": 0,
        "secondary_max": 0,

        "production_material": MaterialType.weaponry,
        "production_frequency": 3,
        "production_qty": 1,
        "production_max": 55,

        "sell_price": 590,
        "primary_buy_price": 540,
        "secondary_buy_price": 100,

        "base_sell_price": 540,
        "base_primary_buy_price": 590,
        "base_secondary_buy_price": 0,

        "cargo": {
            MaterialType.computers: 50,
            MaterialType.weaponry: 0
        }
    },
    {
        #s5 Machinery
        "type": ObjectType.station,
        "name": "Machinery Station",
        "position": percent_world(0.085, 0.40),

        "primary_import": MaterialType.steel,
        "primary_consumption_qty": 8,
        "primary_max": 120,

        "secondary_import": MaterialType.pylons,
        "secondary_consumption_qty": 1,
        "secondary_max": 10,

        "production_material": MaterialType.machinery,
        "production_frequency": 2,
        "production_qty": 3,
        "production_max": 100,

        "sell_price": 45,
        "primary_buy_price": 20,
        "secondary_buy_price": 370,

        "base_sell_price": 45,
        "base_primary_buy_price": 20,
        "base_secondary_buy_price": 370,

        "cargo": {
            MaterialType.steel: 56,
            MaterialType.pylons: 100
        }
    },
    {
        #s0 Wire
        "type": ObjectType.station,
        "name": "Wire Station",
        "position": percent_world(0.4, 0.10),

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

        "sell_price": 100,
        "primary_buy_price": 100,
        "secondary_buy_price": 100,

        "base_sell_price": 100,
        "base_primary_buy_price": 100,
        "base_secondary_buy_price": 100,

        "cargo": {
            MaterialType.copper: 23,
        }
    },
    {
        #s8 Iron
        "type": ObjectType.station,
        "name": "Iron Station",
        "position": percent_world(0.6, 0.80),

        "primary_import": MaterialType.goethite,
        "primary_consumption_qty": 1,
        "primary_max": 175,

        "secondary_import": MaterialType.machinery,
        "secondary_consumption_qty": 1,
        "secondary_max": 14,

        "production_material": MaterialType.iron,
        "production_frequency": 1,
        "production_qty": 6,
        "production_max": 150,

        "sell_price": 25,
        "primary_buy_price": 13,
        "secondary_buy_price": 30,

        "base_sell_price": 25,
        "base_primary_buy_price": 13,
        "base_secondary_buy_price": 30,

        "cargo": {
            MaterialType.goethite: 75,
        }
    },
    {
        #s1 Computers
        "type": ObjectType.station,
        "name": "Computers Station",
        "position": percent_world(0.63, 0.08),

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

        "sell_price": 100,
        "primary_buy_price": 100,
        "secondary_buy_price": 100,

        "base_sell_price": 100,
        "base_primary_buy_price": 100,
        "base_secondary_buy_price": 100,

        "cargo": {
            MaterialType.circuitry: 75,
        }
    },
    {
        #s2 Circuitry
        "type": ObjectType.station,
        "name": "Circuitry Station",
        "position": percent_world(0.90, 0.38),

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

        "sell_price": 100,
        "primary_buy_price": 100,
        "secondary_buy_price": 100,

        "base_sell_price": 100,
        "base_primary_buy_price": 100,
        "base_secondary_buy_price": 100,

        "cargo": {
            MaterialType.gold: 75,
            MaterialType.wire: 75,
        }
    },
    {
        #s3 Drones
        "type": ObjectType.station,
        "name": "Drones Station",
        "position": percent_world(0.96, 0.95),

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

        "sell_price": 100,
        "primary_buy_price": 100,
        "secondary_buy_price": 100,

        "base_sell_price": 100,
        "base_primary_buy_price": 100,
        "base_secondary_buy_price": 100,

        "cargo": {
            MaterialType.weaponry: 15,
        }
    },
    {
        #s7 Steel
        "type": ObjectType.station,
        "name": "Steel Station",
        "position": percent_world(0.92, 0.03),

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

        "sell_price": 100,
        "primary_buy_price": 100,
        "secondary_buy_price": 100,

        "base_sell_price": 100,
        "base_primary_buy_price": 100,
        "base_secondary_buy_price": 100,

        "cargo": {
            MaterialType.iron: 100,
            MaterialType.drones: 5,
        }
    },
    {
        # black market 2
        "type": ObjectType.black_market_station,
        "name": "Black Market 2",
        "position": percent_world(0.1, 0.8)
    },
    {
        # black market 1
        "type": ObjectType.black_market_station,
        "name": "Black Market 1",
        "position": percent_world(0.88, 0.25)
    },
    {
        "type": ObjectType.secure_station,
        "name": "Station Authority",
        "position": percent_world(0.5, 0.5)
    }
]

ASTEROID_FIELD_DEFINITIONS = [
    {
        "type": ObjectType.goethite_field,
        "name": "Geothite Asteroid Field",
        "position": percent_world(0.05, 0.05)
    },
    {
        "type": ObjectType.gold_field,
        "name": "Gold Asteroid Field",
        "position": percent_world(0.85, 0.85)
    },
    {
        "type": ObjectType.cuprite_field,
        "name": "Cuprite Asteroid Field",
        "position": percent_world(0.5, 0.85)
    }
]
