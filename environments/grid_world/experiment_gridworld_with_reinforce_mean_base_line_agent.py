from agents import ReinforceMeanBaseLineAgent
from environments import GridWorldGameState
from runners import run_for_n_games_and_print_stats, run_step
import tensorflow as tf
if __name__ == "__main__":
    tf.compat.v1.disable_eager_execution()
    gs = GridWorldGameState()
    agent = ReinforceMeanBaseLineAgent(action_space_size=4)

    for i in range(100):
        run_for_n_games_and_print_stats([agent], gs, 1000)
        while not gs.is_game_over():
            run_step([agent], gs)
            print(gs)
            try:
                print(agent.probs[-1])
            except:
                print('FINI')
        gs.__init__()

    run_for_n_games_and_print_stats([agent], gs, 100)

    gs = gs.clone()
    while not gs.is_game_over():
        run_step([agent], gs)
        print(gs)
