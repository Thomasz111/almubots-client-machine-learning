import gym
from gym import spaces
import numpy as np

from utils.almubots_comm import Comm


class AlmubotsEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, num_of_bots, bot_num):
        self.num_of_bots = num_of_bots
        self.bot_num = bot_num
        self.comm = Comm(bot_num)

        # posX, posY, velX, velY, angle, ammo, life, shoot, score
        low = np.tile(np.array([0, 0, -500, -500, 0, 0, 0, 0, 0], dtype=np.float32), self.num_of_bots)
        high = np.tile(np.array([900, 900, 500, 500, 360, 10, 20, 1, 1000], dtype=np.float32), self.num_of_bots)

        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        # rotate: -1, 0, 1
        # move: (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)
        # shoot: 0, 1
        self.action_space = spaces.Discrete(54)

        self.state = None

    def step(self, action):
        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg

        self.comm.reset_cmd()

        # for values go to end of this file
        # shoot or not
        if action >= 27:
            self.comm.shoot(1)
            action -= 27
        else:
            self.comm.shoot(0)

        # rotate lef, right, non
        if action < 9:
            self.comm.rotate(-1)
        elif action >= 18:
            self.comm.rotate(1)
            action -= 18
        else:
            self.comm.rotate(0)
            action -= 9
        # move x, y
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
        for bot in bots_status:
            self.state.append(bot["x"])
            self.state.append(bot["y"])
            self.state.append(bot["vx"])
            self.state.append(bot["vy"])
            self.state.append(bot["angle"])
            self.state.append(bot["ammo"])
            self.state.append(bot["life"])
            self.state.append(bot["shoot"])
            self.state.append(bot["score"])

        reward = bots_status[self.bot_num]['score']

        done = state_raw['reset']

        return np.array(self.state), reward, done, {}

    def reset(self):
        # env resets itself
        pass

    def render(self, mode='human'):
        # why render, when u can NOT TO FOR ONLY 19.99$ IF U CALL US RIGHT NOW!
        pass

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
