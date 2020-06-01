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
        self.action_space = spaces.Discrete(9)

        self.state = None

        self.previous_life = 20
        self.previous_score = 0

    def step(self, action):
        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg

        self.comm.reset_cmd()

        movement = {
            0: (-1, -1),
            1: (-1, 0),
            2: (-1, 1),
            3: (0, -1),
            4: (0, 0),
            5: (0, 1),
            6: (1, -1),
            7: (1, 0),
            8: (1, 1)
        }
        self.comm.move(movement.get(action)[0], movement.get(action)[1])

        state_raw = (self.comm.send())

        bots_status = state_raw['bots']

        self.state = []
        self.state += [bots_status[0]["x"], bots_status[0]["y"], bots_status[0]["vx"], bots_status[0]["vy"]]
        self.state += [bots_status[1]["x"], bots_status[1]["y"], bots_status[1]["vx"], bots_status[1]["vy"]]
        self.state += [bots_status[1]["angle"]]

        if bots_status[self.bot_num]['life'] == 20:
            self.previous_life = 20

        me = bots_status[self.bot_num]
        enemy = bots_status[self.num_of_bots - self.bot_num - 1]

        angle = desired_angle(enemy, me)
        # print(angle)
        reward = angle / 180.0

        if self.previous_score > bots_status[self.bot_num]['score']:
            reward = 0

        self.previous_score = bots_status[self.bot_num]['score']
        self.previous_life = bots_status[self.bot_num]['life']

        done = state_raw['reset']

        return np.array(self.state), 0 if done else reward, done, {}

    def reset(self):
        self.previous_life = 20
        self.previous_score = 0
        bots_status = self.comm.status()['bots']
        if len(bots_status) == 0:
            return np.zeros(9)
        return np.array([bots_status[0]["x"], bots_status[0]["y"], bots_status[0]["vx"], bots_status[0]["vy"],
                         bots_status[1]["x"], bots_status[1]["y"], bots_status[1]["vx"], bots_status[1]["vy"],
                         bots_status[1]["angle"]])
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
