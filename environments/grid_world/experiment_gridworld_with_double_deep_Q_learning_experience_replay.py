from agents import  DoubleDeepQLearningExprerienceReplayAgent
from environments import GridWorldGameState
from runners import run_for_n_games_and_print_stats, run_step
import tensorflow as tf

if __name__ == "__main__":
    tf.compat.v1.disable_eager_execution()
    gs = GridWorldGameState()
    agent = DoubleDeepQLearningExprerienceReplayAgent(action_space_size=4)

    for i in range(100):
        print(i)
        run_for_n_games_and_print_stats([agent], gs, 100)
        if i % 10 == 0:
            while not gs.is_game_over():
                run_step([agent], gs)
                try:
                    print(agent.probs[-1])
                except:
                    pass
                print(gs)
        gs.__init__()

    for i in range(5):
        gs = gs.clone()
        gs.__init__()
        while not gs.is_game_over():
            run_step([agent], gs)
            print(gs)
        gs.__init__()

    agent.epsilon = -1.0
    run_for_n_games_and_print_stats([agent], gs, 100)


