from agents import RandomRolloutAgent, MOMCTSAgent, RandomAgent, HalfAlphaZeroAgent
from environments.tictactoe import TicTacToeGameState
from runners import run_to_the_end, run_for_n_games_and_print_stats

if __name__ == "__main__":

    import tensorflow as tf

    tf.compat.v1.disable_eager_execution()

    gs = TicTacToeGameState()
    agent0 = HalfAlphaZeroAgent(10, gs.get_action_space_size(), keep_memory=True)
    agent1 = RandomAgent()

    for _ in range(1000):
        run_for_n_games_and_print_stats([agent0, agent1], gs, 100, shuffle_players=True)
