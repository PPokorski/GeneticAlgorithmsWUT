from scipy.spatial import Delaunay
import numpy as np
from plotly import tools as tls
import plotly.plotly as py
from plotly.graph_objs import *
import matplotlib.pyplot as plt


import pylab as py
import shapely.geometry as geometry
from shapely.ops import cascaded_union, polygonize
from scipy.spatial import Delaunay
import numpy as np
import math
import pylab as pl


from descartes import PolygonPatch
def plot_polygon(polygon):
    fig = pl.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    margin = .3
    x_min, y_min, x_max, y_max = polygon.bounds
    ax.set_xlim([x_min-margin, x_max+margin])
    ax.set_ylim([y_min-margin, y_max+margin])
    patch = PolygonPatch(polygon, fc='#999999',
                         ec='#000000', fill=True,
                         zorder=-1)
    ax.add_patch(patch)
    return fig


def alpha_shape(points, alpha):
    """
    Compute the alpha shape (concave hull) of a set
    of points.
    @param points: Iterable container of points.
    @param alpha: alpha value to influence the
        gooeyness of the border. Smaller numbers
        don't fall inward as much as larger numbers.
        Too large, and you lose everything!
    """
    if len(points) < 4:
        # When you have a triangle, there is no sense
        # in computing an alpha shape.
        return geometry.MultiPoint(list(points)).convex_hull
    def add_edge(edges, edge_points, coords, i, j):
        """
        Add a line between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            return
        edges.add( (i, j) )
        edge_points.append(coords[ [i, j] ])
    #coords = np.array([point.coords[0]
    #                    for point in points])
    coords = points
    tri = Delaunay(coords)
    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the
    # triangle
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]
        # Lengths of sides of triangle
        a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
        b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
        c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)
        # Semiperimeter of triangle
        s = (a + b + c)/2.0
        # Area of triangle by Heron's formula
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        circum_r = a*b*c/(4.0*area)
        # Here's the radius filter.
        #print circum_r
        if circum_r < 1.0/alpha:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)
    m = geometry.MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return cascaded_union(triangles), edge_points
    #return edge_points


if __name__ == '__main__':
    pass

    filename = "C:/Users/Kacper/Desktop/github/GeneticAlgorithmsWUT/agp_algorithm/inputs/temp.poly"
    file = open(filename, "r")

    points = []
    with open(filename, "r") as hfile:
        hfile.readline()
        i = 0
        for line in hfile:
            x, y = line.split()
            points.append([int(x), int(y)])
    file.close()

    points_not_sorted = np.array(points)

    from matplotlib.collections import LineCollection

#    points = [geometry.shape(points_not_sorted)]
    #cascaded_union, edge_points = alpha_shape(points_not_sorted, alpha=0.015)
    #_ = plot_polygon(concave_hull)
    #_ = pl.plot(x, y, 'o', color='#f16824')
    import matplotlib.pyplot as plt

    alpha_array = [0.021, 0.022, 0.023, 0.024, 0.025, 0.026, 0.027, 0.028, 0.029, 0.03]
    for i in range(10):
        alpha = alpha_array[i]
        concave_hull, edge_points = alpha_shape(points_not_sorted,
                                                alpha=alpha)
        print(edge_points)
        # print concave_hull
        lines = LineCollection(edge_points)
        pl.figure(figsize=(10, 10))
        #pl.title('Alpha={0} Delaunay triangulation'.format(
        #    alpha))
        pl.gca().add_collection(lines)
        #delaunay_points = np.array([point.coords[0]
        #                            for point in points_not_sorted])
        pl.plot(points_not_sorted[:, 0], points_not_sorted[:, 1],
                'o', color='#f16824')

        #plot_polygon(concave_hull)
        #pl.plot(x, y, 'o', color='#f16824')