from artificial_intelligence import TheAIProgram
import sys
from utils import checker_utils
from input_methods import InputFunctions
from print_methods import PrintFunctions
from game_tracking_variables import GameVariables

class SinglePlayer:
    """
        This class is the implementation of single player Tic Tac Toe.
    """

    def person_goes_first(self,name,difficulty,artificial_intelligence_object,\
                          input_object,print_object,game_tracking_variable_object):
        """
            This function carries out the game when the individual opts to go first against
            the computer.
        """
        game_tracking_variable_object.instance_turn_of_x_char_or_not = input_object.who_starts_first(False)
        nobody_has_won = artificial_intelligence_object.no_wins(game_tracking_variable_object.instance_current_status_of_board_pieces)
        nobody_wins = None
        coordinates = None
        # Our loop to continue playing while nobody has won
        while nobody_has_won[0]:
            # Print the board, then ask for input, then change the state of the board,
            # then check if nobody won, or if the board is filled up
            print_object.print_board(game_tracking_variable_object)
            coordinates = input_object.nothing_there(game_tracking_variable_object.instance_turn_of_x_char_or_not,\
                                                     game_tracking_variable_object,False)
            print_object.change_game_state(game_tracking_variable_object,coordinates)
            nobody_has_won = artificial_intelligence_object.no_wins(game_tracking_variable_object.instance_current_status_of_board_pieces)
            all_filled = checker_utils.all_filled_up(game_tracking_variable_object.instance_array_of_available_spots)
            nobody_wins = ((nobody_has_won[0]) and all_filled)
            # If somebody won, the print the board along with who won
            # and return the result.
            if (not (nobody_has_won[0])):
                print_object.print_board(game_tracking_variable_object)
                if (game_tracking_variable_object.instance_turn_of_x_char_or_not):
                    print('X wins')
                else:
                    print('O wins')
                return [name,difficulty,True,False,False]
                break
            # If nobody won, print the board and print that nobody won, then return
            # the result.
            if (nobody_wins):
                print_object.print_board(game_tracking_variable_object)
                print('Nobody wins.')
                return [name,difficulty,False,False,True]
                break
            # We play as the result character that wants to maximize its score here
            if (game_tracking_variable_object.instance_turn_of_x_char_or_not):
                coordinates = artificial_intelligence_object.minimax(difficulty,\
                                                                     game_tracking_variable_object.instance_current_status_of_board_pieces,\
                                                                     True,2,1,[0,0],\
                                                                     game_tracking_variable_object.instance_array_of_available_spots)
            # Here we play as the y character that want to minimize its score
            else:
                coordinates = artificial_intelligence_object.minimax(difficulty,\
                                                                     game_tracking_variable_object.instance_current_status_of_board_pieces,\
                                                                     True,1,2,[0,0],\
                                                                     game_tracking_variable_object.instance_array_of_available_spots)
            # Switch the boolean representing who's turn it is, for the next iteration
            game_tracking_variable_object.instance_turn_of_x_char_or_not = not(game_tracking_variable_object.instance_turn_of_x_char_or_not)
            # Change the state of the game now that the minimax function chose the right
            # coordinates
            print_object.change_game_state(game_tracking_variable_object,\
                                           [game_tracking_variable_object.instance_number_legend.get(int(coordinates[0][0])),\
                                            (coordinates[0][1] + 1)])
            # Now check that nobody won, and that the array is not filled up.
            nobody_has_won = artificial_intelligence_object.no_wins(game_tracking_variable_object.instance_current_status_of_board_pieces)
            all_filled = checker_utils.all_filled_up(game_tracking_variable_object.instance_array_of_available_spots)
            nobody_wins = ((nobody_has_won[0]) and all_filled)
            # If the booleans indicate that someone won, or that the board filled up
            # and nobody won, then react accordingly
            if (not (nobody_has_won[0])):
                print_object.print_board(game_tracking_variable_object)
                if (game_tracking_variable_object.instance_turn_of_x_char_or_not):
                    print('X wins')
                else:
                    print('O wins')
                return [name,difficulty,False,True,False]
                break
            if (nobody_wins):
                print_object.print_board(game_tracking_variable_object)
                print('Nobody wins.')
                return [name,difficulty,False,False,True]
                break
            game_tracking_variable_object.instance_turn_of_x_char_or_not = not(game_tracking_variable_object.instance_turn_of_x_char_or_not)


    # I added functionality for when the computer goes first. The minimax function
    # result works differently when the person goes first vs when the computer
    # goes second. When it goes first, it works more so as to how it should with the
    # layers of recursion, except it seems easier to beat on medium than easy mode,
    # so I gave the "medium" layer of recursion when in easy mode.
    def computer_goes_first(self,name,difficulty,artificial_intelligence_object,\
                            input_object,print_object,game_tracking_variable_object):
        """
            This function carries out the game when the individual opts to let the
            computer go first.
        """
        # Figure out who's playing as who, to establish accordingly which piece or
        # number associated with it is going to be played by you.
        game_tracking_variable_object.instance_turn_of_x_char_or_not = input_object.who_starts_first(False)
        nobody_has_won = artificial_intelligence_object.no_wins(game_tracking_variable_object.instance_current_status_of_board_pieces)
        nobody_wins = None
        coordinates = None
        while nobody_has_won[0]:
            # Based on who's result and who's o, the computer then plays as the according
            # character and thus that number.
            if (game_tracking_variable_object.instance_turn_of_x_char_or_not):
                coordinates = artificial_intelligence_object.minimax(difficulty,\
                                                                     game_tracking_variable_object.instance_current_status_of_board_pieces,\
                                                                     True,2,1,[0,0],\
                                                                     game_tracking_variable_object.instance_array_of_available_spots)
            else:
                coordinates = artificial_intelligence_object.minimax(difficulty,\
                                                                     game_tracking_variable_object.instance_current_status_of_board_pieces,\
                                                                     True,1,2,[0,0],\
                                                                     game_tracking_variable_object.instance_array_of_available_spots)
            # print(difficulty, coordinates)
            # Flip the switch of which character is going to be filled. Change the
            # game state based on the coordinates returned, check to see if anybody won
            # or if the board is full. If any of those things happened, react accordingly.
            game_tracking_variable_object.instance_turn_of_x_char_or_not = not(game_tracking_variable_object.instance_turn_of_x_char_or_not)
            print_object.change_game_state(game_tracking_variable_object,\
                                           [game_tracking_variable_object.instance_number_legend.get(int(coordinates[0][0])),\
                                            (coordinates[0][1] + 1)])
            nobody_has_won = artificial_intelligence_object.no_wins(game_tracking_variable_object.instance_current_status_of_board_pieces)
            all_filled = checker_utils.all_filled_up(game_tracking_variable_object.instance_array_of_available_spots)
            nobody_wins = ((nobody_has_won[0]) and all_filled)
            if (not (nobody_has_won[0])):
                print_object.print_board(game_tracking_variable_object)
                if (game_tracking_variable_object.instance_turn_of_x_char_or_not):
                    print('X wins')
                else:
                    print('O wins')
                if (difficulty == game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Easy']):
                    return [name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Hard'],False,True,False]
                elif (difficulty == game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Medium']):
                    return [name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Easy'],False,True,False]
                else:
                    return [name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Medium'],False,True,False]
                break
            if (nobody_wins):
                print_object.print_board(game_tracking_variable_object)
                print('Nobody wins.')
                if (difficulty == game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Easy']):
                    return [name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Hard'],False,False,True]
                elif (difficulty == game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Medium']):
                    return [name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Easy'],False,False,True]
                else:
                    return [name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Medium'],False,False,True]
                break
            # switch to the character of the user, get input from them, update the board,
            # then check if someone won or the board is full. If either of those things
            # happened, react accordingly.
            game_tracking_variable_object.instance_turn_of_x_char_or_not = not(game_tracking_variable_object.instance_turn_of_x_char_or_not)

            print_object.print_board(game_tracking_variable_object)
            coordinates = input_object.nothing_there(game_tracking_variable_object.instance_turn_of_x_char_or_not,game_tracking_variable_object,False)
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
                if (difficulty == game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Easy']):
                    return [name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Hard'],True,False,False]
                elif (difficulty == game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Medium']):
                    return [name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Easy'],True,False,False]
                else:
                    return [name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Medium'],True,False,False]
                break
            if (nobody_wins):
                print_object.print_board(game_tracking_variable_object)
                print('Nobody wins.')
                if (difficulty == game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Easy']):
                    return [name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Hard'],False,False,True]
                elif (difficulty == game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Medium']):
                    return [name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Easy'],False,False,True]
                else:
                    return [name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Medium'],True,False,False]
                break


    # This is the full single player version against the computer
    def run_single_player(self,name,difficulty,artificial_intelligence_object,\
                          input_object,print_object,game_tracking_variable_object):
        """
            This function carries out the single-player version of the game.
        """
        result = None

        in_put = input("Enter '1' to go first, enter '2' for the computer to go first: ")
        while (not((in_put.casefold()) in ['1','2'])):
            in_put = input("Invalid input. Enter '1' to go first, enter '2' for the computer to go first: ")

        if ((in_put.casefold()) == '1'):
            result = self.person_goes_first(name,difficulty,artificial_intelligence_object,\
                                            input_object,print_object, game_tracking_variable_object)
            return result
        else:
            # Easy
            if (difficulty == game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Hard']):
                result = self.computer_goes_first(name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Hard'],\
                                                  artificial_intelligence_object,\
                                                  input_object,print_object,\
                                                  game_tracking_variable_object)
                return result
            elif (difficulty == game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Easy']):
                result = self.computer_goes_first(name,game_tracking_variable_object.instance_translate_difficulty_to_recursion_levels['Medium'],\
                                                  artificial_intelligence_object,\
                                                  input_object,print_object,\
                                                  game_tracking_variable_object)
                return result
            else:
                result = self.computer_goes_first(name,2,\
                                                  artificial_intelligence_object,\
                                                  input_object,print_object,\
                                                  game_tracking_variable_object)
                return result

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
