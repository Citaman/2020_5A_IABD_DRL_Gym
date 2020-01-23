from agents import RandomAgent, PPOAgent
from environments import GridWorldGameState
from runners import run_to_the_end, run_for_n_games_and_print_stats, run_step
import tensorflow as tf

if __name__ == "__main__":
    tf.compat.v1.disable_eager_execution()
    gs = GridWorldGameState()
    agent = PPOAgent(
        state_space_size=gs.get_vectorized_state().shape[0],
        action_space_size=gs.get_action_space_size())
    for i in range(20):
        print(i)
        run_for_n_games_and_print_stats([agent], gs, 300)
        while not gs.is_game_over():
            run_step([agent], gs)
            print(gs)

        gs.__init__()
    print(gs)
    run_to_the_end([agent], gs)
    print(gs)