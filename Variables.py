# These are saved as .txt files most likely. Copy the text onto your python IDE
# (preferrably use Atom) and save this as "Variables.py"

# This is our class for the output shown on the board, as well as functions
# relating to the string that we put out. It's a string that turns into a
# list because we need to be able to modify the strings that we output.

class Output_array:
    # This is our constructor
    # Basically all the attributes in this object are used by other modules and according objects
    # It's nicer to put it into one object to start with.
    def __init__(self):
        # The following first few attributes are how our output board is designed
        self.Border = '   -- -- -- '
        self.First_Row_Top =  'A |  |  |  |'
        self.Row_Bottom = '  |  |  |  |'
        self.Second_Row_Top = 'B |  |  |  |'
        self.Third_Row_Top = 'C |  |  |  |'
        self.Top_Numbers = '    1  2  3 '
        self.Board = [list(self.Top_Numbers),list(self.Border),list(self.First_Row_Top),\
                      list(self.Row_Bottom),list(self.Border),list(self.Second_Row_Top),\
                      list(self.Row_Bottom),list(self.Border),list(self.Third_Row_Top),\
                      list(self.Row_Bottom),list(self.Border)]
        # This is how we translate horizontally the entered coordinates vs. where
        # we have to change the Board list element above
        self.Coordinate_Numbers = {
            1:3,
            2:6,
            3:9
        }
        self.player_1 = None
        # This is how we keep track of what spots are taken up
        self.Array_of_available_spots = [[True, True, True],\
                                         [True, True, True],\
                                         [True, True, True]]
        # Thisi s how we keep track what pieces are where
        self.Array_of_player_pieces = [[0,0,0],\
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
        self.Difficulty = {
            'Easy':5,
            'Medium':3,
            'Hard':1
        }
        # This helps us turn our entered inputs of the coordinates into according
        # numbers which will be used elsewhere
        self.Letter_legend = {
            'A': 1,
            'B': 2,
            'C': 3
        }

        # our dictionary we use to get the right spot on either the Array_of_player_pieces,
        # or on the board we output. I forget.
        self.Number_legend = {
            0:'A',
            1:'B',
            2:'C'
        }

        self.List_of_coordinates = [[['A',3],['A',6],['A',9]],\
                                    [['B',3],['B',6],['B',9]],\
                                    [['C',3],['C',6],['C',9]]]
        # all possible combinations we can enter. This is used in our Checker function module
        self.Combinations = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1','C2','C3']
        # we use this in the select difficulty function to make sure inputs are entered
        # correctly
        self.Difficulties = ['easy','medium','hard']
        # used when we choose single or multiplayer mode
        self.Player_Options = ['s','m']
