import game_tracking_variables

class PrintFunctions:
    """
        This is our class for all methods that print out to the machine, namely,
        they only print out values, and do not interact with our user - not input
        functions.
    """
    def print_board(self,game_variable_object):
        """
            This function prints the output of the board to the screen.
        """
        print_string = ''
        for board_row in game_variable_object.instance_board:
            # Add the individual character strings and print them, before setting
            # the string to empty and starting from the next list within the list of lists
            for i in range(len(board_row)):
                print_string += board_row[i]
            print(print_string)
            print_string = ''

    def find_the_y_coordinate(self,y_coordinate,game_variable_object):
        """
            We use the first part of our coordinate (that represents the y coordinate)
            to find the appropriate row in our 2-dimensional board list in the
            game_tracking_variables class to then mutate to.
        """
        for i in (range(len(game_variable_object.instance_board))):
            # parse through the instance board to find if the y coordinate matches the start of our list
            # of lists of strings (the first character in this list of strings)
            if ((y_coordinate.casefold()) == (game_variable_object.instance_board[i][0].casefold())):
                return i
        return 0

    def add_an_X(self,coordinates,game_variable_object):
        """
            This function adds an X to the board at the appropriate location in
            the instance_board array of our game_tracking_variables class, based on the
            coordinates entered here.
        """
        # Find the x and y indices to then change the list to have the X on the board where it should be.
        x_index = game_variable_object.instance_translate_input_to_board_index[int(coordinates[1])]
        y_index = self.find_the_y_coordinate(coordinates[0],game_variable_object)
        game_variable_object.instance_board[y_index][x_index] = '\\'
        game_variable_object.instance_board[y_index][x_index + 1] = '/'
        game_variable_object.instance_board[y_index + 1][x_index] = '/'
        game_variable_object.instance_board[y_index + 1][x_index + 1] = '\\'

    def add_an_O(self,coordinates,game_variable_object):
        """
            This function adds an O to the instance_board at the appropriate location in
            the board array of our game_tracking_variables class, based on the
            coordinates entered here.
        """
        # Find the x and y indices to then change the list to have the O on the board where it should be.
        x_index = game_variable_object.instance_translate_input_to_board_index[int(coordinates[1])]
        y_index = self.find_the_y_coordinate(coordinates[0],game_variable_object)
        game_variable_object.instance_board[y_index][x_index] = '/'
        game_variable_object.instance_board[y_index][x_index + 1] = '\\'
        game_variable_object.instance_board[y_index + 1][x_index] = '\\'
        game_variable_object.instance_board[y_index + 1][x_index + 1] = '/'

    #Name: Mutate_Board
    def change_game_state(self,game_variable_object,coordinates):
        """
            This function is responsible for changing the state of the current game
            by mutating the list we print out, as well as mutating the list of the available
            spots and the list representing the current status of instance_board pieces.
        """
        # Make this spot on the board unavailable
        game_variable_object.instance_array_of_available_spots\
        [game_variable_object.instance_letter_legend[coordinates[0].upper()] - 1]\
        [(int(coordinates[1])) - 1] = False

        # If it's the turn of the X value, put a X on the board in the right spot,
        # otherwise put an O there instead
        if game_variable_object.instance_turn_of_x_char_or_not:
            game_variable_object.instance_current_status_of_board_pieces\
            [game_variable_object.instance_letter_legend[coordinates[0].upper()] - 1]\
            [(int(coordinates[1])) - 1] = 1
            self.add_an_X(coordinates,game_variable_object)
        else:
            game_variable_object.instance_current_status_of_board_pieces\
            [game_variable_object.instance_letter_legend[coordinates[0].upper()] - 1]\
            [(int(coordinates[1])) - 1] = 2
            self.add_an_O(coordinates,game_variable_object)

    # Name: clear_the_board
    def clear_the_board(self,game_variable_object):
        """
            This function is responsible for clearing the board when the game finishes.
        """
        # Run a for loop to clear the spots where there are X and O values
        for i in (range(len(game_variable_object.instance_all_valid_coordinates))):
            for j in (range(len(game_variable_object.instance_all_valid_coordinates[i]))):
                x_index = game_variable_object.instance_all_valid_coordinates[i][j][1]
                y_index = self.find_the_y_coordinate(game_variable_object.instance_all_valid_coordinates[i][j][0],game_variable_object)
                game_variable_object.instance_board[y_index][x_index] = ' '
                game_variable_object.instance_board[y_index][x_index + 1] = ' '
                game_variable_object.instance_board[y_index + 1][x_index] = ' '
                game_variable_object.instance_board[y_index + 1][x_index + 1] = ' '
