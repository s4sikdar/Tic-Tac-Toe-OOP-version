import game_tracking_variables
from print_methods import PrintFunctions

class Checker:
    """
        This class is for our checker functions, which monitor
        the status of the game (i.e. if someone won, etc.).
    """

    # Name: true across
    def all_3_equal(self,row):
        """
            This function returns a boolean expression checking the row
            having all equal elements.
        """
        return ((row[0] == row[1]) and (row[1] == row[2]))

    # Checks all of the three rows to see if we have three in a row
    def three_in_a_row(self,board):
        """
            This function checks all 3 rows to see if we have 3 in a row.
        """
        for i in (range(len(board))):
            if (self.all_3_equal(board[i])):
                if (not (board[i][0] == 0)):
                    return board[i][0]
        return None

    # Checks all of the three columns to see if we have three in a column
    def three_in_a_column(self,board):
        """
            This function checks all 3 columns to see if we have 3 in a column.
        """
        for i in (range(len(board[0]))):
            if ((board[0][i] == board[1][i]) and (board[1][i] == board[2][i])):
                if (not (board[0][i] == 0)):
                    return board[0][i]
        return None

    # Checks the diagonals to see if something is there
    def diagonals(self,board):
        """
            This function checks to see if we have 3 in a row diagonally.
        """
        if ((board[0][0] == board[1][1]) and (board[1][1] == board[2][2])):
            if (not (board[0][0] == 0)):
                return board[0][0]
        elif ((board[0][2] == board[1][1]) and (board[1][1] == board[2][0])):
            if (not (board[1][1] == 0)):
                return board[1][1]
        else:
            return None

    # Checks if we have a winner
    # no_one_wins(self,Game_board,Print_fn_object,Variable_object):
    def no_one_wins(self,print_fn_object,variable_object):
        """
            This function checks to see if we have a winner, returning true if
            nobody won, false otherwise.
        """
        horizontal = self.three_in_a_row(variable_object.instance_current_status_of_board_pieces)
        vertical = self.three_in_a_column(variable_object.instance_current_status_of_board_pieces)
        diagonal = self.diagonals(variable_object.instance_current_status_of_board_pieces)

        if ((not (horizontal is None)) and (not(horizontal == 0))):
            print_fn_object.print_board(variable_object)
            print('Player', horizontal, 'wins!')
            return False
        elif ((not (vertical is None)) and (not(horizontal == 0))):
            print_fn_object.print_board(variable_object)
            print('Player', vertical, 'wins!')
            return False
        elif ((not (diagonal is None)) and (not (diagonal == 0))):
            print_fn_object.print_board(variable_object)
            print('Player', diagonal, 'wins!')
            return False
        else:
            return True

    # this checks to see if all spots are filled up
    def all_filled_up(self,available_spots_left):
        """
            This function checks to see if all spots are filled up.
        """
        row_1 = ((not available_spots_left[0][0]) and (not available_spots_left[0][1]) and (not available_spots_left[0][2]))
        row_2 = ((not available_spots_left[1][0]) and (not available_spots_left[1][1]) and (not available_spots_left[1][2]))
        row_3 = ((not available_spots_left[2][0]) and (not available_spots_left[2][1]) and (not available_spots_left[2][2]))

        return (row_1 and row_2 and row_3)

    # We reset the boards that store the numbers and booleans
    def reset_the_board(self, variable_object):
        """
            This function resets the boards in the variable object that track
            the current status of the game (what players are positioned where,
            what spots are taken).
        """
        for i in (range(len(variable_object.instance_array_of_available_spots))):
            for j in (range(len(variable_object.instance_array_of_available_spots[i]))):
                variable_object.instance_array_of_available_spots[i][j] = True
                variable_object.instance_current_status_of_board_pieces[i][j] = 0
