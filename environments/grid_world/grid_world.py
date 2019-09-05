import numpy as np
from typing import List
import os

from contracts import GameState


class GridWorldGameState(GameState):
    def __init__(self):
        self.world = np.array([
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 2, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 2, 1],
            [1, 1, 1, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 3, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ])  # 0 = Empty, 1 = Wall, 2 = Hole, 3 = Goal
        self.player_pos = np.array([1, 1])
        self.game_over = False
        self.scores = np.array([0], dtype=np.float)
        self.available_actions = [0, 1, 2, 3]  # Up Down Left Right
        self.remaining_actions = 50
        self.action_vector = {
            0: np.array([-1, 0]),
            1: np.array([1, 0]),
            2: np.array([0, -1]),
            3: np.array([0, 1]),
        }

    def player_count(self) -> int:
        return 1

    def is_game_over(self) -> bool:
        return self.game_over

    def get_active_player(self) -> int:
        return 0

    def clone(self) -> 'GameState':
        pass

    def step(self, player_index: int, action_index: int):
        assert (not self.game_over)
        assert (player_index == 0)
        assert (0 <= action_index <= 3)

        target_pos = self.player_pos + self.action_vector[action_index]
        assert (0 <= target_pos[0] < self.world.shape[0])
        assert (0 <= target_pos[1] < self.world.shape[1])

        target_type = self.world[target_pos[0], target_pos[1]]

        self.scores[player_index] += -0.01
        self.remaining_actions -= 1
        if target_type == 0:
            self.player_pos = target_pos
        elif target_type == 1:
            pass
        elif target_type == 2:
            self.game_over = True
            self.scores[player_index] += -1
            return
        elif target_type == 3:
            self.player_pos = target_pos
            self.game_over = True
            self.scores[player_index] += 1
            return

        if self.remaining_actions <= 0:
            self.game_over = True
            self.scores[player_index] += -1

    def get_scores(self) -> np.ndarray:
        return self.scores

    def get_available_actions(self, player_index: int) -> List[int]:
        return self.available_actions

    def __str__(self):
        str_acc = f"Game Over : {self.game_over}{os.linesep}"
        str_acc += f"Remaining Actions : {self.remaining_actions}{os.linesep}"
        str_acc += f"Scores : {self.scores}{os.linesep}"

        for i, line in enumerate(self.world):
            for j, cell_type in enumerate(line):
                if self.player_pos[0] == i and self.player_pos[1] == j:
                    str_acc += "X"
                else:
                    str_acc += f"{cell_type}"
            str_acc += f"{os.linesep}"

        return str_acc