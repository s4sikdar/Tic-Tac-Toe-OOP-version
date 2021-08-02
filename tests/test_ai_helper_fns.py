from logging import BufferingFormatter
import unittest
from unittest.mock import patch, Mock
import copy

from utils import checker_utils
from artificial_intelligence import TheAIProgram
from game_tracking_variables import GameVariables


class TestAI(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_game_vars = GameVariables()
        self.instance_ai_prog = TheAIProgram()
        self.directions = {
            'horizontal': True,
            'vertical': True,
            'diagonal_1': True,
            'diagonal_2': True
        }

    def clean_mock_side_effect(self):
        """
            Used to "clean" the directions dictionary for when we wish to use it the next
            time.
        """
        for direc in self.instance_ai_prog.instance_directions:
            self.instance_ai_prog.instance_directions[direc] = True

    def test_all_the_same_values(self):
        self.assertTrue(self.instance_ai_prog.all_the_same_values(1, [1, 1, 1]))

    def test_all_the_same_values_false(self):
        self.assertFalse(self.instance_ai_prog.all_the_same_values(1, [1, 1, 0]))

    def test_three_in_a_row_case_1(self):
        board = copy.deepcopy(
            self.instance_game_vars.instance_current_status_of_board_pieces
        )
        for index, row in enumerate(board):
            row[index] = 1
        # [
        #  [1, 0, 0]
        #  [0, 1, 0]
        #  [0, 0, 1]
        # ]
        # Now we have the above, and make sure that we get the same resullt at all coordinates
        # Better to hardcode this than use a for loop.
        self.assertTrue(self.instance_ai_prog.three_in_a_row_at_this_spot(1, board, [0, 0]))
        self.assertTrue(self.instance_ai_prog.three_in_a_row_at_this_spot(1, board, [2, 2]))

    def test_three_in_a_row_case_2(self):
        board = copy.deepcopy(
            self.instance_game_vars.instance_current_status_of_board_pieces
        )
        for index, row in enumerate(board):
            row[2 - index] = 1
        # [
        #  [0, 0, 1]
        #  [0, 1, 0]
        #  [1, 0, 0]
        # ]
        # Now we have the above, and make sure that we get the same resullt at all coordinates
        self.assertTrue(self.instance_ai_prog.three_in_a_row_at_this_spot(1, board, [0, 2]))
        self.assertTrue(self.instance_ai_prog.three_in_a_row_at_this_spot(1, board, [2, 0]))

    def test_three_in_a_row_case_3(self):
        board = copy.deepcopy(
            self.instance_game_vars.instance_current_status_of_board_pieces
        )
        board[0] = [1] * 3
        # [
        #  [1, 1, 1]
        #  [0, 0, 0]
        #  [0, 0, 0]
        # ]
        # Now we have the above.
        self.assertTrue(self.instance_ai_prog.three_in_a_row_at_this_spot(1, board, [0, 1]))
        board[0] = [0] * 3
        for row in board:
            row[1] = 1
        # [
        #  [0, 1, 0]
        #  [0, 1, 0]
        #  [0, 1, 0]
        # ]
        # Now we have the above. This should cover the remaining positiions of 3 in a row
        # where the coordinates are in [[0, 1], [1, 0], [1, 2], [2, 1]]
        self.assertTrue(self.instance_ai_prog.three_in_a_row_at_this_spot(1, board, [0, 1]))

    def test_three_in_a_row_case_4(self):
        board = copy.deepcopy(
            self.instance_game_vars.instance_current_status_of_board_pieces
        )
        for row in board:
            row[1] = 1
        self.assertTrue(self.instance_ai_prog.three_in_a_row_at_this_spot(1, board, [1, 1]))
        for row in board:
            row[1] = 0
        board[1] = [1] * 3
        self.assertTrue(self.instance_ai_prog.three_in_a_row_at_this_spot(1, board, [1, 1]))
        board[1] = [0] * 3
        for index, row in enumerate(board):
            row[index] = 1
        self.assertTrue(self.instance_ai_prog.three_in_a_row_at_this_spot(1, board, [1, 1]))

    def test_blocked_row_of_2(self):
        row = [1, 1, 2]
        self.assertTrue(self.instance_ai_prog.blocked_row_of_2(2, 1, row))
        row[0] = 0
        self.assertFalse(self.instance_ai_prog.blocked_row_of_2(2, 1, row))

    def test_block_case_1(self):
        board = copy.deepcopy(
            self.instance_game_vars.instance_current_status_of_board_pieces
        )
        board[0][0] = 1
        board[1][1] = 1
        board[2][2] = 2
        # [
        #  [1, 0, 0],
        #  [0, 1, 0],
        #  [0, 0, 2]
        # ]
        # What we have for the board
        self.assertTrue(self.instance_ai_prog.block([0, 0], board, 2, 1))
        self.assertTrue(self.instance_ai_prog.block([2, 2], board, 2, 1))
        board[1][1] = 0
        self.assertFalse(self.instance_ai_prog.block([0, 0], board, 2, 1))
        self.assertFalse(self.instance_ai_prog.block([2, 2], board, 2, 1))

    def test_block_case_2(self):
        board = copy.deepcopy(
            self.instance_game_vars.instance_current_status_of_board_pieces
        )
        board[2][0] = 1
        board[1][1] = 1
        board[0][2] = 2
        # [
        #  [0, 0, 1],
        #  [0, 1, 0],
        #  [2, 0, 0]
        # ]
        # What we have for the board
        self.assertTrue(self.instance_ai_prog.block([2, 0], board, 2, 1))
        self.assertTrue(self.instance_ai_prog.block([0, 2], board, 2, 1))
        board[1][1] = 0
        self.assertFalse(self.instance_ai_prog.block([2, 0], board, 2, 1))
        self.assertFalse(self.instance_ai_prog.block([0, 2], board, 2, 1))

    def test_block_case_3(self):
        board = copy.deepcopy(
            self.instance_game_vars.instance_current_status_of_board_pieces
        )
        board[2][0] = 1
        board[1][1] = 2
        board[0][2] = 1
        self.assertTrue(self.instance_ai_prog.block([1, 1], board, 2, 1))
        board[2][0] = 0
        board[0][2] = 0
        board[1] = [1, 2, 1]
        self.assertTrue(self.instance_ai_prog.block([1, 1], board, 2, 1))
        board[1] = [0, 2, 0]
        board[0][1] = 1
        board[2][1] = 1
        self.assertTrue(self.instance_ai_prog.block([1, 1], board, 2, 1))
        board[1][1] = 0
        self.assertFalse(self.instance_ai_prog.block([1, 1], board, 2, 1))

    def test_block_case_4(self):
        board = copy.deepcopy(
            self.instance_game_vars.instance_current_status_of_board_pieces
        )
        board[0] = [1, 2, 1]
        self.assertTrue(self.instance_ai_prog.block([0, 1], board, 2, 1))
        board[0] = [0, 2, 0]
        board[1][1] = 1
        board[2][1] = 1
        self.assertTrue(self.instance_ai_prog.block([0, 1], board, 2, 1))
        board[1][1] = 0
        self.assertFalse(self.instance_ai_prog.block([0, 1], board, 2, 1))

    def test_two_in_a_row(self):
        row = [1, 1, 0]
        self.assertTrue(self.instance_ai_prog.two_in_a_row(1, row))
        row[1] = 0
        self.assertFalse(self.instance_ai_prog.two_in_a_row(1, row))

    def test_fork_helper_case_1(self):
        board = copy.deepcopy(
            self.instance_game_vars.instance_current_status_of_board_pieces
        )
        for index, row in enumerate(board):
            row[index] = 1 if index in [0, 1] else 0
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [0, 0], board, self.directions),
            [[0,0], [1,1], [2,2]]
        )
        board[1][1] = 0
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [0, 0], board, self.directions),
            []
        )

    def test_fork_helper_case_2(self):
        board = copy.deepcopy(
            self.instance_game_vars.instance_current_status_of_board_pieces
        )
        for index, row in enumerate(board):
            row[2 - index] = 1 if index in [0, 1] else 0
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [0,2], board, self.directions),
            [[0, 2], [1, 1], [2, 0]]
        )
        board[1][1] = 0
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [0,2], board, self.directions),
            []
        )

    def test_fork_helper_case_3(self):
        board = copy.deepcopy(
            self.instance_game_vars.instance_current_status_of_board_pieces
        )
        directions = copy.deepcopy(self.directions)
        directions['diagonal_2'] = False
        for index, row in enumerate(board):
            row[2 - index] = 1 if index in [0, 1] else 0
        # First test that if the diagonal direction is turned off when you have 2 in a row 
        # diagonally, an empty list is returned because you weren't allowed to seach diagonally
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [1,1], board, directions),
            []
        )
        directions['diagonal_2'] = True
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [1,1], board, directions),
            [[0, 2], [1, 1], [2, 0]]
        )
        for index, row in enumerate(board):
            row[index] = 1 if index in [0, 1] else 0
            row[2 - index] = 0 if index in [0, 2] else 1
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [1,1], board, directions),
            [[0, 0], [1, 1], [2, 2]]
        )
        board[1][1] = 0
        directions['diagonal_1'] = False
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [1,1], board, directions),
            []
        )

    def test_fork_helper_case_4(self):
        board = copy.deepcopy(
            self.instance_game_vars.instance_current_status_of_board_pieces
        )
        directions = copy.deepcopy(self.directions)
        board[0] = [1, 1, 0]
        directions['horizontal'] = False
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [0, 1], board, directions),
            []
        )
        directions['horizontal'] = True
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [0, 1], board, directions),
            [[0, 0], [0, 1], [0, 2]]
        )
        board[0][0] = 0
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [0, 1], board, directions),
            []
        )
        board[1][1] = 1
        directions['vertical'] = False
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [0, 1], board, directions),
            []
        )
        directions['vertical'] = True
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [0, 1], board, directions),
            [[0, 1], [1, 1], [2, 1]]
        )

    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_fork_case_1(self, clean_mock):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        clean_mock.side_effect = self.clean_mock_side_effect
        board[0] = [1, 0, 1]
        board[1][1] = 1
        self.assertTrue(self.instance_ai_prog.fork([0, 0], board, 1))
        self.assertTrue(self.instance_ai_prog.fork([1, 1], board, 1))
        self.assertTrue(self.instance_ai_prog.fork([0, 2], board, 1))
        board[0][2] = 0
        self.assertFalse(self.instance_ai_prog.fork([0, 0], board, 1))
        self.assertEqual(clean_mock.call_count, 4)

    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_fork_case_2(self, clean_mock):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        clean_mock.side_effect = self.clean_mock_side_effect
        board[0] = [1, 1, 0]
        board[1][1] = 1
        self.assertTrue(self.instance_ai_prog.fork([0, 0], board, 1))
        self.assertTrue(self.instance_ai_prog.fork([1, 1], board, 1))
        board[1][1] = 0
        self.assertFalse(self.instance_ai_prog.fork([0, 0], board, 1))
        self.assertEqual(clean_mock.call_count, 3)

    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_fork_case_3(self, clean_mock):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        clean_mock.side_effect = self.clean_mock_side_effect
        board[0] = [1, 0, 1]
        board[2][0] = 1
        self.assertTrue(self.instance_ai_prog.fork([0, 2], board, 1))
        self.assertTrue(self.instance_ai_prog.fork([2, 0], board, 1))
        board[2][0] = 0
        self.assertFalse(self.instance_ai_prog.fork([0, 0], board, 1))
        self.assertEqual(clean_mock.call_count, 3)

    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_fork_case_4(self, clean_mock):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        clean_mock.side_effect = self.clean_mock_side_effect
        board[0] = [1, 1, 0]
        board[2][1] = 1
        self.assertTrue(self.instance_ai_prog.fork([0, 0], board, 1))
        self.assertTrue(self.instance_ai_prog.fork([2, 1], board, 1))
        board[2][1] = 0
        self.assertFalse(self.instance_ai_prog.fork([0, 1], board, 1))
        self.assertEqual(clean_mock.call_count, 3)

    def test_opposite_corner_case_1(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        board[0][0] = 2
        self.assertTrue(self.instance_ai_prog.opposite_corner([2, 2], board, 2))
        board[0][0] = 0
        self.assertFalse(self.instance_ai_prog.opposite_corner([2, 2], board, 2))

    def test_opposite_corner_case_2(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        board[0][2] = 2
        self.assertTrue(self.instance_ai_prog.opposite_corner([2, 0], board, 2))
        board[0][2] = 0
        self.assertFalse(self.instance_ai_prog.opposite_corner([2, 0], board, 2))

    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_fork_for_them(self, clean_mock):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        # 2 is the number representing the other player, 1 is the number representing us.
        board[0] = [2, 0, 1]
        board[2][2] = 2
        self.assertTrue(self.instance_ai_prog.fork_for_them([0, 2], board, 1, 2))
        board[2][2] = 0
        self.assertFalse(self.instance_ai_prog.fork_for_them([0, 2], board, 1, 2))
        self.assertEqual(clean_mock.call_count, 2)

    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_fork_for_them_not_true(self, clean_mock):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        # 2 is the number representing the other player, 1 is the number representing us.
        # As the inside fork function has been tested, I don't need to test all the cases where
        # you could have a fork, as I am then just testing all the cases of the fork function
        # again. Best not to test the same thing twice, as now it falls a little more into
        # regression tests.
        board[0] = [1, 0, 1]
        board[1][1] = 1
        self.assertFalse(self.instance_ai_prog.fork_for_them([1, 1], board, 1, 2))
        clean_mock.assert_called_once()

    # Both tests break
    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_static_evaluation_win(self, clean_mock):
        # 4 cases of winning: one horizontal, one vertical, and both diagonals.
        # We don't need to test for them all, because we have tested this through
        # the test_three_in_a_row_case_{case number} test cases near the start. We
        # just need to test one. 
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        board[0] = [1, 1, 1]
        self.assertEqual(self.instance_ai_prog.static_evaluation([0, 0], board, 1, 2), [[0, 0], 9])
        self.assertEqual(clean_mock.call_count, 2)

    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_static_evaluation_block(self, clean_mock):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        board[0][1] = 1
        board[1][1] = 2
        board[2][1] = 1
        self.assertEqual(self.instance_ai_prog.static_evaluation([1, 1], board, 2, 1), [[1, 1], 8])
        self.assertEqual(clean_mock.call_count, 2)

    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_static_evaluation_fork(self, clean_mock):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        board[0] = [1, 0, 1]
        board[2][2] = 1
        self.assertEqual(self.instance_ai_prog.static_evaluation([0, 2], board, 1, 2), [[0, 2], 7])
        self.assertEqual(clean_mock.call_count, 2)

    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_static_evaluation_fork_for_them(self, clean_mock):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        board[0] = [2, 0, 1]
        board[2][2] = 2
        self.assertEqual(self.instance_ai_prog.static_evaluation([0, 2], board, 1, 2), [[0, 2], 5])
        self.assertEqual(clean_mock.call_count, 2)

    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_center(self, clean_mock):
        board = self.instance_game_vars.instance_current_status_of_board_pieces
        self.assertEqual(self.instance_ai_prog.static_evaluation([1, 1], board, 1, 2), [[1,1], 4])
        self.assertEqual(clean_mock.call_count, 1)

    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_fork_opposite(self, clean_mock):
        board = copy.deepcopy(
            self.instance_game_vars.instance_current_status_of_board_pieces
        )
        board[0][0] = 1
        board[2][2] = 2
        self.assertEqual(self.instance_ai_prog.static_evaluation([0, 0], board, 1, 2), [[0, 0], 3])
        self.assertEqual(clean_mock.call_count, 2)

    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_corner(self, clean_mock):
        board = self.instance_game_vars.instance_current_status_of_board_pieces
        self.assertEqual(self.instance_ai_prog.static_evaluation([0, 0], board, 1, 2), [[0, 0], 2])
        self.assertEqual(self.instance_ai_prog.static_evaluation([0, 2], board, 1, 2), [[0, 2], 2])
        self.assertEqual(self.instance_ai_prog.static_evaluation([2, 2], board, 1, 2), [[2, 2], 2])
        self.assertEqual(self.instance_ai_prog.static_evaluation([2, 0], board, 1, 2), [[2, 0], 2])
        self.assertEqual(clean_mock.call_count, 4)

    @patch('artificial_intelligence.TheAIProgram.clean')
    def test_normal_case(self, clean_mock):
        board = self.instance_game_vars.instance_current_status_of_board_pieces
        self.assertEqual(self.instance_ai_prog.static_evaluation([0, 1], board, 1, 2), [[0, 1], 1])
        self.assertEqual(clean_mock.call_count, 1)

    def test_no_wins_false(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        board[0] = [1, 1, 1]
        self.assertEqual(self.instance_ai_prog.no_wins(board), [False, 1])

    def test_no_wins_true(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        self.assertEqual(self.instance_ai_prog.no_wins(board), [True, 0])

    def test_find_optimal_move_special_case(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        board[0][0] = 1
        board[1][1] = 2
        board[2][2] = 1
        self.instance_ai_prog.instance_player_spots[1] = [[0, 0], [2, 2]]
        self.instance_ai_prog.instance_player_spots[2] = [[1, 1]]
        self.assertEqual(self.instance_ai_prog.find_optimal_move(board, 2, 1, [[0, 2], [2, 0]]), [[1, 0], 6])
        self.instance_ai_prog.instance_player_spots[1] = []
        self.instance_ai_prog.instance_player_spots[2] = []

    def test_find_optimal_move_one_fork(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        board[0][0] = 1
        board[2][0] = 2
        board[2][1] = 1
        self.instance_ai_prog.instance_player_spots[1] = [[0, 0], [2, 1]]
        self.instance_ai_prog.instance_player_spots[2] = [[2, 0]]
        self.assertEqual(self.instance_ai_prog.find_optimal_move(board, 2, 1, [[0, 1]]), [[0, 1], 5])
        self.instance_ai_prog.instance_player_spots[1] = []
        self.instance_ai_prog.instance_player_spots[2] = []

    def test_find_optimal_move_multiple_forks(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        board[0][0] = 1
        board[1][1] = 1
        board[2][2] = 2
        forks = [[0, 1], [0, 2], [1, 0], [2, 0]]
        self.instance_ai_prog.instance_player_spots[1] = [[0, 0], [1, 1]]
        self.instance_ai_prog.instance_player_spots[2] = [[2, 2]]
        self.assertEqual(self.instance_ai_prog.find_optimal_move(board, 2, 1, forks), [[2, 0], 6])
        self.instance_ai_prog.instance_player_spots[1] = []
        self.instance_ai_prog.instance_player_spots[2] = []

    def test_find_optimal_move_failed_case(self):
        # This is a case that failed earlier.
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        board[1] = [1, 1, 2]
        board[0][0] = 2
        board[2][2] = 1
        forks = [[2, 0], [2, 1]]
        self.instance_ai_prog.instance_player_spots[1] = [[1, 0], [1, 1], [2, 2]]
        self.instance_ai_prog.instance_player_spots[2] = [[0, 0], [1, 2]]
        self.assertEqual(self.instance_ai_prog.find_optimal_move(board, 2, 1, forks), [[0, 1], 6])
        self.instance_ai_prog.instance_player_spots[1] = []
        self.instance_ai_prog.instance_player_spots[2] = []

if __name__ == '__main__':
    unittest.main()
