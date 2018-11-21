import platform
## Config

NPCS_TO_GENERATE = 20

NUM_POLICE = 8

WORLD_BOUNDS = (1000, 700)

DISPLAY_SIZE = (1280, 720)

SECURE_ZONE_RADIUS = 200


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
