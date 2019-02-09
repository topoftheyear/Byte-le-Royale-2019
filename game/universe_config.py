import math

from game.config import *
from game.common.enums import *
from game.utils.projection import *

frequency_addition = 10
STATION_DEFINITIONS = [
    {
        #s6 Copper
        "type": ObjectType.station,
        "name": "Copper Station",
        "position": percent_world(0.05, 0.9),

        "primary_import": MaterialType.cuprite,
        "primary_consumption_qty": 80,
        "primary_max": 2000,

        "secondary_import": MaterialType.drones,
        "secondary_consumption_qty": 10,
        "secondary_max": 1000,

        "production_material": MaterialType.copper,
        "production_frequency": frequency_addition + 20,
        "production_qty": 35,
        "production_max": 1000,

        "sell_price": 16,
        "primary_buy_price": 7,
        "secondary_buy_price": 56,

        "base_sell_price": 16,
        "base_primary_buy_price": 7,
        "base_secondary_buy_price": 56,


        "cargo": {
            MaterialType.cuprite: 500,
            MaterialType.drones: 10,
            MaterialType.copper: 0
        }
    },
    {
        #s4 Pylons
        "type": ObjectType.station,
        "name": "Pylon Station",
        "position": percent_world(0.025, 0.6),

        "primary_import": MaterialType.circuitry,
        "primary_consumption_qty": 20,
        "primary_max": 300,

        "secondary_import": MaterialType.null,
        "secondary_consumption_qty": 0,
        "secondary_max": 0,

        "production_material": MaterialType.pylons,
        "production_frequency": frequency_addition + 27,
        "production_qty": 50,
        "production_max": 500,

        "sell_price": 15,
        "primary_buy_price": 25,
        "secondary_buy_price": 0,

        "base_sell_price": 15,
        "base_primary_buy_price": 25,
        "base_secondary_buy_price": 0,

        "cargo": {
            MaterialType.circuitry: 80,
            MaterialType.pylons: 10,
        }
    },
    {
        #s9 Weaponry
        "type": ObjectType.station,
        "name": "Weaponry Station",
        "position": percent_world(0.15, 0.58),

        "primary_import": MaterialType.computers,
        "primary_consumption_qty": 20,
        "primary_max": 300,

        "secondary_import": MaterialType.null,
        "secondary_consumption_qty": 0,
        "secondary_max": 0,

        "production_material": MaterialType.weaponry,
        "production_frequency": frequency_addition + 15,
        "production_qty": 20,
        "production_max": 260,

        "sell_price": 42,
        "primary_buy_price": 30,
        "secondary_buy_price": 0,

        "base_sell_price": 42,
        "base_primary_buy_price": 30,
        "base_secondary_buy_price": 0,

        "cargo": {
            MaterialType.computers: 50,
            MaterialType.weaponry: 10
        }
    },
    {
        #s5 Machinery
        "type": ObjectType.station,
        "name": "Machinery Station",
        "position": percent_world(0.085, 0.40),

        "primary_import": MaterialType.steel,
        "primary_consumption_qty": 40,
        "primary_max": 500,

        "secondary_import": MaterialType.pylons,
        "secondary_consumption_qty": 30,
        "secondary_max": 1500,

        "production_material": MaterialType.machinery,
        "production_frequency": frequency_addition + 23,
        "production_qty": 40,
        "production_max": 400,

        "sell_price": 20,
        "primary_buy_price": 24,
        "secondary_buy_price": 20,

        "base_sell_price": 20,
        "base_primary_buy_price": 24,
        "base_secondary_buy_price": 20,

        "cargo": {
            MaterialType.steel: 56,
            MaterialType.pylons: 70,
            MaterialType.machinery: 0
        }
    },
    {
        #s0 Wire
        "type": ObjectType.station,
        "name": "Wire Station",
        "position": percent_world(0.4, 0.10),

        "primary_import": MaterialType.copper,
        "primary_consumption_qty": 42,
        "primary_max": 800,

        "secondary_import": MaterialType.null,
        "secondary_consumption_qty": 0,
        "secondary_max": 0,

        "production_material": MaterialType.wire,
        "production_frequency": frequency_addition + 18,
        "production_qty": 38,
        "production_max": 900,

        "sell_price": 10,
        "primary_buy_price": 19,
        "secondary_buy_price": 10,

        "base_sell_price": 10,
        "base_primary_buy_price": 19,
        "base_secondary_buy_price": 10,

        "cargo": {
            MaterialType.copper: 50,
            MaterialType.wire: 0
        }
    },
    {
        #s8 Iron
        "type": ObjectType.station,
        "name": "Iron Station",
        "position": percent_world(0.6, 0.80),

        "primary_import": MaterialType.goethite,
        "primary_consumption_qty": 55,
        "primary_max": 1600,

        "secondary_import": MaterialType.machinery,
        "secondary_consumption_qty": 10,
        "secondary_max": 1200,

        "production_material": MaterialType.iron,
        "production_frequency": frequency_addition + 22,
        "production_qty": 40,
        "production_max": 800,

        "sell_price": 12,
        "primary_buy_price": 5,
        "secondary_buy_price": 21,

        "base_sell_price": 12,
        "base_primary_buy_price": 5,
        "base_secondary_buy_price": 21,

        "cargo": {
            MaterialType.goethite: 700,
            MaterialType.machinery: 0,
            MaterialType.iron: 0
        }
    },
    {
        #s1 Computers
        "type": ObjectType.station,
        "name": "Computers Station",
        "position": percent_world(0.63, 0.08),

        "primary_import": MaterialType.circuitry,
        "primary_consumption_qty": 30,
        "primary_max": 700,

        "secondary_import": MaterialType.null,
        "secondary_consumption_qty": 0,
        "secondary_max": 0,

        "production_material": MaterialType.computers,
        "production_frequency": frequency_addition + 30,
        "production_qty": 50,
        "production_max": 400,

        "sell_price": 26,
        "primary_buy_price": 31,
        "secondary_buy_price": 10,

        "base_sell_price": 26,
        "base_primary_buy_price": 31,
        "base_secondary_buy_price": 10,

        "cargo": {
            MaterialType.circuitry: 75,
            MaterialType.computers: 20
        }
    },
    {
        #s2 Circuitry
        "type": ObjectType.station,
        "name": "Circuitry Station",
        "position": percent_world(0.90, 0.38),

        "primary_import": MaterialType.gold,
        "primary_consumption_qty": 70,
        "primary_max": 1500,

        "secondary_import": MaterialType.wire,
        "secondary_consumption_qty": 30,
        "secondary_max": 1420,

        "production_material": MaterialType.circuitry,
        "production_frequency": frequency_addition + 30,
        "production_qty": 30,
        "production_max": 450,

        "sell_price": 23,
        "primary_buy_price": 10,
        "secondary_buy_price": 12,

        "base_sell_price": 23,
        "base_primary_buy_price": 10,
        "base_secondary_buy_price": 12,

        "cargo": {
            MaterialType.gold: 350,
            MaterialType.wire: 75,
            MaterialType.circuitry: 0
        }
    },
    {
        #s3 Drones
        "type": ObjectType.station,
        "name": "Drones Station",
        "position": percent_world(0.96, 0.95),

        "primary_import": MaterialType.weaponry,
        "primary_consumption_qty": 10,
        "primary_max": 200,

        "secondary_import": MaterialType.null,
        "secondary_consumption_qty": 0,
        "secondary_max": 0,

        "production_material": MaterialType.drones,
        "production_frequency": frequency_addition + 23,
        "production_qty": 30,
        "production_max": 300,

        "sell_price": 49,
        "primary_buy_price": 45,
        "secondary_buy_price": 10,

        "base_sell_price": 49,
        "base_primary_buy_price": 45,
        "base_secondary_buy_price": 10,

        "cargo": {
            MaterialType.weaponry: 30,
            MaterialType.drones: 0
        }
    },
    {
        #s7 Steel
        "type": ObjectType.station,
        "name": "Steel Station",
        "position": percent_world(0.92, 0.03),

        "primary_import": MaterialType.iron,
        "primary_consumption_qty": 50,
        "primary_max": 900,

        "secondary_import": MaterialType.drones,
        "secondary_consumption_qty": 10,
        "secondary_max": 1100,

        "production_material": MaterialType.steel,
        "production_frequency": frequency_addition + 21,
        "production_qty": 70,
        "production_max": 630,

        "sell_price": 18,
        "primary_buy_price": 15,
        "secondary_buy_price": 54,

        "base_sell_price": 18,
        "base_primary_buy_price": 15,
        "base_secondary_buy_price": 54,

        "cargo": {
            MaterialType.iron: 100,
            MaterialType.drones: 5,
            MaterialType.steel: 0
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
