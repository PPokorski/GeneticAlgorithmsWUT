class Point(tuple):
    """ Represents a 2D point. Inherits built-in tuple """

    def __new__(cls, num, x, y):
        return tuple.__new__(cls, (int(num), int(x), int(y)))

    def __init__(self, num, x, y):
        #super(Point, self).__init__(num, x, y)
        self.id = int(num)
        self.x = int(x)
        self.y = int(y)
        self.color = 0

    def __repr__(self):
        return "(%s, %s)" % (self.x, self.y)

    def get_pos(self):
        return (self.x, self.y)

if __name__ == "__main__":

    point = Point(0, 3, 8)

    print(point)
    print("id = %s" % point.id)
    print("x = %s" % point.x)
    print("y = %s" % point.y)

    for i in point:
        print(i)
