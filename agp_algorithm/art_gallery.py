import sys
from point import Point
from triangulation import Triangulation
from coloring import Coloring
import threading
import triangulation_test


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
origin = [152, 26]
refvec = [59, 34]

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


import numpy as np
import matplotlib.pyplot as plt
import graphics
from agp_algorithm import testing

if __name__ == '__main__':
    pass

    print("Start ")
    #filename = args[1]
    filename = "C:/Users/Kacper/Desktop/github/GeneticAlgorithmsWUT/agp_algorithm/inputs/temp.poly"
    filename2 = "C:/Users/Kacper/Desktop/github/GeneticAlgorithmsWUT/agp_algorithm/inputs/coords_sorted.poly"
    filename3 = "C:/Users/Kacper/Desktop/github/GeneticAlgorithmsWUT/agp_algorithm/inputs/enterprise.poly"
    file = open(filename, 'r')

    points = []
    with open(filename, "r") as hfile:
        hfile.readline()
        i = 0
        for line in hfile:
            x, y = line.split()
            points.append([int(x), int(y)])
    file.close()

    points_not_sorted = np.array(points)

    alpha_array = [0.021, 0.022, 0.023, 0.024, 0.025, 0.026, 0.027, 0.028, 0.029, 0.03]
    alpha = alpha_array[i]
    concave_hull, edge_points = testing.alpha_shape(points_not_sorted,
                                            alpha=alpha)
    edge_points = np.array(edge_points)
    edge_points.flatten()
    print(edge_points)

    sort = sorted(points_not_sorted, key=clockwiseangle_and_distance)
    sorted_points = np.array(sort)
    #print(sorted_points)

    #from scipy.spatial import ConvexHull
    #hull = ConvexHull(points)
    #print(hull)
    #sorted_points = np.array(hull.points)
    #print(sorted_points)
    file = open(filename2, 'w')
    file.write('71\n')
    for vertice in edge_points:
        file.write("%d %d\n" % vertice[0], vertice[1])
    file.close()
    #filename = "C:/Users/Kacper/Desktop/github/GeneticAlgorithmsWUT/pictures/coords.txt"

    tmp = ArtGallery.load(filename2)

    g = ArtGallery(tmp.pop(0))
    for p in tmp:
        g.include(p)

    triangle = []
    vertices = []
    i = 0


    triangles = g._triangulation.get_triangles()
    #triangles = np.array(triangles)

    guard_point = g.get_points()


    for t in triangles:
        i += 1
        print("Triangle %d => (%s,%s)[%s] (%s,%s)[%s] (%s,%s)[%s]" % (i, t.u.x, t.u.y, t.u.color,t.v.x, t.v.y, t.v.color,t.w.x, t.w.y, t.w.color))
        triangle.append([[t.u.x, t.u.y], [t.v.x, t.v.y], [t.w.x, t.w.y]])

    plt.figure(1)
    #plt.scatter(sorted_points[:, 0], sorted_points[:, 1])
    pts = np.array(sorted_points)
    plt.scatter(pts[:, 0], pts[:, 1])
    #test = np.array(triangle)
    for trian in triangle:
        test = plt.Polygon(trian, fill=None)
        plt.gca().add_patch(test)



 ######################
    from scipy.spatial import Delaunay

    import matplotlib.tri as tri
    #sorted_points -= sorted_points.mean(axis=0)
    triang = tri.Triangulation(sorted_points[:, 0], sorted_points[:, 1])
    #tri = Delaunay(sorted_points, qhull_options = "QJ")

    mask = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 0, 0, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 1, 1, 1, 1, 1, 1, 1,
        0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 0, 0, 0, 0, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0, 0
    ]
    #triang.set_mask(mask)
    plt.figure(2)

    plt.triplot(triang, 'bo-', lw=1)
    for j, p in enumerate(sorted_points):
        plt.text(p[0] - 0.03, p[1] + 0.03, j, ha='right')  # label the points




    #for j, s in enumerate(triang.triangles):
    #    p = sorted_points[s].mean(axis=0)
    #    plt.text(p[0], p[1], '#%d' % j, ha='center')  # label triangles

    #vertices = np.asarray(triangle)
    #print(vertices[0])

    #plt.plot(points[:, 0],points[:,1])
    #plt.triplot(points[:, 0], points[:, 2], vertices, ld=1)
    #plt.plot(vertices)

    guard = []

    print("Gaurds should be placed at following points")
    for p in g.get_points():
        if g.is_guard(p):
            guard.append(p)

    print(guard)

    print("Min_color = " + str(g._color.get_min_color()))
    print("color[0] = " + str(g._color.get_color_count(0)))
    print("color[1] = " + str(g._color.get_color_count(1)))
    print("color[2] = " + str(g._color.get_color_count(2)))
    print("color[3] = " + str(g._color.get_color_count(3)))

    print("END!")

    plt.show()
