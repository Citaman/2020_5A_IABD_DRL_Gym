from random import shuffle
from typing import List
import numpy as np

from contracts import Agent, GameState


def run_step(agents: List[Agent], gs: GameState):
    assert (not gs.is_game_over())
    active_player_index = gs.get_active_player()

    old_scores = gs.get_scores().copy()
    action = agents[active_player_index].act(gs)
    gs.step(active_player_index, action)
    new_scores = gs.get_scores()
    rewards = new_scores - old_scores
    for i, agent in enumerate(agents):
        agent.observe(rewards[i], gs.is_game_over(), i)


def run_to_the_end(agents: List[Agent], gs: GameState):
    while not gs.is_game_over():
        run_step(agents, gs)


def run_for_n_games_and_return_stats(agents: List[Agent], gs: GameState, games_count: int,
                                     shuffle_players: bool = False) -> (np.ndarray, np.ndarray):
    total_scores = np.zeros_like(gs.get_scores())
    agents_order = np.arange(len(agents))

    agents_copy = agents
    if shuffle_players:
        agents_copy = agents.copy()
    for _ in range(games_count):
        gs_copy = gs.clone()
        if shuffle_players:
            agents_copy = agents.copy()
            shuffle(agents_order)
            for i in agents_order:
                agents_copy[i] = agents[agents_order[i]]
        run_to_the_end(agents_copy, gs_copy)
        total_scores += gs_copy.get_scores()[agents_order]

    return total_scores, total_scores / games_count


def run_for_n_games_and_print_stats(agents: List[Agent], gs: GameState, games_count: int,
                                    shuffle_players:bool = False):
    total_scores, mean_scores = run_for_n_games_and_return_stats(agents, gs, games_count,
                                                                 shuffle_players=shuffle_players)

    print(f"Total Scores : {total_scores}")
    print(f"Mean Scores : {mean_scores}")


def run_for_n_games_and_return_max(agents: List[Agent], gs: GameState, games_count: int) -> np.ndarray:
    old_and_new_scores = np.ones((2, len(gs.get_scores()))) * -9999.9

    for _ in range(games_count):
        gs_copy = gs.clone()
        run_to_the_end(agents, gs_copy)
        new_scores = gs_copy.get_scores()
        old_and_new_scores[1, :] = new_scores
        old_and_new_scores[0, :] = np.max(old_and_new_scores, axis=0)

    return old_and_new_scores[0, :]
