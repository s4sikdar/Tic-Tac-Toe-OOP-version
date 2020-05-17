# These are saved as .txt files most likely. Copy the text onto your python IDE
# (preferrably use Atom) and save this as "Print_fns.py"
import Variables
from Variables import *

# This class is for the functions that affect the visual output.
class Print_Functions:

    # Our print function to print the output . Basically take the variables
    # above in board, append them to a string, and print the string that
    # gets modified for each line in the board. So it print out the whole
    # board in the end
    def print_board(self,Variable_object):
        print_string = ''
        for board_row in Variable_object.Board:
            for i in range(len(board_row)):
                print_string += board_row[i]
            print(print_string)
            print_string = ''

    # The way our strings for the board worked was that you had the letter in the
    # beginning and this is how we will locate which element in the list of string
    # lists we used to figure out which level vertically we have to change the
    # individual characters
    def find_Y(self,Y_coordinate,Variable_object):
        for i in (range(len(Variable_object.Board))):
            if ((Y_coordinate.casefold()) == (Variable_object.Board[i][0].casefold())):
                return i
        return 0

    # We add an X to the visual output depending on the coordinates
    def Add_X(self,coordinates,Variable_object):
        X_val = Variable_object.Coordinate_Numbers[int(coordinates[1])]
        Y_val = self.find_Y(coordinates[0],Variable_object)
        Variable_object.Board[Y_val][X_val] = '\\'
        Variable_object.Board[Y_val][X_val + 1] = '/'
        Variable_object.Board[Y_val + 1][X_val] = '/'
        Variable_object.Board[Y_val + 1][X_val + 1] = '\\'

    # We add an O to the visual output depending on the coordinates
    def Add_O(self,coordinates,Variable_object):
        X_val = Variable_object.Coordinate_Numbers[int(coordinates[1])]
        Y_val = self.find_Y(coordinates[0],Variable_object)
        Variable_object.Board[Y_val][X_val] = '/'
        Variable_object.Board[Y_val][X_val + 1] = '\\'
        Variable_object.Board[Y_val + 1][X_val] = '\\'
        Variable_object.Board[Y_val + 1][X_val + 1] = '/'

    # This is what we use to mutate our board we print out, as well as modify
    # the array that keeps track of the pieces
    def Mutate_Board(self,Variable_object,coordinates):
        Variable_object.Array_of_available_spots\
        [Variable_object.Letter_legend[coordinates[0].upper()] - 1]\
        [(int(coordinates[1])) - 1] = False
        #print(Array_of_available_spots[Letter_legend[coordinates[0].upper()] - 1][(int(coordinates[1])) - 1])
        if Variable_object.player_1:
            Variable_object.Array_of_player_pieces\
            [Variable_object.Letter_legend[coordinates[0].upper()] - 1]\
            [(int(coordinates[1])) - 1] = 1
            self.Add_X(coordinates,Variable_object)
            #print_board()
        else:
            Variable_object.Array_of_player_pieces\
            [Variable_object.Letter_legend[coordinates[0].upper()] - 1]\
            [(int(coordinates[1])) - 1] = 2
            self.Add_O(coordinates,Variable_object)

    # We basically clear the board we print out
    def Clear_the_board(self,Variable_object):
        for i in (range(len(Variable_object.List_of_coordinates))):
            for j in (range(len(Variable_object.List_of_coordinates[i]))):
                X_val = Variable_object.List_of_coordinates[i][j][1]
                Y_val = self.find_Y(Variable_object.List_of_coordinates[i][j][0],Variable_object)
                Variable_object.Board[Y_val][X_val] = ' '
                Variable_object.Board[Y_val][X_val + 1] = ' '
                Variable_object.Board[Y_val + 1][X_val] = ' '
                Variable_object.Board[Y_val + 1][X_val + 1] = ' '
'''
Print_object = Print_fns()
Variable = Output_array()
Print_object.print_board(Variable)
Variable.player_1 = True
Print_object.Mutate_Board(Variable,'A1')
Print_object.print_board(Variable)
Print_object.Clear_the_board(Variable)
Print_object.print_board(Variable)
''' #This was all just test code. Nothing to see here

# This class is for functions that read in data from the user.
class Input_fns:

    # This is a helper function to the Enter_Coordinates function below.
    # Basically we check if a function is in the allowed combinations on the
    # board.
    def in_combinations(self,x,Variable_object):
        for i in range(len(Variable_object.Combinations)):
            if (x.casefold() == (Variable_object.Combinations[i].casefold())):
                return True
        return False

    # Enter_Coordinates takes in your input for coordinates and returns it back,
    # but displays different text based on the mode you're playing in
    def Enter_Coordinates(self,turn,Variable_object,multi_player):
        if multi_player:
            if turn:
                coordinates = input('Player 1, enter a set of coordinates.\nEnter the row first, then the column: ')
                while (not(self.in_combinations(coordinates,Variable_object))):
                    coordinates = input('This coordinate does not exist. Enter another set of coordinates: ')
            else:
                coordinates = input('Player 2, enter a set of coordinates.\nEnter the row first, then the column: ')
                while (not(self.in_combinations(coordinates,Variable_object))):
                    coordinates = input('This coordinate does not exist. Enter another set of coordinates: ')
        else:
            if turn:
                coordinates = input("Enter a set of coordinates (you're X): ")
                while (not(self.in_combinations(coordinates,Variable_object))):
                    coordinates = input('This coordinate does not exist. Enter another set of coordinates: ')
            else:
                coordinates = input("Enter a set of coordinates (you're O): ")
                while (not(self.in_combinations(coordinates,Variable_object))):
                    coordinates = input('This coordinate does not exist. Enter another set of coordinates: ')
        return coordinates

    # Basically we take in coordinates using the above functions and make sure the
    # spot's not already taken. Until we find such a spot, it keeps asking again.
    def Nothing_There(self,whos_turn,Variable_object,multi_player):
        coordinates = list(self.Enter_Coordinates(whos_turn,Variable_object,multi_player))
        First_Index = Variable_object.Letter_legend[coordinates[0].upper()]
        Not_There = Variable_object.Array_of_available_spots[First_Index - 1][(int(coordinates[1])) - 1]
        while(not Not_There):
            print('Sorry, that spot\'s taken. Choose another one.')
            coordinates = list(self.Enter_Coordinates(whos_turn,Variable_object,multi_player))
            First_Index = Variable_object.Letter_legend[coordinates[0].upper()]
            Not_There = Variable_object.Array_of_available_spots[First_Index - 1][(int(coordinates[1])) - 1]
        #print('All good. Nothing\'s there.')
        coordinates[0] = coordinates[0].upper()
        return coordinates

    # This is our function to determine who starts based on your input.
    def Who_starts(self,multi_player):
        Local_array = ['1', '2']
        if (multi_player):
            Player_1_or_2 = input('Enter who starts first.1 for player 1 (X), 2 for player 2 (O): ')
            while (not(Player_1_or_2 in Local_array)):
                Player_1_or_2 = input('Invalid input. Enter a 1 or a 2: ')
            if (Player_1_or_2 == Local_array[0]):
                return True
            return False
        else:
            Player_1_or_2 = input('Enter 1 to be X, enter 2 to be O: ')
            while (not(Player_1_or_2 in Local_array)):
                Player_1_or_2 = input('Invalid input. Enter a 1 or a 2: ')
            if (Player_1_or_2 == Local_array[0]):
                return True
            return False

    # if you want to keep playing, enter 'y' or 'n' for yes and no respectively.
    # This functio used to be in use, but our main menu makes it such that this function
    # is not used. It is used in one of the Game_module functions to determine if you want to
    # continue playing.
    def keep_playing(self):
        Inputs = ['y', 'n']
        Keep_playing = input('Keep playing? \'Y\' for yes, \'N\' for No: ')
        while (not ((Keep_playing.lower()) in Inputs)):
            Keep_playing = input('Invalid Entry. Enter \'Y\' for yes, \'N\' for No: ')

        if ((Keep_playing.casefold()) == ('y'.casefold())):
            return True
        else:
            return False
'''
New_input = Input_fns()
Var = Output_array()
New_input.Who_starts()
'''
