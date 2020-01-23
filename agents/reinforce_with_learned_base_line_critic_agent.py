from collections import Counter

from tensorflow.keras.metrics import *
from tensorflow.keras.utils import *
from brains import DQNBrain, ReinforceBrain, ReinforceBaseLineCriticBrain
from contracts import Agent, GameState

import tensorflow.keras.backend as K

import numpy as np

import tensorflow as tf

class ReinforceLearnedBaseLineCriticAgent(Agent):
    def __init__(self,
                 action_space_size: int,
                 alpha: float = 0.001,
                 gamma: float = 0.999,
                 epsilon: float = 0.1,
                 ):
        self.Q_policy_function = ReinforceBrain(output_dim=action_space_size, learning_rate=alpha,
                          hidden_layers_count=5,
                          neurons_per_hidden_layer=128)
        self.Q_critic = ReinforceBaseLineCriticBrain(output_dim=1, learning_rate=alpha,
                          hidden_layers_count=5,
                          neurons_per_hidden_layer=128)
        self.action_space_size = action_space_size
        self.alpha = alpha
        self.gamma = gamma
        #self.s = None
        self.action = []
        self.a = []
        self.r = 0.0
        self.state = []
        self.rewards = []
        self.log_probs = []
        self.probs = []
        self.value_baseline = []



    def act(self, gs: GameState) -> int:
        available_actions = gs.get_available_actions(gs.get_active_player())

        state_vec = gs.get_vectorized_state()
        #print(state_vec)

        action_probs = self.Q_policy_function.predict(state_vec)
        value_basline = self.Q_critic.predict(state_vec)
        # print(action_probs)

        chosen_action = np.random.choice(available_actions, p=action_probs,replace=True)


        self.state.append(state_vec)
        self.rewards.append(self.r)
        self.value_baseline.append(value_basline)
        self.probs.append(action_probs)
        self.log_probs.append(np.log(action_probs))
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
            #print("r=",self.r)
            #target = self.r
            discounted_rewards = self.compute_discounted_reward()
            policy_gradient = []
            value_gradient = []
            # Base line calcule
            # eps = 0.02
            # discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + eps)

            for log_prob, Gt,v_baseline in zip(self.log_probs, discounted_rewards,self.value_baseline):
                Gt_star = Gt - v_baseline
                policy_gradient.append(-log_prob * Gt_star)
                value_gradient.append(-v_baseline * Gt_star)

            #sum = float(np.sum(np.concatenate(policy_gradient)))
            # print(Counter(self.action).most_common(5))
            self.Q_policy_function.train(self.state, self.a, policy_gradient)
            self.Q_critic.train(self.state,value_gradient)
            #weight = np.array(self.Q_policy_function.model.get_weights())
            #print(weight)
            #self.Q_policy_function.model.set_weights(weight + sum)
            self.state = []
            self.rewards = []
            self.log_probs = []
            self.probs = []
            self.a = []
            self.action =[]
            self.r = 0.0
            #self.Q_policy_function.tensorboard_callback.on_train_end(None)

    def compute_discounted_reward(self):
        cumulative_reward = 0.0
        discounted_reward = np.zeros(len(self.rewards))
        for i in reversed(range(len(self.rewards))):
            # print("reward ",i,self.rewards[i] ,"gamma", self.gamma ,"cumulative_reward",cumulative_reward)
            cumulative_reward = self.rewards[i] + cumulative_reward * self.gamma
            discounted_reward[i] = cumulative_reward

        discounted_reward = np.flipud(discounted_reward)

        return discounted_reward
