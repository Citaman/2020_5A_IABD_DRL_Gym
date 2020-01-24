from collections import Counter
from random import random
from tensorflow.keras.utils import *
from brains import DQNBrain, ReinforceBrain
from contracts import Agent, GameState
import numpy as np


class ReinforceAgent(Agent):
    def __init__(self,
                 action_space_size: int,
                 alpha: float = 0.001,
                 gamma: float = 0.999,
                 epsilon: float = 0.1,
                 ):
        self.Q_policy_function = ReinforceBrain(output_dim=action_space_size, learning_rate=alpha,
                          hidden_layers_count=5,
                          neurons_per_hidden_layer=128)
        self.action_space_size = action_space_size
        self.alpha = alpha
        self.gamma = gamma
        self.action = []
        self.a = []
        self.r = 0.0
        self.state = []
        self.rewards = []
        self.log_probs = []
        self.probs = []


    def act(self, gs: GameState) -> int:
        available_actions = gs.get_available_actions(gs.get_active_player())

        state_vec = gs.get_vectorized_state()

        action_probs = self.Q_policy_function.predict(state_vec)

        chosen_action = np.random.choice(available_actions, p=action_probs,replace=True)

        self.state.append(state_vec)
        self.rewards.append(self.r)
        self.log_probs.append(np.log(action_probs))
        self.probs.append(action_probs)
        self.action.append(chosen_action)
        self.a.append(to_categorical(chosen_action, self.action_space_size))

        self.r = 0.0

        return chosen_action

    def observe(self, r: float, t: bool, player_index: int):
        if self.r is None:
            return

        self.r += r

        if t:
            self.rewards.append(self.r)

            discounted_rewards = self.compute_discounted_reward()
            policy_gradient = []

            for log_prob, Gt in zip(self.log_probs, discounted_rewards):
                policy_gradient.append(-log_prob * Gt)

            # print(Counter(self.action).most_common(5))
            self.Q_policy_function.train(self.state, self.a, policy_gradient)

            self.state = []
            self.rewards = []
            self.log_probs = []
            self.probs = []
            self.a = []
            self.action =[]
            self.r = 0.0

            # self.Q_policy_function.tensorboard_callback.on_train_end(None)

    def compute_discounted_reward(self):
        cumulative_reward = 0.0
        discounted_reward = np.zeros(len(self.rewards))

        for i in reversed(range(len(self.rewards))):
            cumulative_reward = self.rewards[i] + self.gamma * cumulative_reward
            discounted_reward[i] = cumulative_reward
        discounted_reward = np.flipud(discounted_reward)

        return discounted_reward
