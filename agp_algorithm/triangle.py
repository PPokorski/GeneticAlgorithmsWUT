
from point import Point
from side import Side

class Triangle(object):
    """ Class representing a Triangle that is composed by
    three Point objects
    """

    def __init__(self, u, v, w):

        if not all(isinstance(point, Point) for point in (u, v, w)):
            raise TypeError("u, v, w must be Point objects", (u, v, w))

        self.u, self.v, self.w = u, v, w

    def __repr__(self):
        return "[(%s, %s), (%s, %s), (%s, %s)]" \
               % (self.u.x, self.u.y, self.v.x, self.v.y, self.w.x, self.w.y)

    def __iter__(self):
        yield self.u
        yield self.v
        yield self.w

    def sides(self):
        return (Side(self.u, self.v), Side(self.v, self.w), Side(self.w, self.u))

    def opposite(self, side):
        if self.u == side.p0:
            if self.v == side.p1:
                return self.w
            else:
                return self.v
        elif self.u == side.p1:
            if self.v == side.p0:
                return self.w
            else:
                return self.v
        return self.u


