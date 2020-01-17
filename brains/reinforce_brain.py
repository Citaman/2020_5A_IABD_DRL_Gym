from datetime import datetime

from tensorflow.keras import Sequential
from tensorflow.keras.activations import linear, tanh,relu,softmax
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import mse
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow import math
from tensorflow.keras.callbacks import TensorBoard
import numpy as np


def build_ppo_loss(action_prob, reward):
    def ppo_loss(y_true, y_pred):
        return -math.log(action_prob)*reward

    return ppo_loss

class ReinforceBrain:
    def __init__(self,
                 output_dim: int,
                 learning_rate: float = 0.0001,
                 hidden_layers_count: int = 0,
                 neurons_per_hidden_layer: int = 0):
        self.model = Sequential()

        for i in range(hidden_layers_count):
            self.model.add(Dense(neurons_per_hidden_layer, activation=tanh))

        self.model.add(Dense(output_dim, activation=softmax, use_bias=False))
        self.model.compile(loss=mse, optimizer=Adam(lr=learning_rate))
        #log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        #self.tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)
        #self.model.summary()

    def predict(self, state: np.ndarray) -> np.ndarray:
        return self.model.predict(np.array((state,)))[0]

    def train(self, state: list, chosen_action_mask: np.ndarray, target: list):
        target_vec = np.array(chosen_action_mask) * np.array(target) + (1 - np.array(chosen_action_mask)) * self.model.predict(np.array(state))
        print(target_vec[-1],chosen_action_mask[-1])
        self.model.train_on_batch(np.array(state),np.array(target_vec))