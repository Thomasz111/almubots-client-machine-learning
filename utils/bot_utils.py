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


def quadratic_equation(a, b, c):
    delta = b * b - (4 * a * c)
    if delta < 0:
        return 0, 0
    else:
        delta_root = math.sqrt(delta)

        x1 = (-b - delta_root) / 2 / a
        x2 = (-b + delta_root) / 2 / a

        return x1, x2
