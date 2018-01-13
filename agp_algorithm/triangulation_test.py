# ! /usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import triangle


def triangulate_points(corners):
    points = np.array(corners)
    tri = triangle.delaunay(points)
    segments = triangle.convex_hull(points)
    plt.triplot(points[:, 0], points[:, 1], tri)
    plt.plot(points[:, 0], points[:, 1], 'x')
    #plt.plot(segments)
    #print(tri)
    return plt, segments


