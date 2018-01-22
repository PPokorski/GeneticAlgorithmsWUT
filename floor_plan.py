# ! /usr/bin/env python
# coding: utf-8

import copy
import PIL
import tiles
import camera
import ray_trace
import floor_loader

import PIL.Image

import sys
sys.path.append('cd agp_algorithm')

from agp_algorithm import triangulation_test
from agp_algorithm import testing

class FloorPlan:
    def __init__(self, rooms_map, corners):

        self.map = copy.deepcopy(rooms_map)
        self.visibility_map = copy.deepcopy(rooms_map)

        self.corners = copy.deepcopy(corners)

        self.number_of_tiles = self.get_elements_count(self.map, tiles.Tiles.FLOOR)

        self.cameras = []

    def is_position_free(self, x, y):
        return not self.map[x][y] in tiles.occupied_tiles

    def mark_all_cameras(self, tracer):
        for cam in self.cameras:
            self.mark_camera(cam, tracer)

    def mark_camera(self, cam, tracer):
        arc = cam.get_discrete_range_of_view(cam.angular_resolution)

        for arc_point in arc:
            tracer.ray_trace(self.visibility_map, cam.position, arc_point)

    def get_elements_count(self, check_map, element):
        number = 0
        for row in check_map:
            number += row.count(element)

        return number

    def get_coverage(self):

        number_of_seen_tiles = self.get_elements_count(self.visibility_map, tiles.Tiles.SEEN)

        return number_of_seen_tiles / self.number_of_tiles


# import the necessary packages
import numpy as np


if __name__ == '__main__':
    pass

    [grid, corners] = floor_loader.load_map('./pictures/mapa.png',
                                            './pictures/mapa.txt')

    plan = FloorPlan(grid, corners)
    #camera_instance = camera.Camera([0, 0])

    points2 = np.array(corners)

    clock = triangulation_test.clockwiseangle_and_distance
    sort = sorted(points2, key=clock)
    #print(sort)
    sorted_points = np.array(sort)
    print(sorted_points)

    file = open("./pictures/coords.txt", 'w')
    for vertice in sorted_points:
        file.write("%d %d\n" % (vertice[0], vertice[1]))
    file.close()


    tracer = ray_trace.RayTrace(tiles.occupied_tiles, tiles.Tiles.SEEN, False)
    print(tracer)
    print(len(grid))
    print(len(corners))
    k = 0

    filename_guards = "./agp_algorithm/inputs/guards.poly"
    #file = open(filename_guards, 'r')
    points = []
    with open(filename_guards, "r") as hfile:
        hfile.readline()
        i = 0
        for line in hfile:
            x, y = line.split()
            points.append([int(x), int(y)])
    file.close()

    alpha_array = [0.021, 0.022, 0.023, 0.024, 0.025, 0.026, 0.027, 0.028, 0.029, 0.03]
    alpha = alpha_array[1]

    get_points = np.array(points)

    concave_hull,\
    edge_points,\
    edges,\
    triang = testing.alpha_shape(points2, alpha=alpha)


    for i in points:
        plan.cameras.append(camera.Camera(points[k], 0.8, 1*3.14/2.0, range_of_view=20.0))
        k += 1

    plan.mark_all_cameras(tracer)

    img = floor_loader.grid_to_image(plan.visibility_map)
    drawer = PIL.ImageDraw.Draw(img)

    for corner in plan.corners:
        drawer.point(corner, (255, 0, 0))
    #for line in edge_points:
    #    drawer.line(line, fill=255)

    img.show()


###########################################################
###########################################################

    def place_camera_new_position(position):
        _angle   = position.angle
        _range   = position.range
        _corners = position.corners

        plan.cameras.append(camera.Camera(corners[k],
                                          0.8,
                                          1 * 3.14 / 2.0,
                                          range_of_view=20.0)
                            )


    ################### GENERIC ALGORITHM ####################
    dest_area = 0.9 # percentage of camera area
                    # which we want to get

    total_area = 0
    new_area = 0
    old_area = 0

    #while total_area >= dest_area:
    #    place_camera_new_position(&position)
    #    new_area = get_camera_area();
    #    if new_area < old_area:
    #        process_mutation(&position)
    #    old_area = new_area



