# These are saved as .txt files most likely. Copy the text onto your python IDE
# (preferrably use Atom) and save this as "File_and_menu.py"
from game_tracking_variables import GameVariables
from print_methods import PrintFunctions
from input_methods import InputFunctions
from game_module import SinglePlayer
from game_module import Multiplayer
from file_and_database_module import FileAndDatabaseObject
from checker_fns import Checker
from artificial_intelligence import TheAIProgram
import sys
import os
import sqlite3

class MainMenuClass:
    """
        This function is responsible for the user interface of our game, from the choice
        to play, to the leaderboards section, to our main menu, sign in options, etc.
    """
    def select_difficulty(self,game_tracking_var_object):
        """
            This function selects the difficulty when we play in single player.
        """
        string_input = input('Enter a level of difficulty. Enter either \'Easy\', \'Medium\', or \'Hard\':')
        while (not((string_input.casefold()) in game_tracking_var_object.instance_valid_difficulty_inputs)):
            string_input = input('Invalid input. Enter either \'Easy\', \'Medium\', or \'Hard\':')
        if ((string_input.casefold()) == game_tracking_var_object.instance_valid_difficulty_inputs[0]):
            return game_tracking_var_object.instance_translate_difficulty_to_recursion_levels['Easy']
        elif ((string_input.casefold()) == game_tracking_var_object.instance_valid_difficulty_inputs[1]):
            return game_tracking_var_object.instance_translate_difficulty_to_recursion_levels['Medium']
        else:
            return game_tracking_var_object.instance_translate_difficulty_to_recursion_levels['Hard']

    def select_player_option(self,game_tracking_var_object,file_and_database,\
                             single_player_object,multiplayer_game,ai_object,\
                             checker_object,input_method_object,print_method_object):
        """
            This function runs the grand scheme of the single_player_object, taking care
            of which mode is being played at, the difficulty, the adjsuting of the
            database, and reading it to the file.
        """
        difficulty = None
        nones = file_and_database.number_of_nones(file_and_database.instance_players_signed_in)
        result = []
        name_index = None
        string_input = input('Select \'s\' for single player, \'m\' for multiplayer:')
        while (not((string_input.casefold()) in game_tracking_var_object.instance_single_or_multiplayer)):
            string_input = input('Invalid input. Enter either \'s\' for single player,\
 or \'m\' for multiplayer:')
        if ((string_input.casefold()) == game_tracking_var_object.instance_single_or_multiplayer[0]):
            if (nones == 0):
                string_input = input('There are 2 people signed in. Select 1 of \'{First_name}\' and\
 \'{Second_name}\' to play as:'.format(\
                First_name = file_and_database.instance_players_signed_in[0],\
                Second_name = file_and_database.instance_players_signed_in[1]))
                while (not((string_input.casefold()) in file_and_database.instance_players_signed_in)):
                    string_input = input('Invalid input. Select 1 of \'{First_name}\' and\
 \'{Second_name}\' to play as:'.format(\
                First_name = file_and_database.instance_players_signed_in[0],\
                Second_name = file_and_database.instance_players_signed_in[1]))
                difficulty = self.select_difficulty(game_tracking_var_object)
                result = single_player_object.run_single_player(string_input,difficulty,\
                                                                ai_object,checker_object,\
                                                                input_method_object,\
                                                                print_method_object,\
                                                                game_tracking_var_object)
                file_and_database.result_score_single_player(result[0],result[1],\
                                                             result[2],result[3],\
                                                             result[4],\
                                                             game_tracking_var_object)
            elif (nones == 1):
                if (file_and_database.instance_players_signed_in[0] == None):
                    name_index = 1
                else:
                    name_index = 0
                difficulty = self.select_difficulty(game_tracking_var_object)
                result = single_player_object.run_single_player(\
                file_and_database.instance_players_signed_in[name_index],\
                difficulty,ai_object,checker_object,input_method_object,\
                print_method_object,game_tracking_var_object)
                file_and_database.result_score_single_player(result[0],result[1],\
                                                             result[2],result[3],\
                                                             result[4],\
                                                             game_tracking_var_object)

            else:
                print('You will be signed in as nobody.')
                difficulty = self.select_difficulty(game_tracking_var_object)
                result = single_player_object.run_single_player(None,difficulty,ai_object,\
                                                                checker_object,\
                                                                input_method_object,\
                                                                print_method_object,\
                                                                game_tracking_var_object)
                file_and_database.result_score_single_player(result[0],result[1],\
                                                             result[2],result[3],\
                                                             result[4],\
                                                             game_tracking_var_object)
        else:
            if (nones == 1):
                if (file_and_database.instance_players_signed_in[0] == None):
                    i = 1
                    j = 0
                else:
                    i = 0
                    j = 1
                if ((len(file_and_database.instance_database)) == 1):
                    print('Not enough names in the database. Noboody will be signed\
 in during the game.')
                    result = multiplayer_game.run_game('','',checker_object,\
                                                       game_tracking_var_object,\
                                                       print_method_object,\
                                                       input_method_object)
                else:
                    name = input('One person signed in. Sign in another:')
                    is_there = file_and_database.name_is_there(name)
                    while (((len(is_there)) == 0) or (name.casefold() == file_and_database.instance_players_signed_in[i].casefold())):
                        name = input('The name you registered as is not there or \
signed in. Enter a different name.\n')
                        is_there = file_and_database.name_is_there(name)
                    file_and_database.instance_players_signed_in[j] = name.casefold()
                    print('{First_name}, {Second_name} are the two names signed in.\
 The second name just signed in is the second player.'.format\
                    (First_name = file_and_database.instance_players_signed_in[0],\
                    Second_name = file_and_database.instance_players_signed_in[1]))
                    result = multiplayer_game.run_game(file_and_database.instance_players_signed_in[i],\
                                                       name,checker_object,\
                                                       game_tracking_var_object,\
                                                       print_method_object,\
                                                       input_method_object)
                    file_and_database.result_score_multiplayer(result[0],result[1],\
                                                               result[2],result[3],\
                                                               result[4])
            elif (nones == 0):
                print('{First_name} is signed in as player 1, and {Second_name}\
 is signed as player 2.'.format\
                (First_name = file_and_database.instance_players_signed_in[0],\
                Second_name = file_and_database.instance_players_signed_in[1]))
                result = multiplayer_game.run_game(file_and_database.instance_players_signed_in[0],\
                                                   file_and_database.instance_players_signed_in[1],\
                                                   checker_object,game_tracking_var_object,\
                                                   print_method_object,input_method_object)
                file_and_database.result_score_multiplayer(result[0],result[1],\
                                                           result[2],result[3],\
                                                           result[4])
            else:
                print('Nobody is signed in, so the game will continue without anyone signed in.')
                result = multiplayer_game.run_game(None,None,checker_object,game_tracking_var_object,\
                                                   print_method_object,input_method_object)
        checker_object.reset_the_board(game_tracking_var_object)
        print_method_object.clear_the_board(game_tracking_var_object)

    def print_rules(self):
        """
            This function prints the rules of how we organize our leaderboards
            when the player requests it.
        """
        print('We have 3 levels of difficulty: Easy, Medium, Hard. Winning on these\
 levels gives +4,5,6 respectively. Losing on\n Easy, Medium, Hard gives -6,-5,-4\
 respectively. Tying on Easy, Medium, Hard gives +1,2,3 respectively. This is\n\
 added to your existing score to give you your score. Players who haven\'t played\
 are given a score of 0, and are\n placed below the standings of anyone who has\
 played. When scores are tied, they are listed from top down in alphabetical\n\
 order. When you play multiplayer and win, it\'s +2, when you lose it\'s -2, and\
 when you tie yo get +1.\n')


    def leaderboards(self,file_and_database,game_tracking_var_object,single_player_object,\
                     multiplayer_game,ai_object,checker_object,input_method_object,\
                     print_method_object):
        """
            This is our leaderboards function that our leaderboards option leads to
            in the main menu. You can clear names, clear a specific name, read the rules,
            set all profiles back to values of 0 (indicating everyone has a clean slate),
            print the leaderboards, or go back to the main menu.
        """
        string_input = input('Press \'r\' for rules, \'c\' to clear the scores \
(everyone starts at 0 again), \'clear\' to clear\n all names, \'clear name\' to \
clear a name, \'b\' to go back to main menu, and \'p\' to print the leaderboards.\n')
        while (not((string_input.casefold()) in ['r','c','clear','b','clear name','p'])):
            string_input = input('Invalid input Press \'r\' for rules, \'c\' to \
clear the scores (everyone starts at 0 again),\n\'clear\' to clear all names, \
\'clear name\' to clear a name, \'b\' to go back to main menu, amd \'p\' to print \
the leaderboards.\n')
        if ((string_input.casefold()) == 'b'):
            self.main_menu(file_and_database,game_tracking_var_object,single_player_object,\
                           multiplayer_game,ai_object,checker_object,input_method_object,\
                           print_method_object)
        else:
            if ((string_input.casefold()) == 'r'):
                self.print_rules()
            elif ((string_input.casefold()) == 'c'):
                file_and_database.clear()
            elif ((string_input.casefold()) == 'clear'):
                file_and_database.clear_names()
            elif ((string_input.casefold()) == 'p'):
                file_and_database.print_leaderboards()
            else:
                file_and_database.clear_a_name()
            self.leaderboards(file_and_database,game_tracking_var_object,\
                              single_player_object,multiplayer_game,\
                              ai_object,checker_object,input_method_object,\
                              print_method_object)


    def main_menu(self,file_and_database,game_tracking_var_object,single_player_object,\
                  multiplayer_game,ai_object,checker_object,input_method_object,\
                  print_method_object):
        """
            This is our start menu to start from. You can quit, sign in, play the
            single_player_object, sign out, or go to the leaderboards option explained above.
        """
        file_and_database.check_leaderboards()
        if ((len(file_and_database.instance_database)) == 0):
            file_and_database.instance_database = file_and_database.get_and_sort_profiles()

        string_input = input('Welcome to Tic Tac Toe. Press \'l\' for leaderboards,\
 \'q\' to quit, \'s\' to sign in or enter a new username,\n\'g\' to play the game\
 and \'o\' to sign out.\n')
        while (not ((string_input.casefold()) in ['l','q','s','g','o'])):
            string_input = input('Invalid input. Press \'l\' for leaderboards,\
 \'q\' to quit,\'s\' to sign in or enter a new username,\n\'g\' to play the game\
 and \'o\' to sign out.\n')
        if ((string_input.casefold()) == 'l'):
            self.leaderboards(file_and_database,game_tracking_var_object,single_player_object,\
                              multiplayer_game,ai_object,checker_object,input_method_object,\
                              print_method_object)
        else:
            if ((string_input.casefold()) == 's'):
                file_and_database.instance_players_signed_in = file_and_database.sign_in()
            elif ((string_input.casefold()) == 'o'):
                file_and_database.instance_players_signed_in = file_and_database.sign_out()
            elif ((string_input.casefold()) == 'g'):
                self.select_player_option(game_tracking_var_object,file_and_database,\
                                          single_player_object,multiplayer_game,\
                                          ai_object,checker_object,\
                                          input_method_object,print_method_object)
            else:
                return None
            self.main_menu(file_and_database,game_tracking_var_object,single_player_object,\
                           multiplayer_game,ai_object,checker_object,input_method_object,\
                           print_method_object)

file_object = FileAndDatabaseObject()
game_tracking_var_object = GameVariables()
single_player_object = SinglePlayer()
multi = Multiplayer()
AI = TheAIProgram()
checker_obj = Checker()
input_obj = InputFunctions()
print_obj = PrintFunctions()
Main = MainMenuClass()

Main.main_menu(file_object,game_tracking_var_object,single_player_object,multi,\
               AI,checker_obj,input_obj,print_obj)
