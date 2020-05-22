import threading

from rule_based_bots.shoot_circle import ShootCircle
from rule_based_bots.shoot_closest import ShootClosestBot
from rule_based_bots.shoot_lowest_life import ShootLowestLifeBot
from rule_based_bots.shoot_winner import ShootWinner

if __name__ == '__main__':
    threading.Thread(target=ShootClosestBot(1).run).start()
    threading.Thread(target=ShootCircle(2).run).start()
    threading.Thread(target=ShootWinner(3).run).start()
