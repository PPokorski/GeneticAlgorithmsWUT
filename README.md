# GeneticAlgorithmsWUT

## About ##
This project is made for the subject "Evolutionary methods and machine learning". The goal is to find (using a genetic algorthm)
the optimal placement of cameras in the given environement. The floors are generated randomly using an algorithm find [here](http://www.roguebasin.com/index.php?title=A_Simple_Dungeon_Generator_for_Python_2_or_3).

## Assumptions ##
* The world representation is a discrete grid map, each cell being either STONE, WALL, FLOOR, SEEN (as in the [tiles.py](https://github.com/PPokorski/GeneticAlgorithmsWUT/blob/add_world_model/tiles.py)).
* Camera model includes the position and orientation of the camera in the map, its angle of view, range of view (expressed in the number of cells) and angular resolution.
* Visibility model of the camera is simply a ray-tracing algorithm from the camera position to the end of the ray (it very much resembles the [2D LiDAR model](https://i.stack.imgur.com/NglQd.png). Currently there are two algorithms available for ray-tracing: [Bresenham](https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm) and [Xiaolin's Wu](https://en.wikipedia.org/wiki/Xiaolin_Wu%27s_line_algorithm). The former is faster but thicker, whereas the latter slower but denser (doesn't leave the gaps far from camera).
* Starting positions for the cameras will be the corners of the floor, inspider by [Art gallery problem](https://en.wikipedia.org/wiki/Art_gallery_problem).

## Prerequisites ##
* Python 2.7
* [PIL Image Library](https://pillow.readthedocs.io/en/5.0.0/)
* [Pickle Serialization Library](https://docs.python.org/2/library/pickle.html)

## Usage ##
To use the scripts, firstly you need to generate a floor image and a corner binary file (for cameras' starting positions).
```python
generator = FloorGenerator()
generator.gen_level()
floor_loader.save_map('/path/to/image', floor_loader.grid_to_image(generator.level), '/path/to/corners', generator.get_corners())
```
Where ```'/path/to/image'``` is your desired location of the floor image (image format is deduced based on the extension passed to file name) and ```'/path/to/corners'``` is your desired location of the corners file. This is a binary file serialized with [Pickle](https://docs.python.org/2/library/pickle.html).
To use the before saved floor you need to load it from a file:
```python
[grid, corners] = floor_loader.load_map('/path/to/image', '/path/to/binary/corners')
```
Later you need to initialize a FloorPlan object with both a grid and corners:
```python
# Initializing from the file
[grid, corners] = floor_loader.load_map('/path/to/image', '/path/to/binary/corners')
plan = FloorPlan(grid, corners) # 

# Initializing from the generator
generator = FloorGenerator()
generator.gen_level()
plan = FloorPlan(generator.level, generator.get_corners())
```
Initializing the ray-tracer model is also required:
```python
tracer = ray_trace.RayTrace(tiles.occupied_tiles, tiles.Tiles.SEEN, False)
```
First argument contains an array of values for occupied tiles (when tracer stumbles upon them it stops tracing) and a value with which it marks traced tiles. Last argument specifies whether ray-tracing should be dense or not (e.g. Bresenham or Xiaolin's Wu algorithm).
At this point you might initialize the cameras inside FloorPlan class with whatever values you like (FloorPlan contains a list of cameras):
```python
plan.cameras = [camera.Camera([50, 50], 0.0, 3*3.14/2.0, range_of_view=100.0)]
plan.mark_all_cameras(tracer)
```
The method ```FloorPlan::mark_all_cameras(RayTrace object)``` marks all the cells in the grid that are visible to the camera, appropriately filling the ```FloorPlan::visibility_map``` structure.
After marking you may check what part of the floor is covered by using:
```python
plan.get_coverage()
```
which returns a floating-point number in the range [0; 1.0] specyfing what part of the floor is seen by the cameras.
If you wish you may visualize the map (visibility map or the pure one) with:
```python
img = image_from_grid(plan.visibility_map)
drawer = ImageDraw.Draw(img)
img.show()
```
ImageDraw class is documented at [PIL](https://pillow.readthedocs.io/en/5.0.0/). 
