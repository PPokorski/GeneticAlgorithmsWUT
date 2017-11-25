import enum


# The enum holds types of the tiles
class Tiles(enum.Enum):
    STONE = 0
    WALL = 1
    FLOOR = 2
    SEEN = 3

# Which tiles are considered occupied. The rest is considered to be free
occupied_tiles = [Tiles.STONE, Tiles.WALL]