from utils.almubots_comm import Comm


class ShootCircle:
    def __init__(self, bot_num):
        self.bot_num = bot_num
        self.comm = Comm(bot_num)
        self.half_screen_size = 450

    def run(self):
        while True:
            status = self.comm.send()
            me = status['bots'][self.bot_num]

            dx = 0
            dy = 0
            if self.half_screen_size > me['x']:
                dx = 1
            if self.half_screen_size > me['y']:
                dy = 1
            if self.half_screen_size < me['x']:
                dx = -1
            if self.half_screen_size < me['y']:
                dy = -1

            self.comm.rotate(1)
            self.comm.move(dx, dy)
            self.comm.shoot(True)
