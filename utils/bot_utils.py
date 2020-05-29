import math


def dist(my_bot, enemy_bot):
    x = my_bot['x'] - enemy_bot['x']
    y = my_bot['y'] - enemy_bot['y']
    return math.sqrt(x * x + y * y)


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
