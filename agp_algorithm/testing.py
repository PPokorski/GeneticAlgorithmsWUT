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
    triang = []
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
            triang.append([ia, ib, ic])
    m = geometry.MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return cascaded_union(triangles), edge_points, edges, triang
    #return edge_points


from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt


if __name__ == '__main__':
    pass

    filename = "./inputs/temp.poly"
    file = open(filename, "r")

    points = []
    with open(filename, "r") as hfile:
        i = 0
        for line in hfile:
            x, y = line.split()
            points.append([int(x), int(y)])
    file.close()

    points_not_sorted = np.array(points)

    alpha_array = [0.011, 0.015, 0.017, 0.02, 0.023, 0.027, 0.039]
    for i in range(7):
        alpha = alpha_array[i]
        concave_hull, edge_points, edges, triang = alpha_shape(points_not_sorted,
                                                       alpha=alpha)

        print(points_not_sorted[triang])
        plt.triplot(points_not_sorted[:, 0], points_not_sorted[:, 1], triang, 'bo-', lw=1)

        _edge_points = []
        for edge in edge_points:
            if not isinstance(edge, np.ma.MaskedArray):
                edge = np.asarray(edge, int).tolist()
            _edge_points.append(edge)

        #print(concave_hull)
        #print(_edge_points)
        #print(edges)

        # print concave_hull
        lines = LineCollection(edge_points)
        #pl.figure(figsize=(10, 10))

        pl.gca().add_collection(lines)

        pl.plot(points_not_sorted[:, 0], points_not_sorted[:, 1],
                'o', color='#f16824')

        #plot_polygon(concave_hull)
        #pl.plot(x, y, 'o', color='#f16824')
        plt.show()
    pl.show()