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
        self.game_tree = GameTree()
        self.computer_player = MIN


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

    def get_ply_successors(self, state: List[int] = None, player=MIN, iterations: int = 4) -> (int, int):
        """
        Returns the computer's move based on the current state
        return computer optimal move
        crop state to max_depth
        """
        if state is None:
            state = self.game.state.copy()
        # check if the game is over
        if self.game.check_winner(state) in ["X", "O"]:
            return self.game.utility(state, 0), 0
        # if the game is not over, get the best move
        if sum(state) == 0:
            self.computer_player = MAX
        v, a = self.minimax_decision(
            state, self.computer_player, iterations=iterations)
        return v, a

    def minimax_decision(self, state: List[int], player: str, depth:int = None, iterations: int = 4) -> (int, int):
        """
        Returns the best move for the computer
        """
        if depth is None:
            # cals how many moves based on the state
            depth = 0
            for i in state:
                if i != 0:
                    depth += 1
            depth -= 1
        if player == MIN:
            v, a = self.max_value(state, -float('inf'),
                                  float('inf'), depth, iterations)
        else:
            v, a = self.min_value(state, -float('inf'),
                                  float('inf'), depth, iterations)
        return v, a

    def max_value(self, state: List[int], alpha: int, beta: int, depth: int, iterations: int = 4) -> (int, int):
        """
        Returns the maximum value and the action that leads to that value
        """
        ply = [depth, tuple(state), MAX]
        if self.game.is_terminal(state, MAX):
            utility = self.game.utility(state, MAX)
            self.game_tree.update_node_value(ply, utility)
            # -1 for no move
            return utility, None

        best_move = None
        v = -inf # initial value of max node
        for a in self.game.actions(state):
            # TODO: implemet killer move heuristic
            new_state = self.game.result(state, a)
            next_ply = [depth + 1, tuple(new_state), MIN]
            self.game_tree.add_node(next_ply)
            self.game_tree.add_edge(ply, next_ply)
            v2, a2 = self.min_value(
                new_state, alpha, beta, depth + 1, iterations - 1)
            if v <= v2:
                v = v2
                # should not get -1 as a move
                if a2 is not None:
                    best_move = a2
                else:
                    best_move = a
            alpha = max(alpha, v2)
            if beta <= v:
                # to later display the pruned nodes
                self.game_tree.update_node_value(next_ply, inf)
                break
        # updating best move and value wile backtracking
        self.game_tree.update_node_value(ply, v)
        self.game_tree.update_node_best_move(ply, best_move)
        return v, best_move

    def min_value(self, state: List[int], alpha: int, beta: int, depth: int, iterations: int = 4) -> (int, int):
        """
        Returns the minimum value and the action that leads to that value
        """
        v = inf
        best_move = None
        ply = [depth, tuple(state), MIN]

        if self.game.is_terminal(state, MIN):
            v = self.game.utility(state, MIN)
        else:
            for a in self.game.actions(state):
                new_state = self.game.result(state, a)
                # Adjusted key to include newState and updated dif
                next_ply = [depth + 1, tuple(new_state), MAX]
                self.game_tree.add_node(next_ply)
                self.game_tree.add_edge(ply, next_ply)
                v2, a2 = self.max_value(
                    new_state, alpha, beta, depth + 1, iterations-1)
                if v >= v2:
                    if a2 is not None:
                        best_move = a2
                    else:
                        best_move = a
                    v = v2
                beta = min(beta, v2)
                if v <= alpha:
                    # to later display the pruned nodes
                    # add to the tree dummy node with value -inf
                    self.game_tree.update_node_value(next_ply, -inf)
                    break
        # update node_id to be the return value
        self.game_tree.update_node_value(ply, v)
        self.game_tree.update_node_best_move(ply, best_move)
        return v, best_move


if __name__ == "__main__":
    # test why tic tac toe is not working
    game = TicTacToe()
    minimax = Minimax(game)

    minimax.play([0, 0, 0, 0, 0, 0, 0, 0, 0])
    minimax.game_tree.plot_mini_max_tree(label_type="state")