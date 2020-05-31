from dqn import Agent
import numpy as np
import gym
from dqn_utils import plotLearning
from almubots_env import AlmubotsEnv
import pickle

class Dqn:

    def __init__(self, num_of_bots: int, bot_num: int, from_scratch: bool):
        self.num_of_bots = num_of_bots
        self.bot_num = bot_num
        self.from_scratch = from_scratch

    def run(self):
        env = AlmubotsEnv(num_of_bots=self.num_of_bots, bot_num=self.bot_num)
        lr = 0.0005
        # lr = 0.01
        n_games = 1000
        agent = Agent(gamma=0.99, epsilon=1.0, epsilon_dec=0.99, alpha=lr,
                      # input_dims=self.num_of_bots * 2 + ((self.num_of_bots-1) * 1) + 4 + 1,
                      input_dims=3,
                      n_actions=3, mem_size=1000000, batch_size=16, epsilon_end=0.01)

        if not self.from_scratch:
            try:
                agent.load_model()
            except:
                print("No model, starting from scratch.")
        else:
            print("FROM SCRATCH!")

        scores = []
        eps_history = []

        # TODO: ogarnac coz to jest?
        # env = wrappers.Monitor(env, "tmp/lunar-lander-6",
        #                         video_callable=lambda episode_id: True, force=True)

        try:
            for i in range(n_games):
                done = False
                score = 0
                observation = env.reset()
                while not done:
                    action = agent.choose_action(observation)
                    observation_, reward, done, info = env.step(action)
                    score += reward
                    agent.remember(observation, action, reward, observation_, int(done))
                    observation = observation_
                    agent.learn()

                agent.epsilon_decay()
                eps_history.append(agent.epsilon)
                scores.append(score)

                avg_score = np.mean(scores[max(0, i - 100):(i + 1)])
                print('episode: ', i, 'score: %.2f' % score,
                      ' average score %.2f' % avg_score, 'epsilon %.3f' % agent.epsilon)

                if i % 10 == 0 and i > 0:
                    agent.save_model()

                    filename = f'plot-bot-{self.bot_num}.png'
                    x = [i + 1 for i in range(len(eps_history))]
                    plotLearning(x, scores, eps_history, filename)
        except KeyboardInterrupt:
            pass

        filename = f'plot-bot-{self.bot_num}.png'

        with open('scores.pkl', 'wb') as f:
            pickle.dump(scores, f)
        with open('eps_history.pkl', 'wb') as f:
            pickle.dump(eps_history, f)

        x = [i + 1 for i in range(len(eps_history))]
        plotLearning(x, scores, eps_history, filename)
