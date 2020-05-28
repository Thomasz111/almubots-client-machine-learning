from dqn import Agent
import numpy as np
import gym
from dqn_utils import plotLearning
from almubots_env import AlmubotsEnv


class Dqn:

    def __init__(self, num_of_bots: int, bot_num: int, from_scratch: bool):
        self.num_of_bots = num_of_bots
        self.bot_num = bot_num
        self.from_scratch = from_scratch

    def run(self):
        env = AlmubotsEnv(num_of_bots=self.num_of_bots, bot_num=self.bot_num)
        # lr = 0.0005
        lr = 0.002
        n_games = 500
        agent = Agent(gamma=0.999, epsilon=1.0, epsilon_dec=0.9995, alpha=lr,
                      input_dims=self.num_of_bots * 2 + ((self.num_of_bots-1) * 1) + 4 + 1,
                      n_actions=14, mem_size=1000000, batch_size=64, epsilon_end=0.01)

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

                eps_history.append(agent.epsilon)
                scores.append(score)
                #
                # print("###########################################################################################")
                # print("###########################################################################################")
                # print("###########################################################################################")
                # print("###########################################################################################")
                # print("###########################################################################################")
                # print("###########################################################################################")
                # print("###########################################################################################")
                # print("###########################################################################################")
                # print("###########################################################################################")
                # print("###########################################################################################")
                # print("###########################################################################################")
                # print("###########################################################################################")
                # print("###########################################################################################")
                # print("###########################################################################################")

                avg_score = np.mean(scores[max(0, i - 100):(i + 1)])
                print('episode: ', i, 'score: %.2f' % score,
                      ' average score %.2f' % avg_score)

                if i % 10 == 0 and i > 0:
                    agent.save_model()
        except KeyboardInterrupt:
            pass

        filename = f'plot-bot-{self.bot_num}.png'

        x = [i + 1 for i in range(len(eps_history))]
        plotLearning(x, scores, eps_history, filename)
