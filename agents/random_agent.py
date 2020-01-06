from contracts import Agent, GameState
import numpy as np


class RandomAgent(Agent):

    def act(self, gs: GameState) -> int:
        available_actions = gs.get_available_actions(0)
        return np.random.choice(available_actions)

    ''' 
       def act(self, gs: GameState) -> int:
            available_actions = gs.get_available_actions(gs.get_active_player())
            return np.random.choice(available_actions)
    '''
    def observe(self, r: float, t: bool, player_index: int):
        pass

