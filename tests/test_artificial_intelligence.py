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
        self.directions = {
            'horizontal': True,
            'vertical': True,
            'diagonal': True
        }

    # def clean(self):
    #     """
    #         Used to "clean" the directions dictionary for when we wish to use it the next
    #         time.
    #     """
    #     for direc in self.directions:
    #         self.directions[direc] = True

    # def clean_at_end_decorator(func):
    #     """
    #         Used to make sure that the clean method cleans our directions dictionary after
    #         functions are run, by using this function as a decorator. Only use this for
    #         functions that use self.directions.
    #     """
    #     def decorated_func(self, *args, **kwargs):
    #         return_val = func(self, *args, **kwargs)
    #         self.clean()
    #         return return_val
    #     return decorated_func

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
        directions['diagonal'] = False
        for index, row in enumerate(board):
            row[2 - index] = 1 if index in [0, 1] else 0
        # First test that if the diagonal direction is turned off when you have 2 in a row 
        # diagonally, an empty list is returned because you weren't allowed to seach diagonally
        self.assertEqual(
            self.instance_ai_prog.fork_helper(1, [1,1], board, directions),
            []
        )
        directions['diagonal'] = True
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
        directions['diagonal'] = False
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



if __name__ == '__main__':
    unittest.main()
