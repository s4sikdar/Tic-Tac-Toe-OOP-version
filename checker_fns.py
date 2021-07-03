import game_tracking_variables
from print_methods import PrintFunctions

class Checker:
    """
        This class is for our checker functions, which monitor
        the status of the game (i.e. if someone won, etc.).
    """

    def all_3_equal(self,row):
        """
            This function returns a boolean expression checking the row
            having all equal elements.

            Arguments:
            row: list of 3 integers

            Time Complexity: O(1) - List accessing (L[0]) is O(1), boolean operators
            are O(1)
        """
        return ((row[0] == row[1]) and (row[1] == row[2]))

    def three_in_a_row(self,board):
        """
            This function checks all 3 rows to see if we have 3 in a row. Returns
            the integer that was found 3 times in a row, returns None otherwise.

            Arguments:
            board: list of 3 lists, each with 3 integers that are either 0, 1 or 2

            Time Complexity: O(n) runtime where n is the number of elements in the
            list board (3)
        """
        for row in board:
            if (self.all_3_equal(row)) and bool(row[0]):
                return row[0]

    def three_in_a_column(self,board):
        """
            This function checks all 3 columns to see if we have 3 in a column.
            Returns the integer if it is not 0, returns None otherwise

            Arguments:
            board: list of 3 lists, each with 3 integers that are either 0, 1 or 2

            Time Complexity: O(n) runtime where n is the number of elements in the
            list board (3)
        """
        for i in (range(len(board[0]))):
            if (board[0][i] == board[1][i]) and (board[1][i] == board[2][i]) \
                and bool(board[0][i]):
                return board[0][i]

    def diagonals(self,board):
        """
            This function checks to see if we have 3 numbers in a row
            diagonally on a list of 3 lists of numbers. Returns the number
            that matches this condition if it isn't 0. Returns None otherwise.

            Arguments:
            board: list of 3 lists, each with 3 integers that are either 0, 1 or 2

            Time Complexity: O(1) - List accessing (L[0]) is O(1), boolean operators
            and boolean conversions are all O(1)
        """
        if ((board[0][0] == board[1][1]) and (board[1][1] == board[2][2])) \
            and bool(board[1][1]):
            return board[0][0]
        elif ((board[0][2] == board[1][1]) and (board[1][1] == board[2][0])) \
            and bool(board[1][1]):
            return board[1][1]

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

    def all_filled_up(self,available_spots_left):
        """
            This function checks to see if all spots are filled up.
        """
        row_1 = ((not available_spots_left[0][0]) and (not available_spots_left[0][1]) and (not available_spots_left[0][2]))
        row_2 = ((not available_spots_left[1][0]) and (not available_spots_left[1][1]) and (not available_spots_left[1][2]))
        row_3 = ((not available_spots_left[2][0]) and (not available_spots_left[2][1]) and (not available_spots_left[2][2]))

        return (row_1 and row_2 and row_3)

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
