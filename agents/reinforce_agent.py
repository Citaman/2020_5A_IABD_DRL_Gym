from collections import Counter

from tensorflow.keras.metrics import *
from tensorflow.keras.utils import *
from brains import DQNBrain, ReinforceBrain
from contracts import Agent, GameState

import tensorflow.keras.backend as K

import numpy as np

import tensorflow as tf



# si gs1 == gs2 => hash(gs1) == hash(gs2)
# si gs1 != gs2 => hash(gs1) != hash(gs2) || hash(gs1) == hash(gs2)


class ReinforceAgent(Agent):
    def __init__(self,
                 action_space_size: int,
                 alpha: float = 0.05,
                 gamma: float = 0.999,
                 epsilon: float = 0.1,
                 ):
        self.Q_policy_function = ReinforceBrain(output_dim=action_space_size, learning_rate=alpha,
                          hidden_layers_count=0,
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



    def act(self, gs: GameState) -> int:
        available_actions = gs.get_available_actions(gs.get_active_player())

        # self.rewards.append(self.r)
        # print('reward',len(self.rewards))

        state_vec = gs.get_vectorized_state()

        action_probs = self.Q_policy_function.predict(state_vec)
        #print(max(action_probs))
        chosen_action = np.random.choice(available_actions, p=action_probs)

        self.state.append(state_vec)
        self.rewards.append(self.r)
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

            #target = self.r
            discounted_rewards = self.compute_gains_and_advantages()
            policy_gradient = []
            for log_prob, Gt in zip(self.log_probs, discounted_rewards):
                policy_gradient.append(-log_prob * Gt)
                #print("log_prob",log_prob,"Gt",Gt,"-log_prob * Gt",-log_prob * Gt )
            #print(policy_gradient)
            #print(self.s)
            sum = float(np.sum(np.concatenate(policy_gradient)))

            #print('action',self.a)
            print(Counter(self.action).most_common(5))
            self.Q_policy_function.train(self.state, self.a, policy_gradient)
            weight = np.array(self.Q_policy_function.model.get_weights())
            #print(weight[-1][-1][:])
            #self.Q_policy_function.model.set_weights(weight + sum)
            self.state = []
            self.rewards = []
            self.log_probs = []
            self.a = []
            self.action =[]
            self.r = 0.0

    def compute_gains_and_advantages(self):
        cumulative_reward = 0.0
        discounted_reward = np.zeros(len(self.rewards))
        for i in reversed(range(len(self.rewards))):
            # print("reward ",i,self.rewards[i] ,"gamma", self.gamma ,"cumulative_reward",cumulative_reward)
            cumulative_reward = self.rewards[i] + self.gamma * cumulative_reward
            discounted_reward[i] = cumulative_reward
        eps = 0.2
        discounted_reward = (discounted_reward - discounted_reward.mean()) / (discounted_reward.std() + eps)

        return discounted_reward
