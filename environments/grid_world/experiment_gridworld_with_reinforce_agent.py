from agents import ReinforceAgent
from environments import GridWorldGameState
from runners import run_for_n_games_and_print_stats, run_step

if __name__ == "__main__":
    gs = GridWorldGameState()
    agent = ReinforceAgent(action_space_size=4)

    for i in range(10):
        print(i)
        run_for_n_games_and_print_stats([agent], gs, 50)
        while not gs.is_game_over():
            run_step([agent], gs)
            print(gs)
            try:
                print(agent.probs[-1])
            except:
                print('FINI')
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


