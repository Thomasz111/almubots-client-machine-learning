import os

# for keras the CUDA commands must come before importing the keras libraries
from almubots_env import AlmubotsEnv

os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
import gym
from gym import wrappers
import numpy as np
from ddqn_keras import DDQNAgent
from dqn_utils import plotLearning


class DDQN:
    def __init__(self, num_of_bots: int, bot_num: int, from_scratch: bool):
        self.num_of_bots = num_of_bots
        self.bot_num = bot_num
        self.from_scratch = from_scratch

    def run(self):

        env = AlmubotsEnv(num_of_bots=self.num_of_bots, bot_num=self.bot_num)
        ddqn_agent = DDQNAgent(alpha=0.0005, gamma=0.99, n_actions=8, epsilon=1.0,
                               batch_size=64, input_dims=10, epsilon_dec=0.995, epsilon_end=0.01, replace_target=100)
        n_games = 500

        if not self.from_scratch:
            try:
                ddqn_agent.load_model()
            except:
                print("No model, starting from scratch.")
        else:
            print("FROM SCRATCH!")
        ddqn_scores = []
        eps_history = []
        # env = wrappers.Monitor(env, "tmp/lunar-lander-ddqn-2",
        #                         video_callable=lambda episode_id: True, force=True)

        for i in range(n_games):
            done = False
            score = 0
            observation = env.reset()
            while not done:
                action = ddqn_agent.choose_action(observation)
                observation_, reward, done, info = env.step(action)
                score += reward
                ddqn_agent.remember(observation, action, reward, observation_, int(done))
                observation = observation_
                ddqn_agent.learn()
            eps_history.append(ddqn_agent.epsilon)

            ddqn_agent.decrease_epsilon()

            ddqn_scores.append(score)

            avg_score = np.mean(ddqn_scores[max(0, i - 100):(i + 1)])
            print('episode: ', i, 'score: %.2f' % score,
                  ' average score %.2f' % avg_score)

            if i % 10 == 0 and i > 0:
                ddqn_agent.save_model()
                filename = f'ddqn-bot{self.bot_num}.png'
                x = [i + 1 for i in range(len(eps_history))]
                plotLearning(x, ddqn_scores, eps_history, filename)

        filename = f'ddqn-bot{self.bot_num}.png'
        x = [i + 1 for i in range(len(eps_history))]
        plotLearning(x, ddqn_scores, eps_history, filename)
