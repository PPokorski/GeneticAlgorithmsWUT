from point import Point
from triangle import Triangle
from side import Side

class Triangulation(object):
    """ Class that triangulates polygons with no hole """

    # Used to verify if triangulation is counter clockwise
    EPSILON = 0.0000000001

    def __init__(self, points):

        if not isinstance(points, list):
            raise TypeError("_polygon must be a list")
        elif not all(isinstance(point, Point) for point in points):
            raise TypeError("elements of list must be Point objects")

        self._polygon = points
        self._clean()

    def _clean(self):
        self._diagonals = {}
        self._sides = {}
        self._triangles = []
        self._start = None

    def _add_diagonal(self, triangle):
        # identity of diaginal
        diag = Side(triangle.u, triangle.w)
        # mapping the triangulation
        self._diagonals[diag] = triangle
        self._add_triangle(triangle)

    def _add_triangle(self, triangle):
        # put the triangle in list
        self._triangles.append(triangle)
        if self._start is None: self._start = triangle
        for side in triangle.sides():
            tt = self._sides.get(side)
            # side already mapped
            if tt:
                self._sides[side] = (tt[0], triangle)
            else:
                self._sides[side] = (triangle, None)

    def get_start(self):
        return self._start

    def get_triangles(self):
        return self._triangles

    def get_diagonals(self):
        return self._diagonals.keys()

    def get_neighbors(self, triangle):
        """ return all neighbors (max 3) of a triangle """
        neighbors = []
        for side in triangle.sides():
            neighbor = self.get_opposite(triangle, side)
            if neighbor:
                neighbors.append(neighbor)
        return neighbors

    def get_opposite(self, triangle, side):
        """ return the opposite triangle of a given triangle side """
        tt = self._sides.get(side)
        if tt:
            if tt[0] != triangle:
                return tt[0]
            elif tt[1]:
                return tt[1]
        return None

    def _set_indexes(self, v, n_points):
        """ Set indexes for triangulation based on v parameter """

        u = v
        if u >= n_points:
            u = 0

        v = u + 1
        if v >= n_points:
            v = 0

        w = v + 1
        if w >= n_points:
            w = 0

        return u, v, w

    def process(self):
        """ Process and triangulates the polygon """
        # clear the current triangulation
        self._clean()
        n_points = len(self._polygon)  # Controls the number of _polygon
        # Minimum number of _polygon to compose a triangle
        if n_points < 3:
            return False

        tmp_points = self._polygon[:]  # temporary list of _polygon
        # this algorithm runs in Clockwise orientation...
        if self._area() < 0.0:
            tmp_points.reverse()

        # controls the current triangle points inside the while statement
        v = n_points - 1
        attempts = (n_points + 3)
        while n_points > 3:

            if not attempts:
                self._clean()
                return False
            attempts -= 1

            u, v, w = self._set_indexes(v, n_points)

            # Creates a Triangle object with three consecutives Point objects
            triangle = Triangle(tmp_points[u], tmp_points[v], tmp_points[w])

            # check if this triangle can be cutted (snipped)
            if self._snip(tmp_points, triangle):
                # add current triangle to triangulation
                self._add_diagonal(triangle)
                # remove triangle from polygon
                tmp_points.remove(tmp_points[v])
                #v = last_mark # see above
                # adjust the loop controls
                n_points -= 1
                attempts = (n_points + 3)
        # add last triangle to triangulation
        triangle = Triangle(tmp_points[0], tmp_points[1], tmp_points[2])
        self._add_triangle(triangle)
        del tmp_points
        return True

    def _is_inside(self, point, triangle):
        """ Verify if a given point belongs to a triangle inner _area """

        ax, ay = triangle.w.x - triangle.v.x, triangle.w.y - triangle.v.y
        bx, by = triangle.u.x - triangle.w.x, triangle.u.y - triangle.w.y
        cx, cy = triangle.v.x - triangle.u.x, triangle.v.y - triangle.u.y

        apx, apy = point.x - triangle.u.x, point.y - triangle.u.y
        bpx, bpy = point.x - triangle.v.x, point.y - triangle.v.y
        cpx, cpy = point.x - triangle.w.x, point.y - triangle.w.y

        a_cross = ax*bpy - ay*bpx
        b_cross = bx*cpy - by*cpx
        c_cross = cx*apy - cy*apx

        return a_cross >= 0 and b_cross >= 0 and c_cross >= 0

    def _snip(self, points, triangle):
        """Return true if the polygon can be snipped """

        oppos = (triangle.v.x - triangle.u.x) * (triangle.w.y - triangle.u.y)
        adjac = (triangle.v.y - triangle.u.y) * (triangle.w.x - triangle.u.x)

        # the triangle makes a inverse corner (open corner)?
        if self.EPSILON > (oppos - adjac):
            # if so, then this triangle isn't a ear of polygon...
            return False

        # verify if the point belongs to the triangle
        for point in points:
            if point not in triangle and self._is_inside(point, triangle):
                return False
        return True

    def _area(self):
        size = len(self._polygon)
        area = 0.0
        i0 = size -1
        i1 = 0
        while i1 < size:
            area += self._polygon[i0].x * self._polygon[i1].y - \
                    self._polygon[i0].y * self._polygon[i1].x
            i0 = i1
            i1 += 1
        return (area / 2)


