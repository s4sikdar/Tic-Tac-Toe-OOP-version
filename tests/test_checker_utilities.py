import unittest
import copy

from game_tracking_variables import GameVariables
from utils import checker_utils
from print_methods import PrintFunctions 


class TestCheckerFns(unittest.TestCase):
    """
        Used to test all the checker function utilities.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_game_var = GameVariables()
        self.print_fn_obj = PrintFunctions()

    def test_all_equal(self):
        board = copy.deepcopy(
            self.instance_game_var.instance_current_status_of_board_pieces[0]
        )
        self.assertTrue(checker_utils.all_3_equal(board))
        board[1] = 1
        self.assertFalse(checker_utils.all_3_equal(board))

    def test_three_in_a_row(self):
        board = copy.deepcopy(
            self.instance_game_var.instance_current_status_of_board_pieces
        )
        self.assertIsNone(checker_utils.three_in_a_row(board))
        board[0] = [1,1,1]
        self.assertEqual(checker_utils.three_in_a_row(board), 1)

    def test_three_in_a_column(self):
        board = copy.deepcopy(
            self.instance_game_var.instance_current_status_of_board_pieces
        )
        self.assertIsNone(checker_utils.three_in_a_column(board))
        for row in board:
            row[0] = 1
        self.assertEqual(checker_utils.three_in_a_column(board), 1)

    def test_diagonals(self):
        board = copy.deepcopy(
            self.instance_game_var.instance_current_status_of_board_pieces
        )
        self.assertIsNone(checker_utils.diagonals(board))
        for index, row in enumerate(board):
            row[index] = 1
        self.assertEqual(checker_utils.diagonals(board), 1)
        for index, row in enumerate(board):
            row[index] = 0
            row[(len(row)) - index - 1] = 1
        self.assertEqual(checker_utils.diagonals(board), 1)

    def test_somebody_wins(self):
        board = copy.deepcopy(
            self.instance_game_var.instance_current_status_of_board_pieces
        )
        second_board = copy.deepcopy(board)
        for index, row in enumerate(board):
            row[index] = 1
            second_board[index][index] = 2
        self.assertEqual(checker_utils.somebody_wins(board), 1)
        self.assertEqual(checker_utils.somebody_wins(second_board), 2)
        for index, row in enumerate(board):
            row[index] = 0
        self.assertIsNone(checker_utils.somebody_wins(board))

    def test_all_filled_up_false(self):
        self.assertFalse(checker_utils.all_filled_up(
            self.instance_game_var.instance_array_of_available_spots
        ))

    def test_all_filled_up_true(self):
        board = copy.deepcopy(
            self.instance_game_var.instance_array_of_available_spots
        )
        for row in board:
            for counter in enumerate(row):
                row[counter[0]] = False
        self.assertTrue(checker_utils.all_filled_up(board))


if __name__ == '__main__':
    unittest.main()
