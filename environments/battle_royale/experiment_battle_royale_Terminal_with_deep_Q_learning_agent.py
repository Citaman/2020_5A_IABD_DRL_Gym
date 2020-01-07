from agents import DeepQLearningAgent, RandomAgent, TabQLearningAgent, DeepQLearningExperienceReplayAgent
from environments.battle_royale import BattleRoyalGameWorldTerminal, BattleRoyale
from runners import run_for_n_games_and_print_stats, run_step

if __name__ == "__main__":
    list_agent=[DeepQLearningAgent(action_space_size=48) if i <7  else TabQLearningAgent() for i in range(2)]
    for _ in range(1):
        gs = BattleRoyalGameWorldTerminal(0,numberofPlayer=2,list_agent = list_agent)
        gs.run()

    list_agent[0].epsilon = -1
    list_agent[1].epsilon = -1
    gs2 = BattleRoyale(numberofPlayer=2,list_agent=list_agent)
    gs2.run()


