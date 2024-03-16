"""
This module contains the Minimax class which is used to determine the winner of the game
by using the minimax algorithm.
"""
from math import inf
from typing import List
from game_tic_tac_toe import TicTacToe
from game_tree import GameTree

MAX = 1
MIN = -1


def build_tree(func):
    """
    Decorator function to build the game tree
    """
    def wrapper(self, state, alpha, beta, depth, iterations):
        player = MIN
        if depth % 2 == 0:
            player = MAX
        parent = [depth - 1, state, player]  # parent node
        childs = [self.game.result(state, a) for a in self.game.actions(state)]
        for child in childs:
            self.game_tree.add_node([depth + 1, child, -player])
            self.game_tree.add_edge(parent, [depth + 1, child, -player])
            if self.game.is_terminal(child):
                self.game_tree.update_node_value(
                    [depth + 1, child, -player], self.game.utility(child))

        return func(self, state, alpha, beta, depth, iterations)
    return wrapper


class Minimax:
    """
    Minimax class
    """

    def __init__(self, game_logic: TicTacToe):
        """
        Initializes the Minimax class
        """
        self.game = game_logic
        self.game_tree = GameTree()

    def play(self, state: List[int], iterations: int = 4, player="max"):
        """
        Determines the winner of the game
        """
        self.state = state
        self.game_tree = GameTree(state)
        dif, _ = self.max_value(state, -float('inf'),
                                float('inf'), depth=0, iterations=iterations)
        if dif > 0:
            return "Max"
        elif dif < 0:
            return "Min"
        else:
            return "Tie"

    def minimax_move(self, state: List[int], player: str = None, depth: int = 0, iterations: int = 10) -> (int, int):
        """
        Returns the best move for the computer
        """
        cur_depth = 0
        for cell in state:
            if cell != 0:
                cur_depth += 1
        if cur_depth % 2 == 0:
            # max player
            _, move = self.max_value(
                state, -float('inf'), float('inf'), depth, iterations)
        else:
            # min player
            _, move = self.min_value(
                state, -float('inf'), float('inf'), depth, iterations)
        return move

    @build_tree
    def max_value(self, state: List[int], alpha: int, beta: int, depth: int, iterations: int = 10) -> (int, int):
        """
        Returns the maximum value and the action that leads to that value
        """
        if self.game.is_terminal(state):
            utility = self.game.utility(state)
            return utility, None

        best_move = None
        v = -inf  # initial value of max node
        for a in self.game.actions(state):
            # TODO: implemet killer move heuristic
            new_state = self.game.result(state, a)
            v2, _ = self.min_value(
                new_state, alpha, beta, depth + 1, iterations - 1)
            if v <= v2:
                v = v2
                best_move = a
            alpha = max(alpha, v2)
            if beta <= v:
                break
        # updating best move and value wile backtracking
        return v, best_move

    @build_tree
    def min_value(self, state: List[int], alpha: int, beta: int, depth: int, iterations: int = 10) -> (int, int):
        """
        Returns the minimum value and the action that leads to that value
        """
        v = inf
        best_move = None
        if self.game.is_terminal(state, MIN):
            v = self.game.utility(state, MIN)
        else:
            for a in self.game.actions(state):
                new_state = self.game.result(state, a)
                v2, a2 = self.max_value(
                    new_state, alpha, beta, depth + 1, iterations-1)
                if v2 < v:
                    best_move = a
                    v = v2
                beta = min(beta, v2)
                if v <= alpha:
                    break
        return v, best_move
