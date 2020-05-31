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


def desired_angle(my_bot, enemy_bot):
    """returns value between 0-180. 0 means aiming directly at enemy_bot"""
    angle = math.atan2(enemy_bot['y'] - my_bot['y'], enemy_bot['x'] - my_bot['x'])
    angle = (angle * 180 / math.pi) % 360

    if angle < 0:
        angle += 360
    # angle is now 0-360

    my_ang = my_bot['angle']
    if my_ang < 0:
        my_ang += 360
    # my_ang is now 0-360

    angle_diff = abs(my_ang - angle)
    if angle_diff > 180:
        angle_diff = 360 - angle_diff

    return angle_diff

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
