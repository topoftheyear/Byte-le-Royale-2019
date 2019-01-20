import platform
## Config

NPCS_TO_GENERATE = 40

NUM_POLICE = 8

WORLD_BOUNDS = (1000, 700)

DISPLAY_SIZE = (1280, 720)

SECURE_ZONE_RADIUS = 200

ENFORCER_THRESHOLD = 20
ENFORCER_WAVE_TIMER = 100  # how often to spawn the next wave of enforcers


# High Performance Render Mode
if platform.system() == 'Linux':
    VIS_INTERMEDIATE_FRAMES = 10
    FPS = 60
    LOW_FPS = 30
else:
    VIS_INTERMEDIATE_FRAMES = 4
    FPS = 120
    LOW_FPS = 60

# Low Performance Render Mode
#VIS_INTERMEDIATE_FRAMES = -1
#FPS = 10

RESPAWN_TIME = 10

SHIP_SALVAGE_CONSTANT = 500 # the value of a ship kill

ILLEGAL_SCRAP_VALUE = 4.5

# Bounty related items
BOUNTY_DECAY_RATE = 0.002
BOUNTY_PAYOFF_RATIO = 1
ILLEGAL_SCRAP_NOTORIETY_RATIO = 1
