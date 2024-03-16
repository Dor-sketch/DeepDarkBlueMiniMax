"""
This file contains the classes for the game logic of the games StoneGame and TicTacToe
"""

from typing import List


class GameLogic:
    """
    GameLogic class
    """

    def __init__(self):
        self.state = []
        self.rules = ""
        self.player_score = 0
        self.computer_score = 0

    def actions(self, state: List[int]) -> List[int]:
        """
        Generates a list of possible actions based on the current state
        """
        pass

    def result(self, state: List[int], action: int) -> (List[int], int):
        """
        Returns the resulting state and the score gained by taking 'action' number of stones
        """
        pass

    def reset(self):
        self.state = []
        self.player_score = 0
        self.computer_score = 0

    def check_winner(self, state: List[int]) -> str:
        """
        Determines the winner of the game
        """
        pass

    def __str__(self):
        """
        return pretty print of the game state
        """
        ret = ""
        for i, s in enumerate(self.state):
            ret += str(s)
            if i % 3 == 2:
                ret += "\n"
            else:
                ret += " "
        return ret

    def __type__(self):
        """
        return the type of the game
        """
        pass
