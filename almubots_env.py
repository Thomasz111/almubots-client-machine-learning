import math

import gym
from gym import spaces
import numpy as np

from utils.almubots_comm import Comm

from utils.bot_utils import dist, desired_angle


class AlmubotsEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, num_of_bots, bot_num):
        self.num_of_bots = num_of_bots
        self.bot_num = bot_num
        self.comm = Comm(bot_num)

        # posX, posY, velX, velY, angle, ammo, life, shoot, score
        # low = np.tile(np.array([0, 0, -500, -500, 0, 0, 0, 0, 0], dtype=np.float32), self.num_of_bots)
        # high = np.tile(np.array([900, 900, 500, 500, 360, 10, 20, 1, 1000], dtype=np.float32), self.num_of_bots)

        # self.observation_space = spaces.Box(low, high, dtype=np.float32)

        # rotate: -1, 0, 1
        # move: (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)
        # shoot: 0, 1
        self.action_space = spaces.Discrete(14)

        self.state = None

        self.previous_life = 20
        self.previous_score = 0

    def step(self, action):
        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg

        self.comm.reset_cmd()

        # for values go to end of this file
        # shoot or not
        # if action >= 27:
        #     self.comm.shoot(1)
        #     action -= 27
        # else:
        #     self.comm.shoot(0)

        # rotate lef, right, non
        # if action < 9:
        #     self.comm.rotate(-1)
        # elif action >= 18:
        #     self.comm.rotate(1)
        #     action -= 18
        # else:
        #     self.comm.rotate(0)
        #     action -= 9
        # # move x, y
        # movement = {
        #     0: (-1, -1),
        #     1: (-1, 0),
        #     2: (-1, 1),
        #     3: (0, -1),
        #     4: (0, 0),
        #     5: (0, 1),
        #     6: (1, -1),
        #     7: (1, 0),
        #     8: (1, 1)
        # }
        # self.comm.move(movement.get(action)[0], movement.get(action)[1])
        if action >= 7:
            self.comm.shoot(1)
            action -= 7
        # else:
        #     self.comm.shoot(0)

        # movement = {
        #     3: (-1, -1),
        #     4: (-1, 0),
        #     5: (-1, 1),
        #     6: (0, -1),
        #     # 7: (0, 0),
        #     7: (0, 1),
        #     8: (1, -1),
        #     9: (1, 0),
        #     10: (1, 1)
        # }


        # if action >= 3 and action <= 10:
        #     self.comm.move(movement[action][0], movement[action][1])

        if action == 7:
            self.comm.shoot(1)
        if action == 1:
            self.comm.rotate(1)
        elif action == 2:
            self.comm.rotate(-1)
        elif action == 3:
            self.comm.move(0, 1)
        elif action == 4:
            self.comm.move(0, -1)
        elif action == 5:
            self.comm.move(1, 0)
        elif action == 6:
            self.comm.move(-1, 0)
        else:
            pass

        state_raw = (self.comm.send())

        bots_status = state_raw['bots']
        max_angle = 360

        self.state = []
        away_x = bots_status[0]["x"] - bots_status[1]["x"]
        away_y = bots_status[0]["y"] - bots_status[1]["y"]
        self.state.append(away_x)
        self.state.append(away_y)
        self.state.append(bots_status[0]["vx"] - bots_status[1]["vx"])
        self.state.append(bots_status[0]["vy"] - bots_status[1]["vy"])
        for bot in bots_status:

            # if bot['id'] == self.bot_num:
            self.state.append(bot["angle"])
            # self.state.append(bot["ammo"])

            if bot['id'] == self.bot_num:
                self.state.append(bot["score"])
            if bot['id'] != self.bot_num:
                self.state.append(bot["life"])
            self.state.append(bot["shoot"])


        if bots_status[self.bot_num]['life'] == 20:
            self.previous_life = 20

        # reward = 1 if bots_status[self.bot_num]['shoot'] else 0 + \

        me = bots_status[self.bot_num]
        enemy = bots_status[self.num_of_bots - self.bot_num - 1]

        reward =  (bots_status[self.bot_num]['score'] - self.previous_score) * 100 \
                  - (self.previous_life - bots_status[self.bot_num]['life']) * 20 \
                + dist(bots_status[self.bot_num], bots_status[self.num_of_bots - self.bot_num - 1]) / 300 \
                - desired_angle(me, enemy) / 180.0
                # + desired_angle(enemy, me) / 180.0

        if self.previous_score > bots_status[self.bot_num]['score']:
            reward = 0

        # print(f'previous_life: {self.previous_life} '
        #       f'current_life: {bots_status[self.bot_num]["life"]} '
        #       f'shoot: {bots_status[self.bot_num]["shoot"]} '
        #       f'previous_score: {self.previous_score} '
        #       f'current_score: {bots_status[self.bot_num]["score"]} '
        #       f'duze dzialanie: { (bots_status[self.bot_num]["score"] - self.previous_score)} '
        #       f'reward: {reward}')

        self.previous_score = bots_status[self.bot_num]['score']
        self.previous_life = bots_status[self.bot_num]['life']

        done = state_raw['reset']

        return np.array(self.state), 0 if done else reward, done, {}

    def reset(self):
        self.previous_life = 20
        self.previous_score = 0
        return np.zeros(10)
        # return np.zeros((self.num_of_bots * 2 + ((self.num_of_bots-1) * 1) + 4 + 1))

    def render(self, mode='human'):
        # why render, when u can NOT TO FOR ONLY 19.99$ IF U CALL US RIGHT NOW!
        pass

# IN CASE OF FUCKUP
# nothing
# 0,0,0,0

# rotation
# -1,0,0,0
# 1,0,0,0

# vx
# 0,-1
# 0,1,0,0

# vy
# 0,0,-1
# 0,0,1,0

# shooting
# 0,0,0,1



# ----------------------------

# rotation
# -1,0,0,1
# 1,0,0,1

# vx
# 0,-1, 0, 1
# 0,1,0,1

# vy
# 0,0,-1, 1
# 0,0,1,1

# rotation, vx, vy, shoot
# -1,-1,-1,0
# -1,-1,0,0
# -1,-1,1,0
# -1,0,-1,0
# -1,0,0,0
# -1,0,1,0
# -1,1,-1,0
# -1,1,0,0
# -1,1,1,0
# 0,-1,-1,0
# 0,-1,0,0
# 0,-1,1,0
# 0,0,-1,0
# 0,0,0,0
# 0,0,1,0
# 0,1,-1,0
# 0,1,0,0
# 0,1,1,0
# 1,-1,-1,0
# 1,-1,0,0
# 1,-1,1,0
# 1,0,-1,0
# 1,0,0,0
# 1,0,1,0
# 1,1,-1,0
# 1,1,0,0
# 1,1,1,0
# -1,-1,-1,1
# -1,-1,0,1
# -1,-1,1,1
# -1,0,-1,1
# -1,0,0,1
# -1,0,1,1
# -1,1,-1,1
# -1,1,0,1
# -1,1,1,1
# 0,-1,-1,1
# 0,-1,0,1
# 0,-1,1,1
# 0,0,-1,1
# 0,0,0,1
# 0,0,1,1
# 0,1,-1,1
# 0,1,0,1
# 0,1,1,1
# 1,-1,-1,1
# 1,-1,0,1
# 1,-1,1,1
# 1,0,-1,1
# 1,0,0,1
# 1,0,1,1
# 1,1,-1,1
# 1,1,0,1
# 1,1,1,1
