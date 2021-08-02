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
            'diagonal': True,
            'diagonal_1': True,
            'diagonal_2': True
        }

    def test_minimax_empty_board_layer_1(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        available_spots = copy.deepcopy(self.instance_game_vars.instance_array_of_available_spots)
        evaluation = self.instance_ai_prog.minimax(1, board, True, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation, [[1, 1], 4])
        evaluation = self.instance_ai_prog.minimax(1, board, False, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation, [[1, 1], -4])

    def test_minimax_empty_board_layer_2(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        available_spots = copy.deepcopy(self.instance_game_vars.instance_array_of_available_spots)
        evaluation = self.instance_ai_prog.minimax(2, board, True, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation, [[1, 1], -2])
        evaluation = self.instance_ai_prog.minimax(2, board, False, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation, [[1, 1], 2])

    def test_minimax_empty_board_layer_3(self):
        # An interesting edge case where the best move is not chosen on an empty board.
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        available_spots = copy.deepcopy(self.instance_game_vars.instance_array_of_available_spots)
        evaluation = self.instance_ai_prog.minimax(3, board, True, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation, [[0, 0], 2])
        evaluation = self.instance_ai_prog.minimax(3, board, False, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation, [[0, 0], -2])

    def test_minimax_not_empty_layer_1(self):
        # We test that when the board is not empty, minimax returns the right moves based on what's
        # available. We don't run through the whole game because writing a test where you go through
        # the whole game doesn't add much value. We just want to make sure that when the board is not
        # empty, the AI makes the right desicions, especially when blocking a fork is the best move
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        available_spots = copy.deepcopy(self.instance_game_vars.instance_array_of_available_spots)
        board[1][1] = 1
        available_spots[1][1] = False
        evaluation = self.instance_ai_prog.minimax(1, board, False, 2, 1, [0, 0], available_spots)
        self.assertEqual(evaluation, [[0, 0], -2])
        board[0][0] = 2
        board[2][2] = 1
        available_spots[0][0] = False
        available_spots[2][2] = False
        self.instance_ai_prog.instance_player_spots[1] = [[1, 1], [2, 2]]
        self.instance_ai_prog.instance_player_spots[2] = [[0, 0]]
        fork_block_eval = self.instance_ai_prog.minimax(1, board, False, 2, 1, [0, 0], available_spots)
        self.assertEqual(fork_block_eval, [[0, 2], -6])

    def test_minimax_win_for_other_person(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        available_spots = copy.deepcopy(self.instance_game_vars.instance_array_of_available_spots)
        board[0] = [1, 2, 1]
        board[1][1] = 2
        board[2][1] = 2
        available_spots[0] = [False * 3]
        available_spots[1][1] = False
        available_spots[2][1] = False
        evaluation = self.instance_ai_prog.minimax(1, board, True, 1, 2, [2, 1], available_spots)
        self.assertEqual(evaluation, [[2, 1], -18])


if __name__ == '__main__':
    unittest.main()
