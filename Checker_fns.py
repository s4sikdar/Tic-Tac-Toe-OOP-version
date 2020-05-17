# These are saved as .txt files most likely. Copy the text onto your python IDE
# (preferrably use Atom) and save this as "Checker_fns.py"
import Variables
from Print_fns import Print_Functions
# This class is for our checker functions, which basically are responsible
# for monitoring the status of the game (i.e. if someone won, etc.)
class Checker:

    # For our array of available spots are the three spot numbers equal in a given horizontal row?
    # That's what this does
    def True_across(self,row):
        return ((row[0] == row[1]) and (row[1] == row[2]))

    # Checks all of the three rows to see if we have three in a row
    def Three_in_a_row(self,current_row):
        for i in (range(len(current_row))):
            if (self.True_across(current_row[i])):
                if (not (current_row[i][0] == 0)):
                    return current_row[i][0]
        return None

    # Checks all of the three columns to see if we have three in a column
    def Three_in_a_column(self,column):
        for i in (range(len(column[0]))):
            if ((column[0][i] == column[1][i]) and (column[1][i] == column[2][i])):
                if (not (column[0][i] == 0)):
                    return column[0][i]
        return None

    # Checks the diagonals to see if something is there
    def Diagonals(self,Chart):
        if ((Chart[0][0] == Chart[1][1]) and (Chart[1][1] == Chart[2][2])):
            if (not (Chart[0][0] == 0)):
                return Chart[0][0]
        elif ((Chart[0][2] == Chart[1][1]) and (Chart[1][1] == Chart[2][0])):
            if (not (Chart[1][1] == 0)):
                return Chart[1][1]
        else:
            return None

    # Checks if we have a winner
    def No_one_wins(self,Game_board,Print_fn_object,Variable_object):
        Horizontal = self.Three_in_a_row(Game_board)
        Vertical = self.Three_in_a_column(Game_board)
        Diagonal = self.Diagonals(Game_board)

        if ((not (Horizontal is None)) and (not(Horizontal == 0))):
            Print_fn_object.print_board(Variable_object)
            print('Player', Horizontal, 'wins!')
            return False
        elif ((not (Vertical is None)) and (not(Horizontal == 0))):
            Print_fn_object.print_board(Variable_object)
            print('Player', Vertical, 'wins!')
            return False
        elif ((not (Diagonal is None)) and (not (Diagonal == 0))):
            Print_fn_object.print_board(Variable_object)
            print('Player', Diagonal, 'wins!')
            return False
        else:
            return True

    # this checks to see if all spots are filled up
    def All_Filled_Up(self,available_spots):
        Row_1 = ((not available_spots[0][0]) and (not available_spots[0][1]) and (not available_spots[0][2]))
        Row_2 = ((not available_spots[1][0]) and (not available_spots[1][1]) and (not available_spots[1][2]))
        Row_3 = ((not available_spots[2][0]) and (not available_spots[2][1]) and (not available_spots[2][2]))

        return (Row_1 and Row_2 and Row_3)

    # We reset the boards that store the numbers and booleans
    def Reset_the_board(self, Variable_object):

        for i in (range(len(Variable_object.Array_of_available_spots))):
            for j in (range(len(Variable_object.Array_of_available_spots[i]))):
                Variable_object.Array_of_available_spots[i][j] = True
                Variable_object.Array_of_player_pieces[i][j] = 0
