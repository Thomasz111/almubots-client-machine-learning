from utils.almubots_comm import Comm
import math

from utils.bot_utils import dist, sgn


class ShootClosestBot:
    def __init__(self, bot_num):
        self.bot_num = bot_num
        self.comm = Comm(bot_num)

    def rotateBot(self, my_bot, closest_bot, main_bot):
        x = closest_bot['x'] - my_bot['x']
        y = closest_bot['y'] - my_bot['y']
        ang = my_bot['angle']

        angle_to_enemy = 0
        if x != 0:
            angle_to_enemy = math.atan(y / x) * 180 / math.pi
        if x < 0:
            angle_to_enemy += 180
        angle_to_enemy -= ang
        angle_to_enemy //= 1
        angle_to_enemy %= 360

        rotate = 0
        shoot = 0
        if angle_to_enemy % 10 != 5:

            angle_to_enemy = round(angle_to_enemy / 10, 0)
            angle_to_enemy %= 36

            if angle_to_enemy > 18:
                rotate = -(36 - angle_to_enemy)
            else:
                rotate = angle_to_enemy

            if my_bot['ammo'] < 5:
                if closest_bot == main_bot:
                    shoot = 1
            else:
                shoot = 1
        return rotate, shoot

    def run(self):
        status = self.comm.send()
        new_x = 0
        while True:
            new_x += 1
            if new_x == 360:
                new_x = 0
            bots = status['bots']

            # my bot
            my_bot = bots[self.bot_num]
            my_x = my_bot['x']
            my_y = my_bot['y']

            # enemies
            current_bot = {
                'id': 0,
                'x': 0,
                'y': 0,
                'vx': 0,
                'vy': 0,
                'angle': 0,
                'ammo': 0,
                'life': 100,
                'shoot': False,
                'score': 0
            }
            lowest_hp_bot = current_bot
            for bot in bots:
                if bot == my_bot:
                    continue
                enemy_hp = bot['life']
                if lowest_hp_bot['life'] > enemy_hp > 0:
                    lowest_hp_bot = bot
                if enemy_hp == lowest_hp_bot['life'] and enemy_hp > 0:
                    if dist(my_bot, bot) < dist(my_bot, lowest_hp_bot) and enemy_hp > 0:
                        lowest_hp_bot = bot

            closest_bot = lowest_hp_bot
            for bot in bots:
                enemy_hp = bot['life']
                if bot == my_bot:
                    continue
                if dist(my_bot, bot) < dist(my_bot, closest_bot) and enemy_hp > 0:
                    closest_bot = bot

            # move to enemy
            if dist(my_bot, closest_bot) > 150:
                self.comm.move(sgn(lowest_hp_bot['x'] - my_x), sgn(lowest_hp_bot['y'] - my_y))
                status = self.comm.send()
            else:
                self.comm.move(-sgn(lowest_hp_bot['x'] - my_x), -sgn(lowest_hp_bot['y'] - my_y))
                status = self.comm.send()
            if dist(my_bot, lowest_hp_bot) < 300 and lowest_hp_bot['life'] > 0:
                closest_bot = lowest_hp_bot

            rotate, shoot = self.rotateBot(my_bot, closest_bot, lowest_hp_bot)

            if rotate != 0:
                self.comm.rotate(rotate)
                status = self.comm.send()

            if shoot != 0:
                self.comm.shoot(shoot)
                status = self.comm.send()
