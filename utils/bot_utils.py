from math import atan2, pi, sqrt


def dist(my_bot, enemy_bot):
    x = my_bot['x'] - enemy_bot['x']
    y = my_bot['y'] - enemy_bot['y']
    return sqrt(x * x + y * y)


def sgn(val):
    if val > 0:
        return 1
    if val < 0:
        return -1
    return 0


def quadratic_equation(a, b, c):
    delta = b * b - (4 * a * c)
    if delta < 0:
        return 0, 0
    else:
        delta_root = sqrt(delta)

        x1 = (-b - delta_root) / 2 / a
        x2 = (-b + delta_root) / 2 / a

        return x1, x2


def rotation_to_target(angle_to_target, current_gun_angle):
    if abs(angle_to_target - current_gun_angle) <= 5:
        return 0
    else:
        b = (current_gun_angle + 180) % 360
        if 180 > current_gun_angle:
            if (angle_to_target < current_gun_angle) or (angle_to_target > (b + 1)):
                return -1
            else:
                return 1
        elif current_gun_angle == 180:
            if angle_to_target < current_gun_angle:
                return -1
            else:
                return 1
        else:
            if (angle_to_target < b) or (angle_to_target > current_gun_angle):
                return 1
            else:
                return -1


def get_angle_between_bots(bot1, bot2):
    dx = bot2['x'] - bot1['x']
    dy = bot2['y'] - bot1['y']
    if dy == 0:
        if dx > 0:
            return 180
        else:
            return 0

    angle = atan2(dy, dx)
    angle = (angle * 180 / pi) % 360
    return angle
