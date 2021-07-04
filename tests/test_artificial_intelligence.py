import unittest
import copy

from utils import checker_utils
from artificial_intelligence import TheAIProgram
from game_tracking_variables import GameVariables


class TestAI(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_game_vars = GameVariables()
        self.instance_ai_prog = TheAIProgram()

    def test_all_the_same_values(self):
        board =  copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        board[0] = [1, 1, 1]
        self.assertTrue(self.instance_ai_prog.all_the_same_values(1, board))

    def test_all_the_same_values_false(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        board[0] = [1, 1, 0]
        self.assertFalse(self.instance_ai_prog.all_the_same_values(1, board))


if __name__ == '__main__':
    unittest.main()
