from tensorflow.keras.utils import *
import numpy as np
from brains import DQNBrain
from contracts import Agent, GameState

class DoubleDeepQLearningAgent(Agent):
    def __init__(self,
                 action_space_size: int,
                 alpha: float = 0.05,
                 gamma: float = 0.999,
                 epsilon: float = 0.1,
                 ):
        self.Q_action = DQNBrain(output_dim=action_space_size, learning_rate=alpha,
                          hidden_layers_count=5,
                          neurons_per_hidden_layer=128)
        self.Q_evaluation = DQNBrain(output_dim=action_space_size, learning_rate=alpha,
                          hidden_layers_count=5,
                          neurons_per_hidden_layer=128)
        self.action_space_size = action_space_size
        self.s = None
        self.a = None
        self.r = None
        self.count_state = 1
        self.gamma = gamma
        self.epsilon = epsilon
        self.tau = 0.01

    def act(self, gs: GameState) -> int:
        available_actions = gs.get_available_actions(gs.get_active_player())

        state_vec = gs.get_vectorized_state()
        predicted_Q_values = self.Q_action.predict(state_vec)

        if np.random.random() <= self.epsilon:
            chosen_action = np.random.choice(available_actions)
        else:
            chosen_action = available_actions[int(np.argmax(predicted_Q_values[available_actions]))]

        if self.s is not None:
            target = self.r + self.gamma * predicted_Q_values[int(np.argmax(self.Q_evaluation.predict(self.s)))]
            self.Q_action.train(self.s, self.a, target)

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
