import game_tracking_variables
class InputFunctions:
    """
        This class is for functions that read in data from the user.
    """

    #Name: In_Combinations
    def coordinates_in_combinations(self,x,game_variable_object):
        """
            This helper function checks if a set of coordinates is in the allowed
            combinations.
        """
        # run a loop through the instance_all_valid_coordinate_combinations instance variable to
        # see if the coordinate is in there. When found return true, otherwise return false
        for i in range(len(game_variable_object.instance_all_valid_coordinate_combinations)):
            if (x.casefold() == (game_variable_object.instance_all_valid_coordinate_combinations[i].casefold())):
                return True
        return False

    def enter_coordinates(self,xturn,game_variable_object,multi_player):
        """
            This function takes in and validates coordinate inputs from the user, as
            far as whether it's a valid coordinate input in itself.
        """
        # Take input from the user displaying the according messages if  they're in
        # single player or multi-player mode.
        if multi_player:
            if xturn:
                coordinates = input('Player 1 (X), enter a set of coordinates.\nEnter the row first, then the column: ')
                while (not(self.coordinates_in_combinations(coordinates,game_variable_object))):
                    coordinates = input('This coordinate does not exist. Enter another set of coordinates: ')
            else:
                coordinates = input('Player 2 (O), enter a set of coordinates.\nEnter the row first, then the column: ')
                while (not(self.coordinates_in_combinations(coordinates,game_variable_object))):
                    coordinates = input('This coordinate does not exist. Enter another set of coordinates: ')
        else:
            if xturn:
                coordinates = input("Enter a set of coordinates (you're X): ")
                while (not(self.coordinates_in_combinations(coordinates,game_variable_object))):
                    coordinates = input('This coordinate does not exist. Enter another set of coordinates: ')
            else:
                coordinates = input("Enter a set of coordinates (you're O): ")
                while (not(self.coordinates_in_combinations(coordinates,game_variable_object))):
                    coordinates = input('This coordinate does not exist. Enter another set of coordinates: ')
        return coordinates

    def nothing_there(self,whos_turn,game_variable_object,multi_player):
        """
            This function takes in coordinates and ensures the spot is not taken on the
            board. It will ask again until a valid input is entered.
        """
        # Get a coordinate from the user and check if it's a valid input given the current
        # state - both if it's a valid coordinate and the spot's not taken
        coordinates = list(self.enter_coordinates(whos_turn,game_variable_object,multi_player))
        first_index = game_variable_object.instance_letter_legend[coordinates[0].upper()]
        not_there = game_variable_object.instance_array_of_available_spots[first_index - 1][(int(coordinates[1])) - 1]
        # You're stuck in this loop till you give adequate input
        while(not not_there):
            print('Sorry, that spot\'s taken. Choose another one.')
            coordinates = list(self.enter_coordinates(whos_turn,game_variable_object,multi_player))
            first_index = game_variable_object.instance_letter_legend[coordinates[0].upper()]
            not_there = game_variable_object.instance_array_of_available_spots[first_index - 1][(int(coordinates[1])) - 1]
        coordinates[0] = coordinates[0].upper()
        return coordinates

    def who_starts_first(self,multi_player):
        """
            This determines who starts first, based on your input, as well as
            determines which piece you will be if you choose to play against the computer.
        """
        # Based on the mode, prompt the user for input to decide what player they want to be:
        # X or O? Prompt input from them till it's correct.
        player_1_or_2 = None
        player_start_options = ['1', '2']
        if (multi_player):
            player_1_or_2 = input('Enter who starts first. 1 for player 1 (X), 2 for player 2 (O): ')
            while (not(player_1_or_2 in player_start_options)):
                player_1_or_2 = input('Invalid input. Enter a 1 or a 2: ')
            if (player_1_or_2 == player_start_options[0]):
                return True
            return False
        else:
            player_1_or_2 = input('Enter 1 to be X, enter 2 to be O: ')
            while (not(player_1_or_2 in player_start_options)):
                player_1_or_2 = input('Invalid input. Enter a 1 or a 2: ')
            if (player_1_or_2 == player_start_options[0]):
                return True
            return False

    def keep_playing(self):
        """
            This function would determine whether the user would want to keep playing,
            based on them typing 'y' for yes or 'n' for no. It's no longer in use given
            the way our game is structured, so ignore this function.
        """
        # Prompt input corresponding to yes or no, and repeat this until the input is valid.
        yes_or_no = ['y', 'n']
        keep_playing = input('Keep playing? \'Y\' for yes, \'N\' for No: ')
        while (not ((keep_playing.lower()) in yes_or_no)):
            keep_playing = input('Invalid Entry. Enter \'Y\' for yes, \'N\' for No: ')

        if ((keep_playing.casefold()) == ('y'.casefold())):
            return True
        else:
            return False
