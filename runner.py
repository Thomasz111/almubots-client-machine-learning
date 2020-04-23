import threading

from shoot_closest import ShootClosestBot
from shoot_lowest_life import ShootLowestLifeBot

if __name__ == '__main__':
    threading.Thread(target=ShootClosestBot(1).run).start()
    threading.Thread(target=ShootLowestLifeBot(2).run).start()
