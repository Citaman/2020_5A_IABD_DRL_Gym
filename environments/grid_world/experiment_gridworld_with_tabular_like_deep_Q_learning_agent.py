from agents import TabularLikeDeepQLearningAgent
from environments import GridWorldGameState
from runners import run_for_n_games_and_print_stats, run_step

if __name__ == "__main__":
    gs = GridWorldGameState()
    agent = TabularLikeDeepQLearningAgent(action_space_size=4)

    for i in range(500):
        run_for_n_games_and_print_stats([agent], gs, 1)

    agent.epsilon = -1.0
    run_for_n_games_and_print_stats([agent], gs, 100)

    gs = gs.clone()
    while not gs.is_game_over():
        run_step([agent], gs)
        print(gs)
