from artificial_intelligence import TheAIProgram
import sys
import random
from utils import checker_utils
from input_methods import InputFunctions
from print_methods import PrintFunctions
from game_tracking_variables import GameVariables

class SinglePlayer:
    """
        This class is the implementation of single player Tic Tac Toe.
    """
    def find_random_move(self, game_tracking_vars):
        '''
            Responsible for randomly finding a spot on the board when the computer opts for
            a randomly chosen move.
        '''
        # To find a random move, draw a random integer rnum such that 
        # 0 <= rnum <= (len(game_tracking_vars.instance_array_of_available_spots) - 1).
        # This makes it such that rnum is a valid index value to access a row in the
        # board. Check if the row is all filled, and if it is keep repeating
        # this process till you find a row that has an empty spot. Then do the same, but on
        # the indices for spots inside the row. You will end up with an empty spot chosen
        # randomly, unless you have a board that is all filled.
        y_coord = random.randint(0, (len(game_tracking_vars.instance_array_of_available_spots) - 1))
        row_in_question = game_tracking_vars.instance_array_of_available_spots[y_coord]
        all_filled = checker_utils.all_3_equal(row_in_question) and not row_in_question[0]
        while all_filled:
            y_coord = random.randint(0, (len(game_tracking_vars.instance_array_of_available_spots) - 1))
            row_in_question = game_tracking_vars.instance_array_of_available_spots[y_coord]
            all_filled = checker_utils.all_3_equal(row_in_question) and not row_in_question[0]
        x_coord = random.randint(0, (len(game_tracking_vars.instance_array_of_available_spots) - 1))
        while not game_tracking_vars.instance_array_of_available_spots[y_coord][x_coord]:
            x_coord = random.randint(0, (len(game_tracking_vars.instance_array_of_available_spots) - 1))

        return [y_coord, x_coord]

    def find_move(self, game_tracking_vars, difficulty, difficulty_level, ai_object, comp_goes_first):
        '''
            Responsible for finding a move to make when on single player mode. The move could
            be random, or a result of the minimax algorithm, but it depends on the difficulty
            level.
        '''
        # We generate a random number num where both 1 <= num <= 10 and 1 <= threshold_level <= 10
        # and if num <= threshold_level then use find_random_move to get a random move. Otherwise
        # use the minimax algorithm for a move. If you are playing on hard mode, then the
        # threshold level will be 0. In that case, just run the minimax algorithm.
        threshold_level = game_tracking_vars.instance_random_move_thresholds[difficulty]
        recursion_level = 5
        if threshold_level <= 0:
            # player_num and other_player_num are set based on whether it's time for X to move
            # or O to move, and whether the computer goes first or second. So if you choose to
            # be X, then you are player number 1, and the computer is player number 2. If the
            # computer goes first, then game_tracking_vars.instance_turn_of_x_char_or_not = False
            # and player_num = 2, meaning you're X and it's O's turn to put a piece on the board. 
            # If you were O instead of X, player_num = 1. After that, other_player_num gets the
            # opposite player number. The idea of this is that you want to set player_num and
            # other_player_num such that the minimax function is being called against you. See
            # the commit message on 0a0589ad45790fffc641d52f7f28fb7255bd4141 for additional context. 
            if comp_goes_first:
                player_num = 1 if game_tracking_vars.instance_turn_of_x_char_or_not else 2
                other_player_num = 2 if game_tracking_vars.instance_turn_of_x_char_or_not else 1
            else:
                player_num = 2 if game_tracking_vars.instance_turn_of_x_char_or_not else 1
                other_player_num = 1 if game_tracking_vars.instance_turn_of_x_char_or_not else 2
            coordinate = ai_object.minimax(
                recursion_level,\
                game_tracking_vars.instance_current_status_of_board_pieces,\
                True, player_num, other_player_num, [0, 0],\
                game_tracking_vars.instance_array_of_available_spots
            )
            return coordinate[0]
        else:
            number = random.randint(1, 10)
            if number <= threshold_level:
                return self.find_random_move(game_tracking_vars)
            else:
                if comp_goes_first:
                    player_num = 1 if game_tracking_vars.instance_turn_of_x_char_or_not else 2
                    other_player_num = 2 if game_tracking_vars.instance_turn_of_x_char_or_not else 1
                else:
                    player_num = 2 if game_tracking_vars.instance_turn_of_x_char_or_not else 1
                    other_player_num = 1 if game_tracking_vars.instance_turn_of_x_char_or_not else 2
                coordinate = ai_object.minimax(
                    recursion_level,\
                    game_tracking_vars.instance_current_status_of_board_pieces,\
                    True, player_num, other_player_num, [0, 0],\
                    game_tracking_vars.instance_array_of_available_spots
                )
                return coordinate[0]

    def run_single_player(self,name,difficulty, difficulty_level, artificial_intelligence_object,\
                          input_object,print_object,game_tracking_variable_object):
        """
            This function carries out the single-player version of the game.
        """
        result = None

        in_put = input("Enter '1' to go first, enter '2' for the computer to go first: ")
        while (not((in_put.casefold()) in ['1','2'])):
            in_put = input("Invalid input. Enter '1' to go first, enter '2' for the computer to go first: ")
        # comp_goes_first basically keeps track of whether we are making a move as the computer or the user.
        comp_goes_first = in_put.casefold() == '2'
        # Determines whether it's the turn of the X player to move or not. In the event that you start, it
        # determines if you are X or O. If the computer goes first, then negate the boolean value since the
        # other character (X or O) goes first. Basically just keep track if you're putting an X or an O on
        # the board.
        game_tracking_variable_object.instance_turn_of_x_char_or_not = input_object.who_starts_first(False)
        if comp_goes_first:
            game_tracking_variable_object.instance_turn_of_x_char_or_not = not(
                game_tracking_variable_object.instance_turn_of_x_char_or_not
            )
        # So long as nobody has won the game, keep running the loop representing the game
        nobody_has_won = artificial_intelligence_object.no_wins(game_tracking_variable_object.instance_current_status_of_board_pieces)
        nobody_wins = None
        coordinates = None
        while nobody_has_won[0]:
            if comp_goes_first:
                coordinates = self.find_move(
                    game_tracking_variable_object, difficulty,
                    difficulty_level, artificial_intelligence_object, comp_goes_first
                )
                print_object.change_game_state(game_tracking_variable_object,\
                                              [game_tracking_variable_object.instance_number_legend.get(int(coordinates[0])),\
                                               (coordinates[1] + 1)])
            else:
                print_object.print_board(game_tracking_variable_object)
                coordinates = input_object.nothing_there(
                    game_tracking_variable_object.instance_turn_of_x_char_or_not,
                    game_tracking_variable_object,False
                )
                print_object.change_game_state(game_tracking_variable_object,coordinates)
            nobody_has_won = artificial_intelligence_object.no_wins(game_tracking_variable_object.instance_current_status_of_board_pieces)
            all_filled = checker_utils.all_filled_up(game_tracking_variable_object.instance_array_of_available_spots)
            nobody_wins = ((nobody_has_won[0]) and all_filled)
            if (not (nobody_has_won[0])):
                print_object.print_board(game_tracking_variable_object)
                if (game_tracking_variable_object.instance_turn_of_x_char_or_not):
                    print('X wins')
                else:
                    print('O wins')
                if comp_goes_first:
                    result = [name, difficulty_level, False, True, False]
                else:
                    result = [name, difficulty_level, True, False, False]
            if (nobody_wins):
                print_object.print_board(game_tracking_variable_object)
                print('Nobody wins.')
                result = [name, difficulty_level, False, False, True]
            if ((not nobody_has_won[0]) or nobody_wins):
                return result
            comp_goes_first = not comp_goes_first
            game_tracking_variable_object.instance_turn_of_x_char_or_not = not(
                game_tracking_variable_object.instance_turn_of_x_char_or_not
            )

class Multiplayer:
    """
        This class is responsible for the multiplayer version of Tic Tac Toe
    """
    def run_game(self,name,second_name,game_tracking_variable_object,\
                 print_object,input_object):
        """
            This function carries out the multiplayer version of the game.
        """
        # Figure out who starts.
        game_tracking_variable_object.instance_turn_of_x_char_or_not = input_object.who_starts_first(True)
        nobody_has_won = True
        nobody_wins = None
        coordinates = None
        all_filled = False
        while (nobody_has_won):
            # print the board, get input from the first user, then update the board.
            # From there check if anybody won. If somebody won, return the according
            # results. Then check if the board filled up. If it did, return the according
            # results. Then change the boolean representing who's turn it is.
            # Then repeat until somebody won or the board filled up.
            print_object.print_board(game_tracking_variable_object)
            coordinates = input_object.nothing_there(game_tracking_variable_object.instance_turn_of_x_char_or_not,game_tracking_variable_object,\
                                                     True)
            print_object.change_game_state(game_tracking_variable_object,coordinates)
            somebody_won = checker_utils.somebody_wins(game_tracking_variable_object.instance_current_status_of_board_pieces)
            if bool(somebody_won):
                print_object.print_board(game_tracking_variable_object)
                print(f'Player {somebody_won} wins!')
                if game_tracking_variable_object.instance_turn_of_x_char_or_not:
                    return [name,second_name,True,False,False]
                else:
                    return [name,second_name,False,True,False]
            all_filled = checker_utils.all_filled_up(game_tracking_variable_object.instance_array_of_available_spots)
            nobody_wins = (nobody_has_won and all_filled)
            if (nobody_wins):
                print_object.print_board(game_tracking_variable_object)
                print('Nobody wins.')
                return [name,second_name,False,False,True]
                break
            game_tracking_variable_object.instance_turn_of_x_char_or_not = not(game_tracking_variable_object.instance_turn_of_x_char_or_not)


    def Tic_Tac_Toe_Interactive_Version(self,name,second_name,game_tracking_variable_object,print_object,input_object):
        """
            This function calls the game repeatedly, allowing us to continue playing in
            multiplayer until we opt to stop. This function is no longer in use.
        """

        results = None
        continue_playing = True
        while continue_playing:
            results = self.run_game(name,second_name,game_tracking_variable_object,print_object,input_object)
            continue_playing = input_object.keep_playing()
            if continue_playing:
                game_tracking_variable_object.reset_the_board()
                print_object.clear_the_board(game_tracking_variable_object)
