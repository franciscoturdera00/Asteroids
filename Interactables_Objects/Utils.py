
import math


def calculate_new_rotated_position(point, angle):
        x, y = point
        new_x = (x * math.cos(angle)) - (y * math.sin(angle))
        new_y = (x * math.sin(angle)) + (y * math.cos(angle))
        return new_x, new_y