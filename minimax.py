"""
This is a simple game of taking stones.
It is played between the player and the computer,
where the player and the computer take turns taking stones from a pile.
The player can take 1-3 stones from the pile and the computer uses
the minimax algorithm to determine the best move to make.
The game ends when there are no more stones in the pile and the player with the most stones wins.
The game is implemented using tkinter for the GUI and networkx for the minimax tree visualization.
"""
from math import inf
from typing import List
import networkx as nx


class Minimax:
    """
    Minimax class
    """

    def __init__(self, GameLogic):
        self.G = nx.DiGraph()
        self.game = GameLogic
        self.__dict__.update(GameLogic.__dict__)  # copy instance attributes
        self.__type__ = GameLogic.__type__
        self.check_winner = GameLogic.check_winner
        self.result = GameLogic.result
        self.actions = GameLogic.actions
        self.reset = GameLogic.reset
        self.utility = GameLogic.utility

    def play(self, state: List[int], max_depth: int = 20, player="max"):
        """
        Determines the winner of the game
        """
        self.state = state
        dif, _ = self.max_value(state, -float('inf'),
                                float('inf'), 0, tree_level=0)
        if dif > 0:
            return "Max"
        elif dif < 0:
            return "Min"
        else:
            return "Tie"

    def ply(self, state: List[int], player="max"):
        """
        Returns the computer's move based on the current state
        return computer optimal move
        crop state to max_depth
        """
        print(f'Current state: {state}')
        v, a = self.max_value(state, -inf, inf, 0, tree_level=0)
        return v, a

    def max_value(self, state: List[int], alpha: int, beta: int, dif: int, tree_level: int) -> (int, int):
        if len(state) == 0:
            self.G.nodes[str(tree_level) + str(tuple(state)) +
                         str(dif)]['value'] = dif
            return self.utility(state, dif), 0
        node_id = str(tree_level) + str(tuple(state)) + str(dif)
        if node_id not in self.G:
            self.G.add_node(node_id)
            self.G.nodes[node_id]['level'] = tree_level
            self.G.nodes[node_id]['state'] = state

        move = 0
        v = -inf
        for a in self.actions(state):
            newState, score = self.result(state, a)
            # Adjusted key to include newState and updated dif
            son_id = str(tree_level + 1) + \
                str(tuple(newState)) + str(dif + score)
            self.G.add_node(son_id)
            self.G.nodes[son_id]['level'] = tree_level + 1
            self.G.nodes[son_id]['state'] = newState
            self.G.add_edge(node_id, son_id)
            v2, a2 = self.min_value(
                newState, alpha, beta, dif + score, tree_level + 1)
            if v < v2:
                v = v2
                if a2 != 0:
                    move = a2
                else:
                    move = a
            alpha = max(alpha, v2)
            if beta <= v:
                self.G.nodes[son_id]['value'] = inf
                self.G.nodes[node_id]['state'] = state
                break
        self.G.nodes[node_id]['value'] = v
        self.G.nodes[node_id]['state'] = state
        return v, move

    def min_value(self, state: List[int], alpha: int, beta: int, dif: int, tree_level: int) -> (int, int):
        if len(state) == 0:
            self.G.nodes[str(tree_level) + str(tuple(state)) +
                         str(dif)]['value'] = dif
            return self.utility(state, dif), 0
        node_id = str(tree_level) + str(tuple(state)) + str(dif)
        if node_id not in self.G:
            self.G.add_node(node_id)
            self.G.nodes[node_id]['level'] = tree_level
            self.G.nodes[node_id]['state'] = state

        v = inf
        move = 0
        for a in self.actions(state):
            newState, score = self.result(state, a)
            # Adjusted key to include newState and updated dif
            # In your min_value method
            son_id = str(tree_level + 1) + \
                str(tuple(newState)) + str(dif - score)
            self.G.add_node(son_id)
            self.G.nodes[son_id]['level'] = tree_level + 1
            self.G.nodes[son_id]['state'] = newState

            self.G.add_edge(node_id, son_id)
            v2, a2 = self.max_value(
                newState, alpha, beta, dif - score, tree_level + 1)
            if v > v2:
                if a2 != 0:
                    move = a2
                else:
                    move = a
                v = v2
            beta = min(beta, v2)
            if v <= alpha:
                self.G.nodes[son_id]['value'] = -inf
                print(f'Pruning {son_id} with value {v2}')
                break
        # update node_id to be the return value
        self.G.nodes[node_id]['value'] = v
        self.G.nodes[node_id]['state'] = state
        return v, move
