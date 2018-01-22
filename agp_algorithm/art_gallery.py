import sys
from point import Point
from triangulation import Triangulation
from coloring import Coloring
from agp_algorithm import testing
import threading
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri


class ArtGallery(object):
    def __init__(self, point):

        self._point = Point(point.id, point.x, point.y)
        self._points = [point]
        self._polygon = [(point.x, point.y)]
        self._triangulation = Triangulation(self._points)
        self._color = Coloring(self._points, self._triangulation)
        self.lock = threading.RLock()
        self.version = 0

    @staticmethod
    def load(file_name):
        points = []
        with open(file_name, "r") as hfile:
            hfile.readline()
            i = 0
            for line in hfile:
                x, y = line.split()
                point = Point(i, int(x), int(y))
                i += 1
                points.append(point)
        return points

    def _update(self):
        self._points.sort()
        self._polygon = []
        for p in self._points:
            self._polygon.append((p.x, p.y))

    def get_polygon(self):
        with self.lock:
            return self._polygon

    def get_process_point(self):
        with self.lock:
            return self._point

    def get_points(self):
        with self.lock:
            return self._points

    def get_diagonals(self):
        with self.lock:
            return self._triangulation.get_diagonals()

    def get_min_color(self):
        with self.lock:
            return self._color.get_min_color()

    def is_guard(self, point):
        with self.lock:
            return point.color == self._color.get_min_color()

    def include(self, point):
        """ Add a new point to the art gallery """
        with self.lock:
            self._points.append(Point(point.id, point.x, point.y))
            self._update()
            triangulated = self._triangulation.process()
            if (triangulated):
               # coloring
                self._color.process()
            self.version += 1

    def triangulate_all(self):

        with self.lock:
            triangulated = self._triangulation.process()
            if (triangulated):
               # coloring
                self._color.process()


import math
origin = [100, 17]
refvec = [100, 17]

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


def sorting_algorithm(points):

    x = points[:, 0]
    y = points[:, 1]
    cx = np.mean(x)
    cy = np.mean(y)
    angle = np.arctan2(y - cy, x - cx)
    order = angle.ravel().argsort()

    x = x[order]
    y = y[order]

    return np.vstack([x, y])

if __name__ == '__main__':
    pass

    # create file paths for testing
    filename = "./inputs/temp.poly"
    filename2 = "./inputs/coords_sorted.poly"
    filename3 = "./inputs/enterprise.poly"
    filename4 = "./inputs/museum.poly"
    filename_guards = "./inputs/guards.poly"

    # read coordinates from first file
    file = open(filename, 'r')
    points = []
    with open(filename, "r") as hfile:
        i = 0
        for line in hfile:
            x, y = line.split()
            points.append([int(x), int(y)])
    file.close()

    # sort your points clockwise
    points_not_sorted = np.array(points)
    temp = sorting_algorithm(points_not_sorted)

    # create coordinates tuple
    new_coords = []
    i = 0
    for t in temp[0]:
        new_coords.append([temp[0][i], temp[1][i]])
        i += 1

    # array for alpha shape values
    alpha_array = [0.021, 0.022, 0.023, 0.024, 0.025, 0.026, 0.027, 0.028, 0.029, 0.03]
    alpha = alpha_array[1]

    # get your alpha shape from given points
    concave_hull,\
    edge_points,\
    edges,\
    triang = testing.alpha_shape(points_not_sorted, alpha=alpha)

    _edge_points = []
    for edge in edge_points:
        if not isinstance(edge, np.ma.MaskedArray):
            edge = np.asarray(edge, int).tolist()
        _edge_points.append(edge)

    coords = []
    for vertice in _edge_points:
        coords.append([int(vertice[0][0]), int(vertice[0][1])])
    #print(coords)

    # sorted points by using clockwiseangle_and_distance function
    sort = sorted(points_not_sorted, key=clockwiseangle_and_distance)
    sorted_points = np.array(sort)


    file = open(filename2, 'w')
    file.write('%d\n' % len(new_coords))
    for vertice in reversed(new_coords):
        file.write("%d " % vertice[0])
        file.write("%d\n" % vertice[1])
    file.close()

    # load your correct points to ArtGallery object
    tmp = ArtGallery.load(filename2)
    #print(tmp)

    g = ArtGallery(tmp.pop(0))
    for p in tmp:
        g.include(p)

    triangle = []
    triangles = g._triangulation.get_triangles()
    vertex_color = []
    guard_point = g.get_points()

    for t in triangles:
        i += 1
        print("Triangle %d => (%s,%s)[%s] (%s,%s)[%s] (%s,%s)[%s]" % (i, t.u.x, t.u.y, t.u.color,t.v.x, t.v.y, t.v.color,t.w.x, t.w.y, t.w.color))
        triangle.append([[t.u.x, t.u.y], [t.v.x, t.v.y], [t.w.x, t.w.y]])
        vertex_color.append([t.u.color, t.v.color, t.w.color])

    plt.figure(1)
    pts = np.array(sorted_points)
    plt.scatter(pts[:, 0], pts[:, 1])

    for trian in triangle:
        test = plt.Polygon(trian, fill=None)
        plt.gca().add_patch(test)

 ######################

    triang = tri.Triangulation(pts[:, 0], pts[:, 1])

    plt.figure(2)
    plt.triplot(triang, 'bo-', lw=1)
    for j, p in enumerate(pts):
        plt.text(p[0] - 0.03, p[1] + 0.03, j, ha='right')  # label the points

    guard = []

    print("Gaurds should be placed at following points")
    for p in g.get_points():
        if g.is_guard(p):
            guard.append(p)

    file = open(filename_guards, 'w')
    for vertice in guard:
        file.write("%d " % vertice[1])
        file.write("%d\n" % vertice[2])
    file.close()

    print(guard)

    print("Min_color = " + str(g._color.get_min_color()))
    print("color[1] = " + str(g._color.get_color_count(1)))
    print("color[2] = " + str(g._color.get_color_count(2)))
    print("color[3] = " + str(g._color.get_color_count(3)))

    plt.show()




