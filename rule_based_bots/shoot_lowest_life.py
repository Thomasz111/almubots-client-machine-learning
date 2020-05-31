from math import atan2, pi

from utils.almubots_comm import Comm


class ShootLowestLifeBot:
    def __init__(self, bot_num):
        self.bot_num = bot_num
        self.comm = Comm(bot_num)

    def run(self):
        status = self.comm.send()
        while True:
            me = status['bots'][self.bot_num]
            enemy = status['bots'][0]

            for bot in status['bots']:
                if bot is not me and bot['life'] != 0:
                    if enemy['life'] > bot['life']:
                        enemy = bot

            angle = atan2(enemy['y'] - me['y'], enemy['x'] - me['x'])
            angle = angle * 180 / pi
            angle_diff = abs(me['angle']-angle)
            if angle > me['angle']:
                if angle_diff <= 180:
                    self.comm.rotate(1)
                    status = self.comm.send()
                else:
                    self.comm.rotate(-1)
                    status = self.comm.send()
            elif angle < me['angle']:
                if angle_diff <= 180:
                    self.comm.rotate(-1)
                    status = self.comm.send()
                else:
                    self.comm.rotate(1)
                    status = self.comm.send()

            me = status['bots'][self.bot_num]
            enemy = status['bots'][0]

            for bot in status['bots']:
                if bot is not me and bot['life'] != 0:
                    if enemy['life'] > bot['life']:
                        enemy = bot

            dx = 0
            dy = 0
            if enemy['x'] > me['x']:
                dx = 1
            if enemy['y'] > me['y']:
                dy = 1
            if enemy['x'] < me['x']:
                dx = -1
            if enemy['y'] < me['y']:
                dy = -1

            self.comm.move(dx, dy)
            status = self.comm.send()

            me = status['bots'][self.bot_num]
            enemy = status['bots'][0]

            for bot in status['bots']:
                if bot is not me and bot['life'] != 0:
                    if enemy['life'] > bot['life']:
                        enemy = bot

            angle = atan2(enemy['y'] - me['y'], enemy['x'] - me['x'])
            angle = angle * 180 / pi

            shoot = False
            if abs(me['angle'] - angle) < 10:
                shoot = True

            self.comm.shoot(shoot)
            status = self.comm.send()
