from agents import DeepQLearningAgent, DoubleDeepQLearningAgent
from environments import GridWorldGameState
from runners import run_for_n_games_and_print_stats, run_step
import tensorflow as tf
if __name__ == "__main__":
    tf.compat.v1.disable_eager_execution()
    gs = GridWorldGameState()
    agent = DoubleDeepQLearningAgent(action_space_size=4)

    for i in range(500):
        print(i)
        run_for_n_games_and_print_stats([agent], gs, 100)
        while not gs.is_game_over():
            run_step([agent], gs)
            print(gs)
        print('------------')
        gs.__init__()


    gs = gs.clone()
    while not gs.is_game_over():
        run_step([agent], gs)
        print(gs)

    agent.epsilon = -1.0
    run_for_n_games_and_print_stats([agent], gs, 100)

    gs = gs.clone()
    while not gs.is_game_over():
        run_step([agent], gs)
        print(gs)
