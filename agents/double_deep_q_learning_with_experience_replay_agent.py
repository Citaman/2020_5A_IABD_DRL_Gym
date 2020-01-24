from tensorflow.keras.utils import *

from brains import DQNBrain, DDQNBrain
from contracts import Agent, GameState
from collections import deque
from random import sample
import numpy as np

class DoubleDeepQLearningExprerienceReplayAgent(Agent):
    def __init__(self,
                 action_space_size: int,
                 alpha: float = 0.05,
                 gamma: float = 0.999,
                 epsilon: float = 0.1,
                 ):
        self.Q_action = DDQNBrain(output_dim=action_space_size, learning_rate=alpha,
                          hidden_layers_count=5,
                          neurons_per_hidden_layer=128)
        self.Q_evaluation = DDQNBrain(output_dim=action_space_size, learning_rate=alpha,
                          hidden_layers_count=5,
                          neurons_per_hidden_layer=128)
        self.action_space_size = action_space_size
        self.s = None
        self.a = None
        self.r = None
        self.count_state = 1
        self.experience = deque(maxlen=1000)
        self.gamma = gamma
        self.epsilon = epsilon
        self.tau = 0.01

    def act(self, gs: GameState) -> int:
        gs_unique_id = gs.get_unique_id()
        available_actions = gs.get_available_actions(gs.get_active_player())

        state_vec = gs.get_vectorized_state()
        predicted_Q_values = self.Q_action.predict(state_vec)
        #print(predicted_Q_values.round(1))
        if np.random.random() <= self.epsilon:
            chosen_action = np.random.choice(available_actions)
        else:
            chosen_action = available_actions[int(np.argmax(predicted_Q_values[available_actions]))]

        if self.s is not None:
            target = self.r + self.gamma * predicted_Q_values[int(np.argmax(self.Q_evaluation.predict(self.s)))]
            # print('target',target,"state",self.s,predicted_Q_values[int(np.argmax(self.Q_evaluation.predict(self.s)))],np.argmax(self.Q_evaluation.predict(self.s)),self.Q_evaluation.predict(self.s))
            self.Q_action.train(self.s, self.a, target)
            self.experience.append((self.s.copy(), self.a.copy(), self.r, state_vec.copy()))

        #print(len(self.experience))
        if len(self.experience) % 10 == 0 and len (self.experience) > 0 and self.epsilon > 0 :
            #print('here')
            el = sample(self.experience,len(self.experience) if len(self.experience)<30 else 30)
            dict = {'Exp':el}
            el_state = [x[0] for x in dict['Exp']]
            el_a = [x[1] for x in dict['Exp']]
            el_r = [x[2] for x in dict['Exp']]
            el_state_plus_1 = [x[3] for x in dict['Exp']]
            #print(el_a)
            predicted_Q_values_list = self.Q_action.model.predict(np.array(el_state_plus_1))
            # print(np.round(predicted_Q_values_list,2))
            dict_predict_Q_value = {'Predict':predicted_Q_values_list}
            Q_star = [x[int(np.argmax(self.Q_evaluation.predict(el_state[i])))] for i, x in enumerate(dict_predict_Q_value['Predict'])]
            Q_star_np = np.array(Q_star)
            target = np.array(el_r) + self.gamma * Q_star_np
            #print(np.array(el_state).shape,np.array(el_a).shape,np.array(target).shape)

            self.Q_action.retrain(np.array(el_state), np.array(el_a), target)
            #for el in sample(self.experience,len(self.experience) if len(self.experience)<500 else  500) :
                #print(np.argmax(el[1]),el[0][0:2],el[3][0:2])
                #target = el[2] + self.gamma * el[1]
                #self.Q_action.train(el[0], el[1], target)

        # if self.count_state %10 == 0:
        # self.Q_evaluation.model.set_weights(self.Q_action.model.get_weights())
        if self.s is not None:
            update_Q_evaluation = self.tau * np.array(self.Q_action.model.get_weights()) + (1 - self.tau) * np.array(self.Q_evaluation.model.get_weights())
            self.Q_evaluation.model.set_weights(update_Q_evaluation)
        self.s = state_vec
        self.a = to_categorical(chosen_action, self.action_space_size)
        self.r = 0.0
        self.count_state += 1

        return chosen_action

    def observe(self, r: float, t: bool, player_index: int):
        if self.r is None:
            return

        self.r += r

        if t:
            target = self.r
            self.Q_action.train(self.s, self.a, target)
            self.s = None
            self.a = None
            self.r = None
