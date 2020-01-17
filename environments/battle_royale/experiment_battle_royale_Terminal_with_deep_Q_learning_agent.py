import random

from agents import DeepQLearningAgent, RandomAgent, TabQLearningAgent, DeepQLearningExperienceReplayAgent
from environments.battle_royale import BattleRoyalGameWorldTerminal, BattleRoyale
from runners import run_for_n_games_and_print_stats, run_step
import tensorflow as tf
if __name__ == "__main__":
    tf.compat.v1.disable_eager_execution()
    list_agent=[DeepQLearningAgent(action_space_size=48) if i <1  else RandomAgent() for i in range(6)]
    for i in range(100):
        random.shuffle(list_agent)
        gs = BattleRoyalGameWorldTerminal(i,numberofPlayer=6,list_agent = list_agent)
        gs.run()

    #list_agent[0].epsilon = -1
    #list_agent[1].epsilon = -1
    gs2 = BattleRoyale(numberofPlayer=6,list_agent=list_agent)
    gs2.run()


