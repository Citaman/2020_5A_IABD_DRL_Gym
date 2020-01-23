from agents import DeepQLearningAgent, RandomAgent, TabQLearningAgent, DeepQLearningExperienceReplayAgent, PPOAgent, \
    ReinforceAgent, ReinforceMeanBaseLineAgent
from environments.battle_royale import BattleRoyalGameWorldTerminal, BattleRoyale
from runners import run_for_n_games_and_print_stats, run_step
import tensorflow as tf
import random
if __name__ == "__main__":
    tf.compat.v1.disable_eager_execution()
    action_space_size = 48
    number_of_player = 6
    state_space_size = 22
    list_agent=[ReinforceMeanBaseLineAgent(action_space_size=action_space_size) if i <1  else RandomAgent() for i in range(number_of_player)]
    for i in range(300):
        #random.shuffle(list_agent)
        #print(list_agent)
        gs = BattleRoyalGameWorldTerminal(i,numberofPlayer=number_of_player,list_agent = list_agent)
        gs.run()

    #list_agent[0].epsilon = -1
    #list_agent[1].epsilon = -1
    gs2 = BattleRoyale(numberofPlayer=number_of_player,list_agent=list_agent)
    gs2.run()


