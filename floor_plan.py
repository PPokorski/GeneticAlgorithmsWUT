# ! /usr/bin/env python
# coding: utf-8

import copy

import tiles
import camera
import ray_trace
import floor_loader


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

    [grid, corners] = floor_loader.load_map('/path/to/image', '/path/to/binary/corners')
    plan = FloorPlan(grid, corners)

    # tracer = ray_trace.RayTrace(tiles.occupied_tiles, tiles.Tiles.SEEN, False)

    # plan.cameras = [camera.Camera([50, 50], 0.0, 3*3.14/2.0, range_of_view=100.0)]

    # plan.mark_all_cameras(tracer)

    # img = image_from_grid(plan.visibility_map)
    # drawer = ImageDraw.Draw(img)

    # for corner in plan.corners:
        # drawer.point(corner, (255, 0, 0))

    # drawer.point([50, 50], (255, 0, 0))
    # drawer.point([200, 200], (255, 0, 0))
    # img.show()