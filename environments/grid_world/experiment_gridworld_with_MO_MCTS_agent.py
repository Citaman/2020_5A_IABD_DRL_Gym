from agents import MOMCTSAgent
from environments import GridWorldGameState
from runners import run_for_n_games_and_print_stats

if __name__ == "__main__":
    gs = GridWorldGameState()
    agent = MOMCTSAgent(100)

    for _ in range(1000):
        run_for_n_games_and_print_stats([agent], gs, 1)
