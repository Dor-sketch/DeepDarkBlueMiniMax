"""
StoneGame class is a subclass of GameLogic class.
This is a simple game of taking stones, played between the player and the computer.
The player and the computer take turns taking stones from a pile.
In each turn, the player can take 1-3 stones from the pile and the computer uses
the minimax algorithm to determine the best move to make.
Unlike simpler versions of the game, the winner is the player holding
the most stones value at the end of the game.
"""

from typing import List
import random
from game import GameLogic


class StoneGame(GameLogic):
    """
    StoneGame class
    """

    def __init__(self):
        super().__init__()
        self.rules = "The game starts with a pile of stones. Players take turns taking 1, 2, or 3 stones from the pile. The player who takes the last stone loses."
        self.state = [random.randint(0, 10)
                      for _ in range(random.randint(14, 17))]

    def actions(self, state: List[int]) -> List[int]:
        """
        Generates a list of possible actions based on the current state
        """
        return [i for i in range(1, min(3, len(state)) + 1)]

    def result(self, state: List[int], action: int) -> (List[int], int):
        """
        Returns the resulting state and the score gained by taking 'action' number of stones
        """
        score = sum(state[:action])
        return state[action:], score

    def utility(self, state: List[int], player: int) -> int:
        """
        Determines the utility of the current state
        """
        # TODO: complete this function. utility should be 1 if difference in score is positive, -1 if negative, 0 if tie
        return 0

    def reset(self):
        """
        Resets the game state
        """
        super().reset()
        self.state = [i for i in range(15)]

    def check_winner(self, state: List[int]) -> str:
        """
        Determines the winner of the game
        """
        if len(state) == 0:
            if self.player_score > self.computer_score:
                return "Player"
            elif self.player_score < self.computer_score:
                return "Computer"
            else:
                return "Tie"
        return "No winner yet"

    def __type__(self):
        return "StoneGame"
