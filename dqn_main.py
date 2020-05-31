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

        # self.q_eval_angle = build_dqn(alpha, n_actions=3, input_dims=3, fc1_dims=256, fc2_dims=256) # obserwacje: x, y, kat lufy nasz
        # akcje: lufa w lewo, lufa w prawo, nic
        # self.q_eval_shoot = build_dqn(alpha, n_actions=2, input_dims=3, fc1_dims=64, fc2_dims=64)   # obserwacje: x, y, kat lufy nasz
        # akcje: strzel, nic
        # self.q_eval_move =  build_dqn(alpha, n_actions=9, input_dims=1, fc1_dims=256, fc2_dims=256) # obserwacje: kat lufy przeciwnika
        # akcje: gora, dol, lewo, prawo, ukos, ukos, ukos, ukos, nic


        agent_angle = Agent(gamma=0.99, epsilon=1.0, epsilon_dec=0.99, alpha=lr,
                      # input_dims=self.num_of_bots * 2 + ((self.num_of_bots-1) * 1) + 4 + 1,
                      input_dims=3, fname='dqn_angle_model.h5',
                      n_actions=3, mem_size=1000000, batch_size=16, epsilon_end=0.01)
        agent_shoot = Agent(gamma=0.99, epsilon=1.0, epsilon_dec=0.99, alpha=lr,
                      input_dims=3, fname='dqn_shoot_model.h5',
                      n_actions=2, mem_size=1000000, batch_size=16, epsilon_end=0.01)
        agent_move = Agent(gamma=0.99, epsilon=1.0, epsilon_dec=0.99, alpha=lr,
                      input_dims=1, fname='dqn_move_model.h5',
                      n_actions=9, mem_size=1000000, batch_size=16, epsilon_end=0.01)

        if not self.from_scratch:
            try:
                agent_angle.load_model()
            except:
                print("No model, starting from scratch.")
        else:
            print("FROM SCRATCH!")

        scores1 = []
        scores = []
        scores2 = []
        scores3 = []
        eps_history1 = []
        eps_history2 = []
        eps_history3 = []
        eps_history = []

        # TODO: ogarnac coz to jest?
        # env = wrappers.Monitor(env, "tmp/lunar-lander-6",
        #                         video_callable=lambda episode_id: True, force=True)

        try:
            for i in range(n_games):
                done = False
                score = (0, 0, 0)
                observation = env.reset()
                while not done:
                    x,y,angl_my, angl_enemy = observation

                    action_angle = agent_angle.choose_action(np.array([x,y,angl_my]))
                    action_shoot = agent_shoot.choose_action(np.array([x,y,angl_my]))
                    action_move = agent_move.choose_action(np.array([angl_enemy]))
                    observation_, reward, done, info = env.step(action_shoot * 27 + action_angle * 9 + action_move)
                    score = (score[0] + reward[0], score[1] + reward[1], score[2] + reward[2])

                    x_,y_,angl_my_, angl_enemy_ = observation_

                    agent_angle.remember(np.array([x,y,angl_my]), action_angle, reward[0], np.array([x_,y_,angl_my_]), int(done))
                    agent_shoot.remember(np.array([x,y,angl_my]), action_shoot, reward[1], np.array([x_,y_,angl_my_]), int(done))
                    agent_move.remember(np.array([angl_enemy]), action_move, reward[2], np.array([angl_enemy_]), int(done))
                    observation = observation_
                    agent_angle.learn()
                    agent_shoot.learn()
                    agent_move.learn()

                agent_angle.epsilon_decay()
                agent_shoot.epsilon_decay()
                agent_move.epsilon_decay()
                eps_history.append(agent_angle.epsilon)
                scores1.append(score[0])
                scores2.append(score[1])
                scores3.append(score[2])

                avg_score1 = np.mean(scores1[max(0, i - 100):(i + 1)])
                avg_score2 = np.mean(scores2[max(0, i - 100):(i + 1)])
                avg_score3 = np.mean(scores3[max(0, i - 100):(i + 1)])

                avg_score = (avg_score1, avg_score2, avg_score3)

                print('episode: ', i, 'score_angle: %.2f score_shoot: %.2f score_move %.2f' % score,
                      ' average score \t%.2f \t%.2f \t%.2f' % avg_score, 'epsilon %.3f' % agent_angle.epsilon)
                                                         # 'angle_epsilon %.3f shoot_espilon %.3f, move_epsilon %.3f' % (agent_angle.epsilon, agent_shoot.epsilon, agent_move.epsilon))

                if i % 10 == 0 and i > 0:
                    agent_angle.save_model()
                    agent_shoot.save_model()
                    agent_move.save_model()

                    filename = f'plot-bot-{self.bot_num}.png'
                    x = [i + 1 for i in range(len(eps_history))]
                    plotLearning(x, (scores1, scores2, scores3), eps_history, filename)
        except KeyboardInterrupt:
            pass

        filename = f'plot-bot-{self.bot_num}.png'

        with open('scores.pkl', 'wb') as f:
            pickle.dump(scores, f)
        with open('eps_history.pkl', 'wb') as f:
            pickle.dump(eps_history, f)

        x = [i + 1 for i in range(len(eps_history))]
        plotLearning(x, scores, eps_history, filename)
