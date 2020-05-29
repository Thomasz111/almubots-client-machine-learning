import threading

from rule_based_bots.shoot_closest import ShootClosestBot
from rule_based_bots.shoot_lowest_life import ShootLowestLifeBot
from dqn_main import Dqn

if __name__ == '__main__':
    try:
        threading.Thread(target=ShootLowestLifeBot(1).run).start()
        threading.Thread(target=Dqn(2, 0, from_scratch=True).run).start()
        # threading.Thread(target=ShootClosestBot(1).run).start()
    except KeyboardInterrupt:
        pass
