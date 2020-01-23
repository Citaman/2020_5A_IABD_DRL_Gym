from datetime import datetime

from tensorflow.keras import Sequential
from tensorflow.keras.activations import linear, tanh,relu,softmax
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import mse
from tensorflow.keras.optimizers import SGD, Adam
import tensorflow as tf
from tensorflow import math
from tensorflow.keras.callbacks import TensorBoard
import numpy as np


def build_ppo_loss(action_prob, reward):
    def ppo_loss(y_true, y_pred):
        return -math.log(action_prob)*reward

    return ppo_loss

class ReinforceBaseLineCriticBrain:
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
        log_dir = "../../logs/Reinforce/MODELE-MLP__" + datetime.now().strftime("%Y%m%d-%H%M%S")
        self.tensorboard_callback = TensorBoard(log_dir=log_dir,histogram_freq=0,batch_size=440, write_graph=True,write_grads=True)
        self.tensorboard_callback.set_model(self.model)
        self.batch_id = 0
        self.writer = tf.summary.create_file_writer(log_dir)
        #self.model.summary()

    def predict(self, state: np.ndarray) -> np.ndarray:
        return self.model.predict(np.array((state,)))[0]

    def named_logs(self, logs):
        result = {}
        for l in zip(self.model.metrics_names, logs):
            result[l[0]] = l[1]
        return result

    @tf.function
    def write_tensorboard_file(self,step,logs):
        with self.writer.as_default():
            tf.summary.scalar("loss", logs, step=step)

    def train(self, state: list, chosen_action_mask: np.ndarray, target: list):
        target_vec = np.array(chosen_action_mask) * np.array(target) + (1 - np.array(chosen_action_mask)) * self.model.predict(np.array(state))
        #print(target_vec[-1],chosen_action_mask[-1])
        logs = self.model.train_on_batch(np.array(state),np.array(target_vec))
        print(logs)
        self.write_tensorboard_file(self.batch_id,logs)
        #self.tensorboard_callback.on_epoch_end(self.batch_id, self.named_logs([logs]))
        self.batch_id +=1
        self.writer.flush()