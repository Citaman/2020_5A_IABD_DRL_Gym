from datetime import datetime

from tensorflow.keras import Sequential
from tensorflow.keras.activations import linear, tanh
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import mse
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.keras.callbacks import TensorBoard
import numpy as np


class DDQNBrain:
    def __init__(self,
                 output_dim: int,
                 learning_rate: float = 0.0001,
                 hidden_layers_count: int = 0,
                 neurons_per_hidden_layer: int = 0):
        self.model = Sequential()

        for i in range(hidden_layers_count):
            self.model.add(Dense(neurons_per_hidden_layer, activation=tanh))

        self.model.add(Dense(output_dim,activation=linear, use_bias=False))
        self.model.compile(loss=mse, optimizer=Adam(lr=learning_rate))
        log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        self.tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)
        #self.model.summary()

    def predict(self, state: np.ndarray) -> np.ndarray:
        return self.model.predict(np.array((state,)))[0]

    def train(self, state: np.ndarray, chosen_action_mask: np.ndarray, target: float):
        target_vec = chosen_action_mask* target + (1 - chosen_action_mask) * self.predict(state)
        # print(state,target_vec)
        # target_vec = np.array(chosen_action_mask) * np.array(target) + ( 1 - np.array(chosen_action_mask)) * self.model.predict(np.array(state))
        self.model.train_on_batch(x=np.array((state,)),y=np.array((target_vec,)))

    def retrain(self, state: np.ndarray, chosen_action_mask: np.ndarray, target: float):
        #target_vec = np.array(chosen_action_mask) * np.array(target) + ( 1 - np.array(chosen_action_mask)) * self.model.predict(np.array(state))

        part_1 = np.array([el*np.array(target)[i] for i, el in enumerate(np.array(chosen_action_mask))])
        target_vec = part_1 +(1 - np.array(chosen_action_mask)) * self.model.predict(np.array(state))
        self.model.train_on_batch(x=np.array(state), y=np.array(target_vec))