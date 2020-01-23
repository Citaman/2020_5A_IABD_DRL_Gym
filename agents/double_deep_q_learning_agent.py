from tensorflow.python.keras.metrics import *
from tensorflow.python.keras.utils import *

from brains import DQNBrain
from contracts import Agent, GameState


# si gs1 == gs2 => hash(gs1) == hash(gs2)
# si gs1 != gs2 => hash(gs1) != hash(gs2) || hash(gs1) == hash(gs2)


class DoubleDeepQLearningAgent(Agent):
    def __init__(self,
                 action_space_size: int,
                 alpha: float = 0.05,
                 gamma: float = 0.999,
                 epsilon: float = 0.1,
                 ):
        self.Q_action = DQNBrain(output_dim=action_space_size, learning_rate=alpha,
                          hidden_layers_count=2,
                          neurons_per_hidden_layer=128)
        self.Q_evaluation = DQNBrain(output_dim=1, learning_rate=alpha,
                          hidden_layers_count=2,
                          neurons_per_hidden_layer=128)
        self.action_space_size = action_space_size
        self.s = None
        self.a = None
        self.r = None
        self.count_state = 1
        self.gamma = gamma
        self.epsilon = epsilon

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
            target = self.r + self.gamma * self.Q_evaluation.predict(state_vec)
            #print('target',target,"state",self.s)
            self.Q_action.train(self.s, self.a, target)

        if self.count_state%10 == 0:
            self.Q_evaluation.model.set_weights(self.Q_action.model.get_weights())

        self.s = state_vec
        self.a = to_categorical(chosen_action, self.action_space_size)
        self.r = 0.0
        self.count_state+=1

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
