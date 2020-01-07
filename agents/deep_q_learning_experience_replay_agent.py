from tensorflow.python.keras.metrics import *
from tensorflow.python.keras.utils import *

from brains import DQNBrain
from contracts import Agent, GameState
from collections import deque

# si gs1 == gs2 => hash(gs1) == hash(gs2)
# si gs1 != gs2 => hash(gs1) != hash(gs2) || hash(gs1) == hash(gs2)


class DeepQLearningExperienceReplayAgent(Agent):
    def __init__(self,
                 action_space_size: int,
                 alpha: float = 0.01,
                 gamma: float = 0.999,
                 epsilon: float = 0.1,
                 ):
        self.Q = DQNBrain(output_dim=action_space_size, learning_rate=alpha,
                          hidden_layers_count=2,
                          neurons_per_hidden_layer=128)
        self.action_space_size = action_space_size
        self.s = None
        self.a = None
        self.r = None
        self.experience = deque(maxlen=20)
        self.gamma = gamma
        self.epsilon = epsilon

    def act(self, gs: GameState) -> int:
        gs_unique_id = gs.get_unique_id()
        available_actions = gs.get_available_actions(gs.get_active_player())

        state_vec = gs.get_vectorized_state()
        predicted_Q_values = self.Q.predict(state_vec)

        if np.random.random() <= self.epsilon:
            chosen_action = np.random.choice(available_actions)
        else:
            chosen_action = available_actions[int(np.argmax(predicted_Q_values[available_actions]))]

        if self.s is not None:
            target = self.r + self.gamma * max(predicted_Q_values[available_actions])
            self.Q.train(self.s, self.a, target)
            self.experience.append((self.s.copy(),self.a.copy(),self.r,state_vec.copy()))
        print("experience",len(self.experience))

        if len(self.experience) % 10 == 0:
            for el in self.experience :
                #print(np.argmax(el[1]),el[0][0:2],el[3][0:2])
                target = el[2] + self.gamma * el[1]
                self.Q.train(el[0], el[1], target)
        self.s = state_vec
        self.a = to_categorical(chosen_action, self.action_space_size)
        self.r = 0.0

        return chosen_action

    def observe(self, r: float, t: bool, player_index: int):
        if self.r is None:
            return

        self.r += r

        if t:
            target = self.r
            self.Q.train(self.s, self.a, target)
            self.s = None
            self.a = None
            self.r = None
