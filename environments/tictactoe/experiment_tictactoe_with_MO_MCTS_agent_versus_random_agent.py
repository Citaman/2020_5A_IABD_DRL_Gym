from agents import RandomRolloutAgent, MOMCTSAgent, RandomAgent
from environments.tictactoe import TicTacToeGameState
from runners import run_to_the_end, run_for_n_games_and_print_stats

if __name__ == "__main__":
    gs = TicTacToeGameState()
    agent0 = MOMCTSAgent(100)
    agent1 = RandomAgent()

    run_for_n_games_and_print_stats([agent0, agent1], gs, 100)
