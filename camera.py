import math

import utilities


# Given angle, return an angle that is between 0 and 2*PI radians
# This also works for negative angles
def normalize_angle(angle):

    return angle % (2*math.pi)


class Camera:
    def __init__(self, position=[0, 0], orientation=0.0,
                 angle_of_view=1.57, range_of_view=1.0,
                 angular_resolution=0.02):

        # Position in the world
        self.position = position.copy()
        # Direction in which the camera is watching, expressed in rads and in range of [0, 2*PI]
        self.orientation = orientation
        # Camera's field of view, expressed in rads
        self.angle_of_view = angle_of_view
        # Camera's range of view, expressed in the same units as coordinates
        self.range_of_view = range_of_view
        # The camera's angular resolution used for ray tracing
        # It's the angle between consecutive rays
        self.angular_resolution = angular_resolution

    def set_position(self, position, orientation):
        self.position = position.copy()
        self.orientation = orientation

    # Get the list of points which correspond to the camera's arc of visibility range
    def get_discrete_range_of_view(self, angle_resolution=0.02):

        # This list holds points lying on the arc of visibility
        arc_points = []

        # This value holds the beginning angle of the arc
        start_angle = normalize_angle(self.orientation - self.angle_of_view/2.0)
        # This value holds the end angle of the arc
        end_angle = normalize_angle(self.orientation + self.angle_of_view/2.0)

        number_of_points = int(self.angle_of_view / angle_resolution)

        for i in range(number_of_points):
            angle = normalize_angle(start_angle + i * angle_resolution)

            x = utilities.integer_round(self.position[0] + self.range_of_view * math.cos(angle))
            y = utilities.integer_round(self.position[1] + self.range_of_view * math.sin(angle))

            arc_points.append([x, y])

        # If the last point on the list is not the end of the angle (because of discretization)
        # then add it
        end_x = utilities.integer_round(self.position[0] + self.range_of_view * math.cos(end_angle))
        end_y = utilities.integer_round(self.position[1] + self.range_of_view * math.sin(end_angle))
        if arc_points[-1] != [end_x, end_y]:
            arc_points.append([end_x, end_y])

        return arc_points
