import utilities


# This class is responsible for tracing a single segment from point to point
# It's used for marking the visibility area of cameras
class RayTrace:
    def __init__(self, occupied_values=None, mark_value=None, sparse=True):

        # When ray tracing reaches one of this values it will stop
        self.occupied_values = occupied_values.copy()
        # Ray tracing will mark using this value
        self.mark_value = mark_value
        # Whether to use sparse or dense ray tracing
        self.sparse = sparse

    def ray_trace(self, grid, start_point, end_point):
        if self.sparse:
            self.sparse_ray_trace(grid, start_point, end_point)
        else:
            self.dense_ray_trace(grid, start_point, end_point)

    # Ray trace a grid using Bresenham 2D algorithm
    # https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    def sparse_ray_trace(self, grid, start_point, end_point):
        if start_point == end_point:
            self.try_mark_cell(grid, start_point)
            return

        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        sign_x = utilities.sign(dx)
        sign_y = utilities.sign(dy)
        dx = abs(dx)
        dy = abs(dy)
        x = start_point[0]
        y = start_point[1]

        change = False

        if dy > dx:
            dy, dx = dx, dy
            change = True

        e = 2 * dy - dx
        i = 1
        while i <= dx:
            if not self.try_mark_cell(grid, [x, y]):
                return

            if e >= 0:
                if not change:
                    y += sign_y
                else:
                    x += sign_x
                e -= 2 * dx

            if e < 0 :
                if not change:
                    x += sign_x
                else:
                    y += sign_y
                e += 2 * dy

            i += 1

    # Ray trace a grid using Xiaolin Wu's algorithm
    # https://en.wikipedia.org/wiki/Xiaolin_Wu%27s_line_algorithm
    def dense_ray_trace(self, grid, start_point, end_point):

        x_start, y_start = start_point
        x_end, y_end = end_point

        dx = x_end - x_start
        if not dx:
            self.sparse_ray_trace(grid, start_point, end_point)
            return

        dy = y_end - y_start
        steep = abs(dx) < abs(dy)
        if steep:
            x_start, y_start = y_start, x_start
            x_end, y_end = y_end, x_end
            dx, dy = dy, dx

        if x_end < x_start:
            step = -1
        else:
            step = 1

        gradient = step * (float(dy) / float(dx))

        # handle first endpoint
        xend = round(x_start)
        yend = y_start + gradient * (xend - x_start)
        xgap = utilities.rfractional_part(x_start + 0.5)
        xpxl1 = xend
        ypxl1 = utilities.integer_part(yend)

        if not self.try_steep_mark_cell(grid, [xpxl1, ypxl1], steep):
            return

        if not self.try_steep_mark_cell(grid, [xpxl1, ypxl1 + 1], steep):
            return

        intery = yend + gradient # first y-intersection for the main loop

        # handle second endpoint
        xend = round(x_end)
        yend = y_end + gradient * (xend - x_end)
        xgap = utilities.fractional_part(x_end + 0.5)
        xpxl2 = xend  # this will be used in the main loop
        ypxl2 = utilities.integer_part(yend)

        # main loop
        for x in range(int(xpxl1 + 1), int(xpxl2), step):

            if not self.try_steep_mark_cell(grid, [x, utilities.integer_part(intery)], steep):
                return

            if not self.try_steep_mark_cell(grid, [x, utilities.integer_part(intery) + 1], steep):
                return

            intery = intery + gradient

        if not self.try_steep_mark_cell(grid, [xpxl2, ypxl2], steep):
            return

        if not self.try_steep_mark_cell(grid, [xpxl2, ypxl2 + 1], steep):
            return

    # Check whether the cell is occupied
    def is_occupied(self, grid, point):
        return grid[point[0]][point[1]] in self.occupied_values

    # Mark a cell
    def mark_cell(self, grid, point):
        grid[point[0]][point[1]] = self.mark_value

    # Check if the cell is occupied. If no then mark it. Returns whether the cell was marked
    def try_mark_cell(self, grid, point):
        if not self.is_occupied(grid, point):
            self.mark_cell(grid, point)
            return True
        else:
            return False

    # Like try_mark_cell, but if steep=True then inverses the point coordinates
    def try_steep_mark_cell(self, grid, point, steep):
        mark_point = point.copy()
        if steep:
            mark_point.reverse()

        return self.try_mark_cell(grid, mark_point)