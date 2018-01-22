# ! /usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from scipy.spatial import Delaunay
import triangle


def triangulate_points(corners, mask = None):
    points = np.array(corners)

    triangulate = Delaunay(points)
    #triangulate2 = tri.Triangulation(corners[:, 0], corners[:, 2], triangles = None, mask = None)

    #plt.triplot(points[:, 0], points[:, 1], triangulate2)
    #plt.plot(points[:, 0], points[:, 1], 'x')

    #print(tri)
    return triangulate


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
