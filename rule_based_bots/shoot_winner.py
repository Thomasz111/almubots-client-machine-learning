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
        self.small_health = 5
        self.close_dist = 125
        self.medium_dist = 250
        self.dist_to_shoot = 200

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
        angle = (atan2(dy, dx) * 180 / pi) % 360
        if a != 0:
            b = 2 * (vx * dx + vy * dy)
            c = dx * dx + dy * dy
            (t1, t2) = quadratic_equation(a, b, c)
            if t1 == 0:
                return angle
            if t1 < 0:
                t1 = 1000
            if t2 < 0:
                t2 = 1000
            if t1 > t2:
                t1 = t2
            if t1 == 1000:
                return angle
            dx = x2 - x1 + vx * (t1 + delta_time)
            dy = y2 - y1 + vy * (t1 + delta_time)
            angle = (atan2(dy, dx) * 180 / pi) % 360
        return angle

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
            score_dif = 0
            for current_bot in bots:
                if current_bot is not my:
                    if current_bot['score'] > max_score_bot['score'] and current_bot['life'] != 0:
                        score_dif = current_bot['score'] - max_score_bot['score']
                        max_score_bot = current_bot
                    if dist(my, current_bot) < dist(my, closest_bot) and current_bot['life'] != 0:
                        closest_bot = current_bot
                    if (current_bot['life'] < smallest_hp_bot['life']) and current_bot['life'] != 0:
                        smallest_hp_bot = current_bot

            if (my['life'] <= smallest_hp_bot['life']) or (score_dif < self.min_score_dif) \
                    or (smallest_hp_bot['life'] < self.small_health and smallest_hp_bot['life'] != 0):
                bot_to_target = smallest_hp_bot
            else:
                bot_to_target = max_score_bot

            y1 = my['y']
            x1 = my['x']
            x2 = closest_bot['x']
            y2 = closest_bot['y']
            x3 = bot_to_target['x']
            y3 = bot_to_target['y']
            if dist(my, bot_to_target) < self.medium_dist:
                if dist(my, bot_to_target) < self.close_dist:
                    angle_to_enemy = get_angle_between_bots(my, bot_to_target)
                else:
                    angle_to_enemy = self.get_angle_with_speed_prediction(my, bot_to_target, delta_time)
            else:
                bot_to_target = closest_bot
                if dist(my, closest_bot) < self.close_dist:
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

            if my['life'] > self.small_health:
                if dist(my, closest_bot) < self.close_dist:
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
            if my['ammo'] >= self.max_ammo - 1 or dist(my, bot_to_target) < self.dist_to_shoot \
                    or bot_to_target['life'] < self.small_health:
                shoot = True
            comm.shoot(shoot)

            status = comm.send()
