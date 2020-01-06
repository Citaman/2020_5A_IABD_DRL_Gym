from agents import RandomRolloutAgent
from environments import GridWorldGameState
from runners import run_to_the_end

if __name__ == "__main__":
    gs = GridWorldGameState()
    agent = RandomRolloutAgent(1000, True)

    print(gs)
    run_to_the_end([agent], gs)
    print(gs)