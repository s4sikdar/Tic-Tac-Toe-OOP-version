# from _typeshed import Self
from logging import BufferingFormatter
import unittest
from unittest.mock import patch, Mock
import copy
import sys

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
        self.alpha_beta = {
            'alpha': -1 * sys.maxsize,
            'beta': sys.maxsize
        }

    def static_evaluation(self,current_coordinate,player_pieces_array,player_number,\
                          other_player_number):
        """
            This is the static evaluation function that puts everything together.
            We basically check what the evaluation is at this spot based on a ranking
            system of priorities I got from wikipedia:
            https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
            We return the result accordingly.
        """
        # So we exercise the above helper functions and assign the results to booleans.
        # The corresponding states will cause us to return a list with static evaluations
        # at that spots.
        win = self.instance_ai_prog.three_in_a_row_at_this_spot(player_number,player_pieces_array,\
                                                                current_coordinate)
        a_block = self.instance_ai_prog.block(current_coordinate,player_pieces_array,player_number,\
                                              other_player_number)
        forks = self.instance_ai_prog.fork(current_coordinate,player_pieces_array,player_number)
        opposite_fork = self.instance_ai_prog.fork_for_them(current_coordinate,player_pieces_array,\
                                                            player_number, other_player_number)
        if win:
            return [current_coordinate,9]
        elif a_block:
            return [current_coordinate,8]
        elif forks:
            return [current_coordinate,7]
        elif opposite_fork:
            return [current_coordinate,5]
        elif current_coordinate == [1,1]:
            return [current_coordinate,4]
        elif self.instance_ai_prog.opposite_corner(current_coordinate,player_pieces_array,other_player_number):
            return [current_coordinate,3]
        elif current_coordinate in [[0,0],[0,2],[2,0],[2,2]]:
            return [current_coordinate,2]
        else:
            return [current_coordinate,1]

    def test_minimax_empty_board_layer_1(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        available_spots = copy.deepcopy(self.instance_game_vars.instance_array_of_available_spots)
        alpha_beta = copy.deepcopy(self.alpha_beta)
        evaluation = self.instance_ai_prog.minimax(1, board, True, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation, [[1, 1], 4])
        alpha_beta = copy.deepcopy(self.alpha_beta)
        evaluation = self.instance_ai_prog.minimax(1, board, False, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation, [[1, 1], -4])

    def test_minimax_empty_board_layer_2(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        available_spots = copy.deepcopy(self.instance_game_vars.instance_array_of_available_spots)
        alpha_beta = copy.deepcopy(self.alpha_beta)
        evaluation = self.instance_ai_prog.minimax(2, board, True, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation, [[1, 1], -2])
        alpha_beta = copy.deepcopy(self.alpha_beta)
        evaluation = self.instance_ai_prog.minimax(2, board, False, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation, [[1, 1], 2])

    def test_minimax_empty_board_layer_3(self):
        # An interesting edge case where the best move is not chosen on an empty board.
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        available_spots = copy.deepcopy(self.instance_game_vars.instance_array_of_available_spots)
        alpha_beta = copy.deepcopy(self.alpha_beta)
        evaluation = self.instance_ai_prog.minimax(3, board, True, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation, [[0, 0], 2])
        alpha_beta = copy.deepcopy(self.alpha_beta)
        evaluation = self.instance_ai_prog.minimax(3, board, False, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation, [[0, 0], -2])

    def test_minimax_empty_board_layer_4(self):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        available_spots = copy.deepcopy(self.instance_game_vars.instance_array_of_available_spots)
        evaluation = self.instance_ai_prog.minimax(4, board, True, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation, [[0, 1], -5])
        alpha_beta = copy.deepcopy(self.alpha_beta)
        evaluation_min = self.instance_ai_prog.minimax(4, board, False, 1, 2, [0, 0], available_spots)
        self.assertEqual(evaluation_min, [[0, 1], 5])

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

    @patch('artificial_intelligence.TheAIProgram.static_evaluation')
    def test_alpha_beta_vs_minimax_layer_2(self, static_eval_mock):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        available_spots  = copy.deepcopy(self.instance_game_vars.instance_array_of_available_spots)
        alpha_beta = copy.deepcopy(self.alpha_beta)
        static_eval_mock.side_effect = self.static_evaluation
        regular_minimax_eval = self.instance_ai_prog.minimax(2, board, True, 1, 2, [0, 0], available_spots)
        self.assertEqual(static_eval_mock.call_count, 72)
        static_eval_mock.reset_mock()
        alpha_beta_eval = self.instance_ai_prog.minimax(2, board, True, 1, 2, [0, 0], available_spots, **alpha_beta)
        self.assertLess(static_eval_mock.call_count, 72)
        self.assertEqual(regular_minimax_eval, [[1, 1], -2])
        self.assertEqual(regular_minimax_eval, alpha_beta_eval)

    @patch('artificial_intelligence.TheAIProgram.static_evaluation')
    def test_alpha_beta_vs_minimax_layer_3(self, static_eval_mock):
        board = copy.deepcopy(self.instance_game_vars.instance_current_status_of_board_pieces)
        available_spots  = copy.deepcopy(self.instance_game_vars.instance_array_of_available_spots)
        alpha_beta = copy.deepcopy(self.alpha_beta)
        static_eval_mock.side_effect = self.static_evaluation
        regular_minimax_eval = self.instance_ai_prog.minimax(3, board, True, 1, 2, [0, 0], available_spots)
        self.assertEqual(static_eval_mock.call_count, 504)
        static_eval_mock.reset_mock()
        alpha_beta_eval = self.instance_ai_prog.minimax(3, board, True, 1, 2, [0, 0], available_spots, **alpha_beta)
        self.assertLess(static_eval_mock.call_count, 504)
        self.assertEqual(regular_minimax_eval, [[0, 0], 2])
        self.assertEqual(regular_minimax_eval, alpha_beta_eval)

if __name__ == '__main__':
    unittest.main()
