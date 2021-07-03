import game_tracking_variables
from print_methods import PrintFunctions


def all_3_equal(row):
    """
        This function returns a boolean expression checking the row
        having all equal elements.

        Arguments:
        row: list of 3 integers

        Time Complexity: O(1) - List accessing (L[0]) is O(1), boolean operators
        are O(1)
    """
    return ((row[0] == row[1]) and (row[1] == row[2]))

def three_in_a_row(board):
    """
        This function checks all 3 rows to see if we have 3 in a row. Returns
        the integer that was found 3 times in a row, returns None otherwise.

        Arguments:
        board: list of 3 lists, each with 3 integers that are either 0, 1 or 2

        Time Complexity: O(n) runtime where n is the number of elements in the
        list board (3)
    """
    for row in board:
        if (all_3_equal(row)) and bool(row[0]):
            return row[0]

def three_in_a_column(board):
    """
        This function checks all 3 columns to see if we have 3 in a column.
        Returns the integer if it is not 0, returns None otherwise

        Arguments:
        board: list of 3 lists, each with 3 integers that are either 0, 1 or 2

        Time Complexity: O(n) runtime where n is the number of elements in the
        list board. Since there are always 3 lists in the board, this always runs
        in constant time.
    """
    for i in (range(len(board[0]))):
        if (board[0][i] == board[1][i]) and (board[1][i] == board[2][i]) \
            and bool(board[0][i]):
            return board[0][i]

def diagonals(board):
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

def somebody_wins(board):
    """
        This function checks to see if we have a winner, returning true if
        nobody won, false otherwise.

        Arguments:
        board: list of 3 lists, each with 3 integers that are either 0, 1 or 2
    """
    horizontal = three_in_a_row(board)
    vertical = three_in_a_column(board)
    diagonal = diagonals(board)
    return bool(horizontal) or bool(vertical) or bool(diagonal)

def all_filled_up(array_of_available_spots):
    """
        This function checks to see if all spots are filled up.
    """
    not_filled_up = True
    for row in array_of_available_spots:
        for item in row:
            not_filled_up = not_filled_up and not item
    return not_filled_up
