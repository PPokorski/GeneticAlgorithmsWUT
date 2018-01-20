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


