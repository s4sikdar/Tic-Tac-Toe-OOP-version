import unittest
from unittest.mock import patch
import copy

from game_tracking_variables import GameVariables
from utils import checker_utilities
from print_methods import PrintFunctions 


class TestCheckerFns(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_game_var = GameVariables()
        self.print_fn_obj = PrintFunctions()

    def test_all_equal(self):
        board = copy.deepcopy(
            self.instance_game_var.instance_current_status_of_board_pieces[0]
        )
        self.assertTrue(checker_utilities.all_3_equal(board))
        board[1] = 1
        self.assertFalse(checker_utilities.all_3_equal(board))

    def test_three_in_a_row(self):
        board = copy.deepcopy(
            self.instance_game_var.instance_current_status_of_board_pieces
        )
        self.assertIsNone(checker_utilities.three_in_a_row(board))
        board[0] = [1,1,1]
        self.assertEqual(checker_utilities.three_in_a_row(board), 1)

    def test_three_in_a_column(self):
        board = copy.deepcopy(
            self.instance_game_var.instance_current_status_of_board_pieces
        )
        self.assertIsNone(checker_utilities.three_in_a_column(board))
        for row in board:
            row[0] = 1
        self.assertEqual(checker_utilities.three_in_a_column(board), 1)

    def test_diagonals(self):
        board = copy.deepcopy(
            self.instance_game_var.instance_current_status_of_board_pieces
        )
        self.assertIsNone(checker_utilities.diagonals(board))
        for index, row in enumerate(board):
            row[index] = 1
        self.assertEqual(checker_utilities.diagonals(board), 1)
        for index, row in enumerate(board):
            row[index] = 0
            row[(len(row)) - index - 1] = 1
        self.assertEqual(checker_utilities.diagonals(board), 1)

    def test_no_one_wins(self):
        board = copy.deepcopy(
            self.instance_game_var.instance_current_status_of_board_pieces
        )
        for index, row in enumerate(board):
            row[index] = 1
        self.assertTrue(checker_utilities.somebody_wins(board))
        for index, row in enumerate(board):
            row[index] = 0
        self.assertFalse(checker_utilities.somebody_wins(board))

    def test_all_filled_up(self):
        self.assertFalse(checker_utilities.all_filled_up(
            self.instance_game_var.instance_array_of_available_spots
        ))

if __name__ == '__main__':
    unittest.main()
