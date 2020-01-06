from agents import RandomAgent,TabQLearningAgent
from environments.battle_royale import BattleRoyale
from runners import run_for_n_games_and_print_stats, run_step

if __name__ == "__main__":
    list_agent = list([TabQLearningAgent() for i in range(6)])
    gs = BattleRoyale(list_agent=list_agent)
    gs.run()
    

