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

    def find_move(self, game_tracking_vars, difficulty, difficulty_level, ai_object):
        threshold_level = game_tracking_vars.instance_random_move_thresholds[difficulty]
        if threshold_level <= 0:
            alpha = sys.maxsize * -1
            beta = sys.maxsize
            if game_tracking_vars.instance_turn_of_x_char_or_not:
                coordinate = ai_object.minimax(
                    7,\
                    game_tracking_vars.instance_current_status_of_board_pieces,\
                    True,2,1,[0,0],\
                    game_tracking_vars.instance_array_of_available_spots,
                    alpha=alpha,
                    beta=beta
                )
            else:
                coordinate = ai_object.minimax(
                    7,\
                    game_tracking_vars.instance_current_status_of_board_pieces,\
                    True,1,2,[0,0],\
                    game_tracking_vars.instance_array_of_available_spots,
                    alpha=alpha,
                    beta=beta
                )
            return coordinate[0]
        else:
            number = random.randint(1, 10)
            if number <= threshold_level:
                return self.find_random_move(game_tracking_vars)
            else:
                alpha = sys.maxsize * -1
                beta = sys.maxsize
                if game_tracking_vars.instance_turn_of_x_char_or_not:
                    coordinate = ai_object.minimax(
                        7,\
                        game_tracking_vars.instance_current_status_of_board_pieces,\
                        True,2,1,[0,0],\
                        game_tracking_vars.instance_array_of_available_spots,
                        alpha=alpha,
                        beta=beta
                    )
                else:
                    coordinate = ai_object.minimax(
                        7,\
                        game_tracking_vars.instance_current_status_of_board_pieces,\
                        True,1,2,[0,0],\
                        game_tracking_vars.instance_array_of_available_spots,
                        alpha=alpha,
                        beta=beta
                    )
                return coordinate[0]

    # This is the full single player version against the computer
    def run_single_player(self,name,difficulty, difficulty_level, artificial_intelligence_object,\
                          input_object,print_object,game_tracking_variable_object):
        """
            This function carries out the single-player version of the game.
        """
        result = None

        in_put = input("Enter '1' to go first, enter '2' for the computer to go first: ")
        while (not((in_put.casefold()) in ['1','2'])):
            in_put = input("Invalid input. Enter '1' to go first, enter '2' for the computer to go first: ")
        comp_goes_first = in_put.casefold() == '2'
        game_tracking_variable_object.instance_turn_of_x_char_or_not = input_object.who_starts_first(False)
        if comp_goes_first:
            game_tracking_variable_object.instance_turn_of_x_char_or_not = not(
                game_tracking_variable_object.instance_turn_of_x_char_or_not
            )
        nobody_has_won = artificial_intelligence_object.no_wins(game_tracking_variable_object.instance_current_status_of_board_pieces)
        nobody_wins = None
        coordinates = None
        while nobody_has_won[0]:
            if comp_goes_first:
                coordinates = self.find_move(
                    game_tracking_variable_object, difficulty,
                    difficulty_level, artificial_intelligence_object
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

# This is the multiplayer version of Tic Tac Toe. I was thinking about putting
# this in its own module, but for roughly 60 lines it doesn't seem worth it.
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
