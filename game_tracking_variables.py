class GameVariables:
    """
        This is our class for the variables that used to keep track, print out,
        and update our game.
    """
    def __init__(self):
        """
            The following attributes are how our board is designed, how the game
            keeps track of
        """
        self.instance_board_border = '   -- -- -- '
        self.instance_board_first_row_top =  'A |  |  |  |'
        self.instance_board_row_bottom = '  |  |  |  |'
        self.instance_board_second_row_top = 'B |  |  |  |'
        self.instance_board_third_row_top = 'C |  |  |  |'
        self.instance_board_column_numbers = '    1  2  3 '
        self.instance_board = [list(self.instance_board_column_numbers),\
                               list(self.instance_board_border),\
                               list(self.instance_board_first_row_top),\
                               list(self.instance_board_row_bottom),\
                               list(self.instance_board_border),\
                               list(self.instance_board_second_row_top),\
                               list(self.instance_board_row_bottom),\
                               list(self.instance_board_border),\
                               list(self.instance_board_third_row_top),\
                               list(self.instance_board_row_bottom),\
                               list(self.instance_board_border)]
        # This is how we translate horizontally the entered coordinates vs. where
        # we have to change the Board list element above
        # Name: Coordinate_Numbers
        self.instance_translate_input_to_board_index = {
            1:3,
            2:6,
            3:9
        }
        # Name: player_1
        self.instance_turn_of_x_char_or_not = None
        # This is how we keep track of what spots are taken up
        self.instance_array_of_available_spots = [[True, True, True],\
                                                  [True, True, True],\
                                                  [True, True, True]]
        # Thisi s how we keep track what pieces are where
        # Name: Array_of_player_pieces
        self.instance_current_status_of_board_pieces = [[0,0,0],\
                                                        [0,0,0],\
                                                        [0,0,0]]
        # We use the values for the dictionary for the layers of recursion in the minimax algorithm.
        # We use the inputs entered by the user as one of the three keys here.
        # Oddly enough, more layers of recursion make it easier to beat, but overall the
        # program works when we thus switch more layers with easy instead of hard.
        # So if it ain't broke don't fix it. Although, it's different for the version
        # where the computer goes first. So we switched it up accordingly. See the minimax
        # function in the Artificial_Intelligence module and the function where the computer
        # goes first in the Game_module for more information about how.
        #Name: Difficulty
        self.instance_translate_difficulty_to_recursion_levels = {
            'Easy':5,
            'Medium':3,
            'Hard':9
        }
        # This helps us turn our entered inputs of the coordinates into according
        # numbers which will be used elsewhere
        # Name: Letter_legend
        self.instance_letter_legend = {
            'A': 1,
            'B': 2,
            'C': 3
        }

        # our dictionary we use to get the right spot on either the Array_of_player_pieces,
        # or on the board we output. I forget.
        self.instance_number_legend = {
            0:'A',
            1:'B',
            2:'C'
        }
        # Name: List_of_coordinates
        self.instance_all_valid_coordinates = [[['A',3],['A',6],['A',9]],\
                                               [['B',3],['B',6],['B',9]],\
                                               [['C',3],['C',6],['C',9]]]
        # all possible combinations we can enter. This is used in our Checker function module
        # Name: Combinations
        self.instance_all_valid_coordinate_combinations = ['A1', 'A2', 'A3', 'B1',\
                                                           'B2', 'B3', 'C1','C2','C3']
        # we use this in the select difficulty function to make sure inputs are entered
        # correctly
        # Name: Difficulties
        self.instance_valid_difficulty_inputs = ['easy','medium','hard']
        # used when we choose single or multiplayer mode
        # Name: Player_Options
        self.instance_single_or_multiplayer  = ['s','m']
