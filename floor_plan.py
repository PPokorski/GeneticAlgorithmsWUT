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
from scipy.spatial import distance as dist
import numpy as np

def order_points(pts):
    # sort the points based on their x-coordinates
    xSorted = pts[np.argsort(pts[:, 0]), :]

    # grab the left-most and right-most points from the sorted
    # x-roodinate points
    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]

    # now, sort the left-most coordinates according to their
    # y-coordinates so we can grab the top-left and bottom-left
    # points, respectively
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost

    # now that we have the top-left coordinate, use it as an
    # anchor to calculate the Euclidean distance between the
    # top-left and right-most points; by the Pythagorean
    # theorem, the point with the largest distance will be
    # our bottom-right point
    D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
    (br, tr) = rightMost[np.argsort(D)[::-1], :]

    # return the coordinates in top-left, top-right,
    # bottom-right, and bottom-left order
    return np.array([tl, tr, br, bl], dtype="float32")


import math
origin = [19, 17]
refvec = [19, 17]

def clockwiseangle_and_distance(point):
    # Vector between point and the origin: v = p - o
    vector = [point[0] - origin[0], point[1] - origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0] / lenvector, vector[1] / lenvector]
    dotprod = normalized[0] * refvec[0] + normalized[1] * refvec[1]  # x1*x2 + y1*y2
    diffprod = refvec[1] * normalized[0] - refvec[0] * normalized[1]  # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    # Negative angles represent counter-clockwise angles so we need to subtract them
    # from 2*pi (360 degrees)
    if angle < 0:
        return 2 * math.pi + angle, lenvector
    # I return first the angle because that's the primary sorting criterium
    # but if two vectors have the same angle then the shorter distance should come first.
    return angle, lenvector

if __name__ == '__main__':
    pass

    [grid, corners] = floor_loader.load_map('C:/Users/Kacper/Desktop/github/GeneticAlgorithmsWUT/pictures/mapa.png',
                                            'C:/Users/Kacper/Desktop/github/GeneticAlgorithmsWUT/pictures/mapa.txt')
    plan = FloorPlan(grid, corners)
    #camera_instance = camera.Camera([0, 0])
    print(corners)
    points2 = np.array(corners)

    #clock = order_points(points2)
    sort = sorted(points2, key=clockwiseangle_and_distance)
    #print(sort)
    sorted_points = np.array(sort)
    print(sorted_points)

    file = open("C:/Users/Kacper/Desktop/github/GeneticAlgorithmsWUT/pictures/coords.txt", 'w')
    for vertice in sorted_points:
        file.write("%d %d\r\n" % (vertice[0], vertice[1]))
    file.close()


    tracer = ray_trace.RayTrace(tiles.occupied_tiles, tiles.Tiles.SEEN, False)
    print(tracer)
    print(len(grid))
    print(len(corners))
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

    drawer.point([50, 50], (255, 0, 0))

    img.show()

    #import numpy as np
    import matplotlib.pyplot as plt

    points = np.array(corners)

    #plt.figure(1)
    #plt.triplot(points[:, 0], points[:, 1], tri_museum.simplices.copy())
    #plt.triplot(points[:, 0], points[:, 1], tri_room2.simplices.copy())
    #plt.plot(points[:, 0], points[:, 1], 'o')
    #for j, p in enumerate(points):
    #    plt.text(p[0]-0.03, p[1]+0.03, j, ha='right')
    #for j, s in enumerate(tri_museum.simplices):
    #    p = points[s].mean(axis=0)
    #    plt.text(p[0], p[1], '#%d' % j, ha='center')


    import matplotlib.tri as tri
    triang = tri.Triangulation(sorted_points[:, 0], sorted_points[:, 1])
    #mask = np.random.randint(2, size=129)
    mask = [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0
    ]
    print(mask)
    #print(triang.triangles)
    #triang.set_mask(mask)
    plt.figure(2)
    test = plt.triplot(triang, 'bo-', lw=1)

