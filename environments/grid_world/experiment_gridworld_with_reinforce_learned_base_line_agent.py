from agents import ReinforceLearnedBaseLineCriticAgent
from environments import GridWorldGameState
from runners import run_for_n_games_and_print_stats, run_step

if __name__ == "__main__":
    gs = GridWorldGameState()
    agent = ReinforceLearnedBaseLineCriticAgent(action_space_size=4)

    for i in range(100):
        run_for_n_games_and_print_stats([agent], gs, 100)
        while not gs.is_game_over():
            run_step([agent], gs)
            print(gs)
            try:
                print(agent.probs[-1])
                print(agent.value_baseline[-1])
            except:
                print('FINI')
        gs.__init__()

    run_for_n_games_and_print_stats([agent], gs, 100)

    gs = gs.clone()
    while not gs.is_game_over():
        run_step([agent], gs)
        print(gs)
