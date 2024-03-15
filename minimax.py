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
from game import GameLogic
from game_tic_tac_toe import TicTacToe
from game_tree import GameTree

MAX = 1
MIN = -1

class Minimax:
    """
    Minimax class
    """

    def __init__(self, GameLogic):
        """
        Initializes the Minimax class
        """
        self.game = GameLogic
        self.game_tree = None

    def play(self, state: List[int], max_moves: int = 6, player="max"):
        """
        Determines the winner of the game
        """
        self.state = state
        self.game_tree = GameTree(state)
        dif, _ = self.max_value(state, -float('inf'),
                                float('inf'), 0, tree_level=0, max_moves=max_moves)
        if dif > 0:
            return "Max"
        elif dif < 0:
            return "Min"
        else:
            return "Tie"

    def ply(self, state: List[int] = None, player="max", max_moves: int = 8) -> (int, int):
        """
        Returns the computer's move based on the current state
        return computer optimal move
        crop state to max_depth
        """
        if state is None:
            state = self.game.state.copy()
        # check if the game is over

        # try to find best move in the stored tree first
        if self.game_tree is not None:
            # look for matching state in the tree where the state is the same and the player is -1
            for node in self.game_tree.G.nodes:
                if self.game_tree.G.nodes[node]['state'] == state and self.game_tree.G.nodes[node]['player'] == -1:
                    # return the best move
                    # get the action based on the node parent
                    action = list(self.game_tree.G.predecessors(node))[0]
                    # find the action based on difference between the states
                    action = [i for i in range(len(state)) if state[i] != self.game_tree.G.nodes[action]['state'][i]][0]
                    return self.game_tree.G.nodes[node]['value'], action

        self.game_tree = GameTree(state)
        if self.game.check_winner(state) in ["X", "O"]:
            print(
                f'game is already over, returning {self.game.utility(state, 0)} and 0')
            return self.game.utility(state, 0), 0
        if player == "max":
            v, a = self.max_value(state, -inf, inf, 0,
                                  tree_level=0, max_moves=max_moves)
        else:
            v, a = self.min_value(state, -inf, inf, 0,
                                  tree_level=0, max_moves=max_moves)
        print(f'returning {v} and {a} for player {player}')
        return v, a

    def max_value(self, state: List[int], alpha: int, beta: int, dif: int, tree_level: int, max_moves: int) -> (int, int):
        """
        Returns the maximum value and the action that leads to that value
        """

        packed_state = [tree_level, tuple(state), MAX]
        if self.game.is_terminal(state, MAX):
            print("hi")
            utility = self.game.utility(state, MAX)
            print(packed_state)
            self.game_tree.update_node_value(packed_state, utility)
            return utility, -1

        move = -1
        v = -inf
        for a in self.game.actions(state):
            new_state, score = self.game.result(state, a)
            packed_successor = [tree_level + 1, tuple(new_state), MIN]
            self.game_tree.add_node(packed_successor)
            self.game_tree.add_edge(packed_state, packed_successor)
            v2, a2 = self.min_value(
                new_state, alpha, beta, dif + score, tree_level + 1, max_moves - 1)
            if v < v2:
                v = v2
                if a2 != 0:
                    move = a2
                else:
                    move = a
            alpha = max(alpha, v2)
            if beta <= v:
                print("pruning")
                # to later display the pruned nodes
                self.game_tree.update_node_value(packed_successor, inf)
                break
        print("returning from max_value")
        # self.game_tree.update_node_value(packed_state, v)
        # self.game_tree.update_node_state(packed_state, state)
        return v, move

    def min_value(self, state: List[int], alpha: int, beta: int, dif: int, tree_level: int, max_moves: int) -> (int, int):
        """
        Returns the minimum value and the action that leads to that value
        """
        packed_state = [tree_level, tuple(state), MIN]
        if self.game.is_terminal(state, MIN):
            utility = self.game.utility(state, MIN)
            self.game_tree.update_node_value(packed_state, utility)
            return utility, -1

        v = inf
        move = -1
        for a in self.game.actions(state):
            new_state, score = self.game.result(state, a)
            # Adjusted key to include newState and updated dif
            packed_successor = [tree_level + 1, tuple(new_state), MAX]
            self.game_tree.add_node(packed_successor)
            self.game_tree.add_edge(packed_state, packed_successor)
            v2, a2 = self.max_value(
                new_state, alpha, beta, dif - score, tree_level + 1, max_moves-1)
            if v > v2:
                if a2 != 0:
                    move = a2
                else:
                    move = a
                v = v2
            beta = min(beta, v2)
            if v <= alpha:
                # to later display the pruned nodes
                self.game_tree.update_node_value(packed_successor, -inf)
                break
        # update node_id to be the return value
        # self.game_tree.update_node_value(packed_state, v)
        # self.game_tree.update_node_state(packed_state, state)
        return v, move


if __name__ == "__main__":
    # test why tic tac toe is not working
    game = TicTacToe()
    minimax = Minimax(game)

    minimax.play([0, 0, 0, 0, 0, 0, 0, 0, 0])
    minimax.game_tree.plot_mini_max_tree(label_type="state")