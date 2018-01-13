# ! /usr/bin/env python
# coding: utf-8

class Side(tuple):
    """ Represents a 2D side of a polygon. Inherits built-in tuple """

    def __new__(cls, p0, p1):
        if (p0 > p1):
            temp = p0
            p0 = p1
            p1 = temp
        return tuple.__new__(cls, (p0, p1))

    def __init__(self, p0, p1):
        if (p0 > p1):
            temp = p0
            p0 = p1
            p1 = temp
        super(Side, self).__init__(p0, p1)
        self.p0 = p0
        self.p1 = p1

    def __repr__(self):
        return "(%s-%s)" % (self.p0, self.p1)


# Testing class
if __name__ == "__main__":
    from point import Point

    side = Side(Point(1, 0, 0), None)

    print(side)
    print("p0 = %s" % str(side.p0))
    print("p1 = %s" % str(side.p1))
    print("[0] = %s" % str(side[0]))
    print("[1] = %s" % str(side[1]))


