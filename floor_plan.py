# ! /usr/bin/env python
# coding: utf-8

import copy
import PIL
import tiles
import camera
import ray_trace
import floor_loader

import sys
sys.path.append('cd agp_algorithm')

from agp_algorithm import triangulation_test

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


if __name__ == '__main__':
    pass

    [grid, corners] = floor_loader.load_map('C:/Users/Kacper/Desktop/github/GeneticAlgorithmsWUT/pictures/mapa.png',
                                            'C:/Users/Kacper/Desktop/github/GeneticAlgorithmsWUT/pictures/mapa.txt')
    plan = FloorPlan(grid, corners)
    #camera_instance = camera.Camera([0, 0])
    print(corners)

    tracer = ray_trace.RayTrace(tiles.occupied_tiles, tiles.Tiles.SEEN, False)

    k = 0

    for i in plan.corners:
        plan.cameras.append(camera.Camera(corners[k], 0.8, 1*3.14/2.0, range_of_view=20.0))
        k += 1

    #plan.cameras = [camera.Camera(corners[0], 0.8, 1*3.14/2.0, range_of_view=20.0)
    #                camera.Camera(corners[20], 1.2, 1 * 3.14 / 2.0, range_of_view=20.0)]

    plan.mark_all_cameras(tracer)

    img = floor_loader.grid_to_image(plan.visibility_map)
    drawer = PIL.ImageDraw.Draw(img)

    for corner in plan.corners:
        drawer.point(corner, (255, 0, 0))

   # drawer.point([50, 50], (255, 0, 0))

    tri_cords, segments = triangulation_test.triangulate_points(corners)
    img.show()

    tri_cords.show()