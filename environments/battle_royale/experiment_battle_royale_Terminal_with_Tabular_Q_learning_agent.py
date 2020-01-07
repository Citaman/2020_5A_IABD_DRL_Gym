from agents import DeepQLearningAgent, RandomAgent ,TabQLearningAgent
from environments.battle_royale import BattleRoyalGameWorldTerminal, BattleRoyale
from runners import run_for_n_games_and_print_stats, run_step

if __name__ == "__main__":
    list_agent=[TabQLearningAgent() if i <7  else RandomAgent() for i in range(6)]
    for _ in range(100):
        gs = BattleRoyalGameWorldTerminal(0, list_agent=list_agent)
        gs.run()

    list_agent[0].epsilon =-1
    list_agent[1].epsilon = -1
    gs2 = BattleRoyale(list_agent=list_agent)
    gs2.run()


