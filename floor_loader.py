import pickle

import PIL.Image
import PIL.ImageDraw

import tiles


# Dictionary for translating tile types to colours
tile_to_colour = {tiles.Tiles.STONE: (0, 0, 0),
                  tiles.Tiles.FLOOR: (128, 128, 128),
                  tiles.Tiles.WALL: (255, 255, 255),
                  tiles.Tiles.SEEN: (0, 255, 0)}

# Dictionary for translating colours to tile types
colour_to_tiles = {(0, 0, 0): tiles.Tiles.STONE,
                   (128, 128, 128): tiles.Tiles.FLOOR,
                   (255, 255, 255): tiles.Tiles.WALL,
                   (0, 255, 0): tiles.Tiles.SEEN}


# Given the grid and list of corners save the map as an image and corners as binary file
# The map's extension will be deduced by image_full_path extension
# CAUTION! DON'T USE FORMATS WITH LOSSY COMPRESSION
def save_map(image_full_path, grid, corners_full_path, corners):

    save_image(image_full_path, grid_to_image(grid))
    save_corners(corners_full_path, corners)


# Load the map. Returns the grid and corners' list
def load_map(image_full_path, corners_full_path):

    grid = image_to_grid(load_image(image_full_path))
    corners = load_corners(corners_full_path)

    return [grid, corners]


# Convert an image to a grid
def image_to_grid(image):

    grid = [[0 for i in range(image.height)] for j in range(image.width)]
    for i in range(image.width):
        for j in range(image.height):
            grid[i][j] = colour_to_tiles[image.getpixel((i, j))]

    return grid


# Convert a grid to an image
def grid_to_image(grid):

    image = PIL.Image.new('RGB', (len(grid), len(grid[0])))
    draw = PIL.ImageDraw.Draw(image)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            draw.point([i, j], tile_to_colour[grid[i][j]])

    return image


# Save the corners as a binary file
def save_corners(full_path, corners):
    with open(full_path, 'wb') as fp:
        pickle.dump(corners, fp)


# Load the corners
def load_corners(full_path):
    with open(full_path, 'rb') as fp:
        corners = pickle.load(fp)

    return corners


# Save image to the disk
def save_image(full_path, image):
    image.save(full_path)


# Load image from the disk
def load_image(full_path):
    image = PIL.Image.open(full_path)

    return image

