import time
from math import atan2, pi
from utils.almubots_comm import Comm
from utils.bot_utils import dist, quadratic_equation, rotation_to_target, get_angle_between_bots


class ShootWinner:
    def __init__(self, bot_num):
        self.bot_num = bot_num
        self.comm = Comm(bot_num)
        self.max_ammo = 10
        self.bullet_speed = 700
        self.min_score_dif = 100

    def get_angle_with_speed_prediction(self, bot1, bot2, delta_time):
        x1 = bot1['x']
        x2 = bot2['x']
        y1 = bot1['y']
        y2 = bot2['y']
        vx = bot2['vx']
        vy = bot2['vy']
        a = vx ** 2 + vy ** 2 - self.bullet_speed ** 2
        dx = (x2 - x1)
        dy = (y2 - y1)
        beta = (atan2(dy, dx) * 180 / pi) % 360
        if a != 0:
            b = 2 * (vx * dx + vy * dy)
            c = dx * dx + dy * dy
            (t1, t2) = quadratic_equation(a, b, c)
            if t1 == 0:
                return beta
            if t1 < 0:
                t1 = 1000
            if t2 < 0:
                t2 = 1000
            if t1 > t2:
                t1 = t2
            if t1 == 1000:
                return beta
            dx = x2 - x1 + vx * (t1 + delta_time)
            dy = y2 - y1 + vy * (t1 + delta_time)
            beta = (atan2(dy, dx) * 180 / pi) % 360
        return beta

    def run(self):
        prev_time = time.clock()
        comm = Comm(self.bot_num)
        status = comm.send()

        while True:
            delta_time = (time.clock() - prev_time)
            prev_time = time.clock()

            bots = status['bots']
            my = bots[self.bot_num]

            smallest_hp_bot = bots[0]
            closest_bot = bots[0]
            max_score_bot = bots[0]
            max_distance = 1000
            smallest_hp = 21
            max_score = -1
            score_dif = 0
            for bot in bots:
                if bot is not my:
                    dist_to_enemy = dist(my, bot)
                    current_bot_hp = bot['life']
                    current_bot_score = bot['score']
                    if current_bot_score > max_score and current_bot_hp != 0:
                        score_dif = current_bot_score - max_score
                        max_score = current_bot_score
                        max_score_bot = bot
                    if dist_to_enemy < max_distance and current_bot_hp != 0:
                        max_distance = dist_to_enemy
                        closest_bot = bot
                    if (current_bot_hp < smallest_hp) and (current_bot_hp != 0):
                        smallest_hp = current_bot_hp
                        smallest_hp_bot = bot

            if (my['life'] <= smallest_hp) or (score_dif < self.min_score_dif) or (smallest_hp < 5):
                max_score_bot = smallest_hp_bot

            y1 = my['y']
            x1 = my['x']
            x2 = closest_bot['x']
            y2 = closest_bot['y']
            x3 = max_score_bot['x']
            y3 = max_score_bot['y']
            if dist(my, max_score_bot) < 250:
                if dist(my, max_score_bot) < 125:
                    angle_to_enemy = get_angle_between_bots(my, max_score_bot)
                else:
                    angle_to_enemy = self.get_angle_with_speed_prediction(my, max_score_bot, delta_time)
            else:
                max_score_bot = closest_bot
                if dist(my, closest_bot) < 125:
                    angle_to_enemy = get_angle_between_bots(my, closest_bot)
                else:
                    angle_to_enemy = self.get_angle_with_speed_prediction(my, closest_bot, delta_time)
            comm.rotate(rotation_to_target(angle_to_enemy, my['angle'] % 360))

            if my['vx'] > 0:
                dx = 1
            else:
                dx = -1
            if my['vy'] > 0:
                dy = 1
            else:
                dy = -1

            if my['life'] > 5:
                if dist(my, closest_bot) < 150:
                    if (y1 - y2) > 0:
                        if (x1 - x2) > 0:
                            dx = 1
                            dy = -1
                        else:
                            dy = 1
                            dx = 1
                    else:
                        if (y1 - y2) > 0:
                            dy = -1
                            dx = -1
                        else:
                            dy = 1
                            dx = -1
                else:
                    dx = x3 - x1
                    dy = y3 - y1
            comm.move(dx, dy)

            shoot = False
            if my['ammo'] >= self.max_ammo - 1 or dist(my, max_score_bot) < 200 or max_score_bot['life'] < 5:
                shoot = True
            comm.shoot(shoot)

            status = comm.send()
