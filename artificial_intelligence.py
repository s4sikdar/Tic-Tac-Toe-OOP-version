from pdb import set_trace
import game_tracking_variables
from utils import checker_utils
import sys

# This class is for our AI that comes up with the right moves using the minimax
# algorithm. There's no need for an __init__ constructor since there are no
# class variables that need to be declared
class TheAIProgram:
    """
        This class is responsible for the artificial intelligence component for the
        single player version of the game - playing against the computer.
    """

    def __init__(self):
        # Used for which directions to check for an unblocked row of 2. Used in fork_helper
        self.instance_directions = {
            'horizontal': True,
            'vertical': True,
            'diagonal_1': True,
            'diagonal_2': True
        }
        self.instance_player_spots = {
            1: [],
            2: []
        }

    def clean(self):
        """
            Used to "clean" the directions dictionary for when we wish to use it the next
            time.
        """
        for direc in self.instance_directions:
            self.instance_directions[direc] = True

    def clean_at_end_decorator(func):
        """
            Used to make sure that the clean method cleans our directions dictionary after
            functions are run, by using this function as a decorator. Only use this for
            functions that use and modify self.instance_directions, and are attached with an object
            instance (reference to the object - self - is the first argument passed).
        """
        # Originally tried this on my own, couldn't figure out how to pass the self argument
        # first, found this solution on Stack Overflow:
        # https://stackoverflow.com/questions/1263451/python-decorators-in-classes
        def decorated_func(self, *args, **kwargs):
            return_val = func(self, *args, **kwargs)
            self.clean()
            return return_val
        return decorated_func

    def all_the_same_values(self,number,player_pieces):
        """
            This checks if all 3 numbers are the same across a row of 3, and they
            equal the number in question.
        """
        all_equal = (number == player_pieces[0])\
                     and (checker_utils.all_3_equal(player_pieces))
        return all_equal


    def three_in_a_row_at_this_spot(self,current_player_number,\
                                    pieces_on_board,current_coordinate, return_rows=False):
        """
            This checks if we have 3 in a row across any possible rows of 3 at
            the coordinate in question.
        """
        # Whether or not we found 3 in a row in these directions:
        # We do only the horizontal and vertical directions since we haven't checked
        # where we are at diagonally, meaning that we may be checking for 3 in a row diagonally, which
        # is invalid with this coordinate. So if you have a 3 x 3 list of lists, and you are in the
        # second element of the first list, there's no diagonal set of 3 you can reach. To visualize,
        # look wherer the 1 representing the current coordinate is in the 3x3 list below:
        # [[0, 1, 0],
        #  [0, 0, 0],
        #  [0, 0, 0]]
        horzontal_row_of_3 = self.all_the_same_values(current_player_number,\
                                                      pieces_on_board[current_coordinate[0]])
        vertical_row_of_3 = self.all_the_same_values(current_player_number,\
                                                    [pieces_on_board[0][current_coordinate[1]],\
                                                     pieces_on_board[1][current_coordinate[1]],\
                                                     pieces_on_board[2][current_coordinate[1]]])
        returned_rows = []
        if return_rows:
            if horzontal_row_of_3:
                returned_rows.append([
                    [current_coordinate[0], 0],
                    [current_coordinate[0], 1],
                    [current_coordinate[0], 2]
                ])
            elif vertical_row_of_3:
                returned_rows.append([
                    [0, current_coordinate[1]],
                    [1, current_coordinate[1]],
                    [2, current_coordinate[1]]
                ])

        # [[1, 0, 0],
        #  [0, 0, 0],
        #  [0, 0, 1]]
        # Here the 1 represents where current_coordinate could be at. So we
        # have to recreate the array going in the diagonal direction to pass into
        # the helper function
        if current_coordinate in [[0,0],[2,2]]:
            diagonal = self.all_the_same_values(current_player_number,\
                                                 [pieces_on_board[0][0],\
                                                  pieces_on_board[1][1],\
                                                  pieces_on_board[2][2]]) 
            if not return_rows:
                return (horzontal_row_of_3 or vertical_row_of_3 or diagonal)
            else:
                if diagonal:
                    returned_rows.append([[0, 0], [1, 1], [2, 2]])

        # [[0, 0, 1],
        #  [0, 0, 0],
        #  [1, 0, 0]]
        # Here the 1 represents where current_coordinate could be at. So we
        # have to recreate the array going in the opposite diagonal to pass into
        # the helper function
        elif current_coordinate in [[0,2],[2,0]]:
            diagonal = self.all_the_same_values(current_player_number,\
                                               [pieces_on_board[0][2],\
                                                pieces_on_board[1][1],\
                                                pieces_on_board[2][0]])
            if not return_rows:
                return (horzontal_row_of_3 or vertical_row_of_3 or diagonal)
            else:
                if diagonal:
                    returned_rows.append([[0, 2], [1, 1], [2, 0]])

        # [[0, 1, 0],
        #  [1, 0, 1],
        #  [0, 1, 0]]
        # Here we're in any of the spots where there's a one. So we only check vertically or horizontally.
        elif current_coordinate in [[0,1],[1,0],[1,2],[2,1]]:
            if not return_rows:
                return (horzontal_row_of_3 or vertical_row_of_3)

        # [[0, 0, 0],
        #  [0, 1, 0],
        #  [0, 0, 0]]
        # Here the 1 represents current_coordinate on the board. Since we're in the middle,
        # we check 4 directions now.
        else:
            diagonal = checker_utils.diagonals(pieces_on_board) == current_player_number
            if not return_rows:
                return (horzontal_row_of_3 or vertical_row_of_3 or diagonal)
            else:
                if diagonal:
                    diagonal_1 = self.all_the_same_values(current_player_number,\
                                                         [pieces_on_board[0][0],\
                                                          pieces_on_board[1][1],\
                                                          pieces_on_board[2][2]])
                    diagonal_2 = self.all_the_same_values(current_player_number,\
                                                         [pieces_on_board[0][2],\
                                                          pieces_on_board[1][1],\
                                                          pieces_on_board[2][0]])
                if diagonal and diagonal_1:
                    returned_rows.append([[0, 0], [1, 1], [2, 2]])
                if diagonal and diagonal_2:
                    returned_rows.append([[0, 2], [1, 1], [2, 0]])
        if return_rows:
            return returned_rows


    def blocked_row_of_2(self,current_player_number,\
                         opposite_player_number,player_pieces):
        """
            This function takes in 2 numbers to look for: the current player's number,
            the other player's number, and our array of 3 on the board. We check if we
            have a combination of 2 and 1 for the opposite player's number and the current
            player's number respectively. This in effect checks to see if we blocked a row of
            2 about to be a row of 3, had we not put our piece here. This function is called
            with the two numbers switched in the order they are entered as arguments, to signify
            turns by the computer vs the other individual.
        """
        current_number_frequency = 0
        opposite_number_frequency = 0

        for i in (range(len(player_pieces))):
            if (player_pieces[i] == current_player_number):
                current_number_frequency += 1
            elif (player_pieces[i] == opposite_player_number):
                opposite_number_frequency += 1

        if ((current_number_frequency == 1) and (opposite_number_frequency == 2)):
            return True
        return False


    def block(self,current_coordinate,player_pieces_array,current_player_number,\
              opposite_player_number):
        """
            Block takes in a current player number, the other number (what to use for blocked row of 2),
            a coordinate, and the array of numbers to use. From our coordinate we see if we have
            blocked any rows of 2, depending on where we are starting from. We will use this to find
            it such that it's main number once, and the opposite number twice. So if you're X,
            you're 1. So if you have [O,O,X], then it registers as [2,2,1], where 1 is the main
            number (number) and 2 is the other number (other_number). So we use the function a
            few lines above that found this to then determine if it's a block.
        """
        # used as a boolean if we found a block that we'e looking for.
        its_a_block = False
        # Whether or not we found a block in these directions:
        # We do only the horizontal and vertical directions since we haven't checked
        # where we are at diagonally, in that we may be checking a diagonal direction that
        # is invalid with this coordinate. So if you have a 3 x 3 list of lists, and you are in the
        # second element of the first list, there's no diagonal set of 3 you can reach. To visualize,
        # look wherer the 1 is in the 3x3 list below:
        # [[0, 1, 0],
        #  [0, 0, 0],
        #  [0, 0, 0]]
        # Trying to do the diagonal rows of 3 here makes no sense and throws us an error.
        horizontal_blocked_row_of_2 = self.blocked_row_of_2(current_player_number,opposite_player_number,\
                                                            player_pieces_array[current_coordinate[0]])
        vertical_blocked_row_of_2 =  self.blocked_row_of_2(current_player_number,opposite_player_number,\
                                                          [player_pieces_array[0][current_coordinate[1]],\
                                                           player_pieces_array[1][current_coordinate[1]],\
                                                           player_pieces_array[2][current_coordinate[1]]])
        diagonal_arr_1 = [player_pieces_array[0][0],player_pieces_array[1][1],player_pieces_array[2][2]]
        diagonal_arr_2 = [player_pieces_array[2][0],player_pieces_array[1][1],player_pieces_array[0][2]]
        # [[1, 0, 0],
        #  [0, 0, 0],
        #  [0, 0, 1]]
        # Here the 1 represents where current_coordinate could be at. So we
        # have to recreate the array going in the diagonal direction to pass into
        # the helper function
        if current_coordinate in [[0,0], [2,2]]:
            its_a_block = horizontal_blocked_row_of_2 or vertical_blocked_row_of_2 or\
                         (self.blocked_row_of_2(current_player_number,
                                                opposite_player_number,
                                                diagonal_arr_1))
            return its_a_block

        # [[0, 0, 1],
        #  [0, 0, 0],
        #  [1, 0, 0]]
        # Here the 1 represents where current_coordinate could be at. So we
        # have to recreate the array going in the opposite diagonal to pass into
        # the helper function
        elif current_coordinate in [[0,2],[2,0]]:
            its_a_block = vertical_blocked_row_of_2 or horizontal_blocked_row_of_2 or \
                         (self.blocked_row_of_2(current_player_number,
                                                opposite_player_number,
                                                diagonal_arr_2))
            return its_a_block

        # [[0, 0, 0],
        #  [0, 1, 0],
        #  [0, 0, 0]]
        # Here the 1 represents current_coordinate on the board. Since we're in the middle,
        # we check 4 directions now.
        elif current_coordinate == [1,1]:
            its_a_block = horizontal_blocked_row_of_2 or vertical_blocked_row_of_2 or \
                          (self.blocked_row_of_2(current_player_number,opposite_player_number,
                                                 diagonal_arr_1)) or \
                          (self.blocked_row_of_2(current_player_number,opposite_player_number,
                                                 diagonal_arr_2))

            return its_a_block

        # [[0, 1, 0],
        #  [1, 0, 1],
        #  [0, 1, 0]]
        # Here we're in any of the spots where there's a one. So we only check vertically or horizontally.
        else:
            its_a_block = horizontal_blocked_row_of_2 or vertical_blocked_row_of_2
            return its_a_block


    def two_in_a_row(self,current_player_number,player_pieces):
        """
            This helper function is used in our fork function, to check if we have 2
            of the same pieces in a row, that are unblocked.
        """
        times_number = 0
        times_0 = 0

        # so we iterate through the current row of 3 to see if we have the right
        # combination of 2 in a row for our number, and a 0 representing an empty space
        for i in (range(len(player_pieces))):
            if (player_pieces[i] == current_player_number):
                times_number += 1
            elif (player_pieces[i] == 0):
                times_0 += 1

        if ((times_number == 2) and (times_0 == 1)):
            return True
        return False


    def fork_helper(self,current_player_number,current_coordinate,\
                     player_pieces_array,directions):
        """
            Fork helper takes in a coordinate, array, 3 boolean values for the vertical,
            horizontal, and diagonal directions and checks where the coordinates are
            that give us 2 of our pieces in a row unblocked at our present coordinate.
            We then give back a list of indices for the row wherever we found the 2 in a row.
            We use the booleans to "turn off a direction" and look for two in a
            row in other directions. For example, this function could find 2 in a row horizontally,
            and if we don't turn the horizontal direction off, it'll just return the same row of
            indices in the same direction again. This is used as a helper function to another function
            that determines if we have a fork (2 unblocked rows of 2).
        """
        # Whether or not we found two in a row in these directions:
        # We do only the horizontal and vertical directions since we haven't checked
        # where we are at diagonally, in that we may be checking a diagonal direction that
        # is invalid with this coordinate. So if you have a 3 x 3 list of lists, and you are in the
        # second element of the first list, there's no diagonal set of 3 you can reach. To visualize,
        # look wherer the 1 is in the 3x3 list below:
        # [[0, 1, 0],
        #  [0, 0, 0],
        #  [0, 0, 0]]
        # Here we found 2 in a row horizontally
        horizontal_2_in_a_row = self.two_in_a_row(current_player_number, player_pieces_array[current_coordinate[0]])
        # Here we found 2 in a row vertically
        vertical_2_in_a_row = self.two_in_a_row(current_player_number,\
                                               [player_pieces_array[0][current_coordinate[1]],\
                                                player_pieces_array[1][current_coordinate[1]],\
                                                player_pieces_array[2][current_coordinate[1]]])

        # Based on the coordinate, we check the according available rows of 3 to see
        # if we have two in a row here, and everything holds.
        # [[1, 0, 0],
        #  [0, 0, 0],
        #  [0, 0, 1]]
        # Here the 1 represents where current_coordinate could be at. So we
        # have to recreate the array going in the diagonal direction to pass into
        # the two_in_a_row function
        if current_coordinate in [[0,0],[2,2]]:
            # If there are 2 in a row in the appropriate directions and the boolean for that direction is true,
            # we just found a new undiscovered row of 2. The same applies below.
            if (horizontal_2_in_a_row and directions.get('horizontal')):
                return [[current_coordinate[0],0],[current_coordinate[0],1],[current_coordinate[0],2]]
            elif (vertical_2_in_a_row and directions.get('vertical')):
                return [[0,current_coordinate[1]],[1,current_coordinate[1]],[2,current_coordinate[1]]]
            elif ((self.two_in_a_row(current_player_number,\
                                    [player_pieces_array[0][0],\
                                     player_pieces_array[1][1],\
                                     player_pieces_array[2][2]])) and directions.get('diagonal_1')):
                return [[0,0],[1,1],[2,2]]
            else:
                return []

        # [[0, 0, 1],
        #  [0, 0, 0],
        #  [1, 0, 0]]
        # Here the 1 represents where current_coordinate could be at. So we
        # have to recreate the array going in the opposite diagonal to pass into
        # the two_in_a_row function
        elif current_coordinate in [[0,2],[2,0]]:
            if (horizontal_2_in_a_row and directions.get('horizontal')):
                return [[current_coordinate[0],0],[current_coordinate[0],1],[current_coordinate[0],2]]
            elif (vertical_2_in_a_row and directions.get('vertical')):
                return [[0,current_coordinate[1]],[1,current_coordinate[1]],[2,current_coordinate[1]]]
            elif ((self.two_in_a_row(current_player_number,\
                                    [player_pieces_array[0][2],\
                                     player_pieces_array[1][1],\
                                     player_pieces_array[2][0]])) and directions.get('diagonal_2')):
                return [[0,2],[1,1],[2,0]]
            else:
                return []

        # [[0, 0, 0],
        #  [0, 1, 0],
        #  [0, 0, 0]]
        # Here the 1 represents current_coordinate on the board. Since we're in the middle,
        # we check 4 directions now.
        elif (current_coordinate == [1,1]):
            if (horizontal_2_in_a_row and directions.get('horizontal')):
                return [[current_coordinate[0],0],[current_coordinate[0],1],[current_coordinate[0],2]]
            elif (vertical_2_in_a_row and directions.get('vertical')):
                return [[0,current_coordinate[1]],[1,current_coordinate[1]],[2,current_coordinate[1]]]
            elif ((self.two_in_a_row(current_player_number,\
                                    [player_pieces_array[0][0],\
                                     player_pieces_array[1][1],\
                                     player_pieces_array[2][2]])) and directions.get('diagonal_1')):
                return [[0,0],[1,1],[2,2]]
            elif ((self.two_in_a_row(current_player_number,\
                                    [player_pieces_array[0][2],\
                                     player_pieces_array[1][1],\
                                     player_pieces_array[2][0]])) and directions.get('diagonal_2')):
                return [[0,2],[1,1],[2,0]]
            else:
                return []

        # [[0, 1, 0],
        #  [1, 0, 1],
        #  [0, 1, 0]]
        # Here we're in any of the spots where there's a one. So we only check vertically or horizontally.
        else:
            if (horizontal_2_in_a_row and directions.get('horizontal')):
                return [[current_coordinate[0],0],[current_coordinate[0],1],[current_coordinate[0],2]]
            elif (vertical_2_in_a_row and directions.get('vertical')):
                return [[0,current_coordinate[1]],[1,current_coordinate[1]],[2,current_coordinate[1]]]
            else:
                return []

    @clean_at_end_decorator
    def fork(self,current_coordinate,player_pieces_array,current_player_number):
        """
            A fork is where we have 2 unblocked rows of 2. By definition we could have
            2 separate unblocked rows of 2, though this will not happen by the design
            of our algorithm, as if there would be 4 pieces used when the player could just win on
            the third turn if it's not blocked (if we have row 1 and 3 are filled with
            2 in a row, if for argument's sake they're never blocked, then we could win
            on the 3rd or 4th turn). For this reason, all our forks will be 2 connected
            unblocked rows of 2. We have a coordinate and we check if we have 2 unblocked
            rows of 2 from this coordinate.
        """
        # Find any unblocked rows of 2
        first_set_of_2_in_a_row = self.fork_helper(current_player_number,\
                                                   current_coordinate,\
                                                   player_pieces_array,\
                                                   self.instance_directions)
        # The second set of 2 that is unblocked and hasn't been found already
        second_set_of_2 = []
        # If the first list returned from fork_helper was non empty then look for the second
        # list. Otherwise return false like the very bottom else case.
        if ((len(first_set_of_2_in_a_row)) != 0):
            if first_set_of_2_in_a_row == [[0,0],[1,1],[2,2]]:
                # So if we found a diagonal row of 2, then we look through each coordinate
                # in the row of 3 and find the next unblocked row of 2 with the diagonal
                # direction switch turned off
                self.instance_directions.update({'diagonal_1': False})
            elif first_set_of_2_in_a_row == [[0,2],[1,1],[2,0]]:
                self.instance_directions.update({'diagonal_2': False})
            elif ((first_set_of_2_in_a_row[0][0] == first_set_of_2_in_a_row[1][0]) and \
                  (first_set_of_2_in_a_row[1][0] == first_set_of_2_in_a_row[2][0])):
                # If our set of 2 in a row was horizontal, turn off that direction,
                # and look for the next unblocked row of 2.
                self.instance_directions.update({'horizontal': False})
            else:
                self.instance_directions.update({'vertical': False})
            for i in (range(len(first_set_of_2_in_a_row))):
                coordinate = first_set_of_2_in_a_row[i]
                # If you have 2 pieces in a row that are unblocked, the third piece is 0.
                # This means that for you to have 2 in a row here, in all directions
                # where you have possibly 3 in a row, the other 2 pieces have to be filled
                # with the same number. So you would have to spend 4 moves to get 2 unblocked
                # rows of 2, and would have something like this:
                # [
                #  [1, 1, 0]
                #  [0, 0, 1]
                #  [0, 0, 1]
                # ]
                # A logical player that wants to win as fast as possible would not do this,
                # as they could win by the 3rd move and definitely by the fourth move if no
                # resistance was offered. So we don't have to compute the self.fork_helper
                # for the 0 in the top right corner, as I can't logically think of a way
                # that you would have a situation where the empty spot has 2 in a row in a
                # different direction with only 3 pieces (the diagram above is done in 3
                # moves)
                if player_pieces_array[coordinate[0]][coordinate[1]]:
                    second_set_of_2 = self.fork_helper(current_player_number,\
                                                        coordinate,\
                                                        player_pieces_array,\
                                                        self.instance_directions)
                # If we get here, we found a second unblocked row of 2 that is connected
                # to our first row but isn't the first row. In this case
                # we have a fork, otherwise return false
                if (len(second_set_of_2)):
                    return True
            return False
        return False

    def find_optimal_move(self, player_pieces_array, player_num, other_num, fork_spots):
        '''
            In the event where blocking an opponent's chance for a fork is your best move, this function
            gives you the optimal coordiate to block their fork, based the strategy to block an opponent's
            fork here:
            https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
        '''
        if len(fork_spots) == 1:
            return [fork_spots[0], 5]
        else:
            coordinates_to_choose = []
            for spot in self.instance_player_spots[player_num]:
                player_pieces_array[spot[0]][spot[1]] = 0
                rows_at_spot = self.three_in_a_row_at_this_spot(0, player_pieces_array, spot, return_rows=True)
                fork_spots_on_row = 0
                if rows_at_spot:
                    for row in rows_at_spot:
                        for coordinate in row:
                            if not coordinate == spot and coordinate in fork_spots:
                                if fork_spots_on_row >= 1:
                                    fork_spots_on_row = 0
                                    coordinates_to_choose = []
                                    break
                                fork_spots_on_row += 1
                                coordinates_to_choose.append(coordinate)
                        try:
                            return [coordinates_to_choose[0], 6]
                        except:
                            for coordinate in row:
                                if coordinate != spot:
                                    return [coordinate, 6]
                        fork_spots_on_row = 0
                        coordinates_to_choose = []
                player_pieces_array[spot[0]][spot[1]] = player_num

    def opposite_corner(self,current_coordinate,player_pieces_array,other_player_number):
        """
            This function is what returns whether or not there was an opposite corner.
            So if we have the situation that in the top left corner there's an X and
            in the bottom right corner there's an O, and the same for the other set of
            corners.
        """
        # If the other player is in a coordiate representing the opposite corner return true, otherwise
        # return false.
        if ((current_coordinate == [0,0]) and (player_pieces_array[2][2] == other_player_number)):
            return True
        elif ((current_coordinate == [2,2]) and (player_pieces_array[0][0] == other_player_number)):
            return True
        elif ((current_coordinate == [2,0]) and (player_pieces_array[0][2] == other_player_number)):
            return True
        elif ((current_coordinate == [0,2]) and (player_pieces_array[2][0] == other_player_number)):
            return True
        else:
            return False

    def fork_for_them(self,current_coordinate,player_pieces_array,\
                      player_number, other_player_number):
        """
            So this is what we use to determine if there would be a fork for the other side
            if they had chosen this spot. So if there is we should block it if we have
            nothing better to do.
        """
        fork_opposite = False
        # This is a little confusing, but other_player_number is our number, and
        # player_number is the other player's number when the function is applied in the static_evaluation
        # function below. So we're switching the array with the other player's number and running the fork
        # function, then replacing the other player's number with our number.
        # So we start with this in the array:
        # [[1, 0, 2],
        #  [0, 0, 0],
        #  [0, 0, 1]]
        # Then we end up with this, and run the fork function on this:
        # [[1, 0, 1],
        #  [0, 0, 0],
        #  [0, 0, 1]]
        # It returns true, and is stored in fork_opposite. Then we switch the array back
        # to this:
        # [[1, 0, 2],
        #  [0, 0, 0],
        #  [0, 0, 1]]
        if (player_pieces_array[current_coordinate[0]][current_coordinate[1]] == player_number):
            player_pieces_array[current_coordinate[0]][current_coordinate[1]] = other_player_number
            fork_opposite = self.fork(current_coordinate,player_pieces_array,other_player_number)
            player_pieces_array[current_coordinate[0]][current_coordinate[1]] = player_number
        return fork_opposite

    def static_evaluation(self,current_coordinate,player_pieces_array,player_number,\
                          other_player_number):
        """
            This is the static evaluation function that puts everything together.
            We basically check what the evaluation is at this spot based on a ranking
            system of priorities I got from wikipedia:
            https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
            We return the result accordingly.
        """
        # So we exercise the above helper functions and assign the results to booleans.
        # The corresponding states will cause us to return a list with static evaluations
        # at that spots.
        # import pdb; pdb.set_trace()
        # if current_coordinate == [1, 1]:
        #     import pdb; pdb.set_trace()
        win = self.three_in_a_row_at_this_spot(player_number,player_pieces_array,\
                                               current_coordinate)
        a_block = self.block(current_coordinate,player_pieces_array,player_number,\
                             other_player_number)
        forks = self.fork(current_coordinate,player_pieces_array,player_number)
        opposite_fork = self.fork_for_them(current_coordinate,player_pieces_array,\
                                           player_number, other_player_number)
        if win:
            return [current_coordinate,9]
        elif a_block:
            return [current_coordinate,8]
        elif forks:
            return [current_coordinate,7]
        elif opposite_fork:
            return [current_coordinate,5]
        elif current_coordinate == [1,1]:
            return [current_coordinate,4]
        elif self.opposite_corner(current_coordinate,player_pieces_array,other_player_number):
            return [current_coordinate,3]
        elif current_coordinate in [[0,0],[0,2],[2,0],[2,2]]:
            return [current_coordinate,2]
        else:
            return [current_coordinate,1]

    def no_wins(self,player_pieces_array):
        """
            This is to check if nobody won. It returns false and the direction of the
            win if it's the case. We use it in minimax
        """
        horizontal = checker_utils.three_in_a_row(player_pieces_array)
        vertical = checker_utils.three_in_a_column(player_pieces_array)
        diagonal = checker_utils.diagonals(player_pieces_array)

        if ((not (horizontal is None)) and (not(horizontal == 0))):
            return [False, horizontal]
        elif ((not (vertical is None)) and (not(vertical == 0))):
            return [False,vertical]
        elif ((not (diagonal is None)) and (not (diagonal == 0))):
            return [False,diagonal]
        else:
            return [True,0]


    def minimax(self,recursion_depth,player_pieces_array,maximizing_player,player_number,\
                other_player_number,current_coordinate,available_spots_on_the_board):
        """
            This is my implementation of the minimax algorithm. Type 'minimax algorithm'
            in YouTube/Google for more information. There's some helpful info on YouTube on
            the concept behind it. I used the helper functions above to implement it.
            Basically minimax says "look ahead x number of moves", x being the layers of
            recursion of the function, and evaluate and score the various moves and
            their outcomes based on their results. So if we found a way
            to win in 3 moves with someone on the other side giving you a hard time,
            then it's worth more than if you can find a way to win in 8 or 9 moves.
            The computer tries to get the result that offers the highest
            static score, while it assignes you to try to get the lowest static score. The
            static values evaluated have equal magnitudes, as it is only the sign (+/-) that
            is flipped. Through seeing ahead through this back and forth struggle,
            it is supposed to find the best move to make. Oddly enough, it works the
            opposite way where less layers of recursion are harder to beat when the
            computer goes second. Hence I switched it so that lower layers are higher
            levels of difficulty on the version where the computer goes second.
            It works more normal when the computer goes first,
            though it's easier to beat on medium than Easy when you play according
            to the strategy programmed in our static evaluation function.
            So I switched it accordingly on the option where the computer goes first.
        """
        max_eval = - sys.maxsize
        min_eval = sys.maxsize
        max_evaluation = [0,0]
        min_evaluation = [0,0]
        win = self.no_wins(player_pieces_array)
        filled_up = checker_utils.all_filled_up(available_spots_on_the_board)
        evaluation = []
        fork_spots = []

        if (((recursion_depth == 0) or (not win[0])) or filled_up):
            # Basically has someone won, or is the array filled, or is the depth at 0
            if not win[0] and win[1] == player_number:
                evaluation = [current_coordinate, -9]
            evaluation = self.static_evaluation(current_coordinate,\
                                                player_pieces_array,\
                                                other_player_number,\
                                                player_number)
            # This line increases values of moves that win earlier, to where
            # if we can find a way to win in 3 moves instead of 5 or 6, let's do
            # that. This could be greater than 1 in the event that we have found
            # a winning move, but the recursion level is not yet at 0.
            evaluation[1] *= (recursion_depth + 1)
            if maximizing_player:
                # The same thing happens in the opposite direction
                evaluation[1] *= -1
            return evaluation

        # We check to see if the spot's empty and we put the number in, and get its evaluation
        if maximizing_player:
            for i in (range(len(player_pieces_array))):
                for j in (range(len(player_pieces_array[i]))):
                    # So the list has lists inside it, and we go across each list
                    # and see get the evaluation of the piece here if it's not full.
                    if (player_pieces_array[i][j] == 0):
                        # So have it equal to the number of the current player
                        # (who's turn it is) and run the minimax function with this coordinate filled.
                        # Eventually it finds a winning move, or recurses to the base case,
                        # returning a value. When it is found, compare it with max eval
                        # and set the new maximum evaluation value accordingly.
                        # Then set the board back to how it was befoe, and iterate through the
                        # remaining spots. Return the maximum evaluation coordinate accordingly.
                        player_pieces_array[i][j] = player_number
                        available_spots_on_the_board[i][j] = False
                        self.instance_player_spots[player_number].append([i, j])
                        evaluation = self.minimax(recursion_depth - 1,\
                                                  player_pieces_array,\
                                                  False,\
                                                  other_player_number,\
                                                  player_number,\
                                                  [i,j],\
                                                  available_spots_on_the_board)
                        if recursion_depth == 1 and abs(evaluation[1]) == 5:
                            fork_spots.append(evaluation[0])
                        if (evaluation[1] > max_eval):
                            max_evaluation = [[i,j],evaluation[1]]
                        max_eval = max(max_eval,evaluation[1])
                        player_pieces_array[i][j] = 0
                        available_spots_on_the_board[i][j] = True
                        self.instance_player_spots[player_number].pop()
            if recursion_depth == 1 and abs(max_evaluation[1]) == 5 and len(fork_spots) > 1:
                max_evaluation = self.find_optimal_move(
                    player_pieces_array, player_number, other_player_number, fork_spots
                )
            return max_evaluation

        # Else if it's not the maximizing player's turn, we see if it's empty and put in the other number
        else:
            for i in (range(len(player_pieces_array))):
                for j in (range(len(player_pieces_array[i]))):
                    # This is the same as above, but we use the minimum evaluation this time.
                    if (player_pieces_array[i][j] == 0):
                        player_pieces_array[i][j] = player_number
                        available_spots_on_the_board[i][j] = False
                        self.instance_player_spots[player_number].append([i, j])
                        evaluation = self.minimax(recursion_depth - 1,\
                                                  player_pieces_array,\
                                                  True,\
                                                  other_player_number,\
                                                  player_number,\
                                                  [i,j],\
                                                  available_spots_on_the_board)
                        if recursion_depth == 1 and abs(evaluation[1]) == 5:
                            fork_spots.append(evaluation[0])
                        if (evaluation[1] < min_eval):
                            min_evaluation = [[i,j],evaluation[1]]
                        min_eval = min(min_eval,evaluation[1])
                        player_pieces_array[i][j] = 0
                        available_spots_on_the_board[i][j] = True
                        self.instance_player_spots[player_number].pop()
            if recursion_depth == 1 and abs(min_evaluation[1]) == 5 and len(fork_spots) > 1:
                min_evaluation = self.find_optimal_move(
                    player_pieces_array, player_number, other_player_number, fork_spots
                )
                min_evaluation[1] *= -1
            return min_evaluation
