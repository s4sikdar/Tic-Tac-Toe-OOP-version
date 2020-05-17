# These are saved as .txt files most likely. Copy the text onto your python IDE
# (preferrably use Atom) and save this as "Artificial_Intelligence.py"
import Checker_fns
from Checker_fns import *
from Checker_fns import Checker
import sys

# This class is for our AI that comes up with the right moves using the minimax
# algorithm
class The_AI_program:
    # This basically checks if all 3 numbers are the same across a row of 3
    # and they equal the number in question
    def All_the_same(self,number,player_pieces,Checker_object):
        all_equal = (number == player_pieces[0])\
                     and (Checker_object.True_across(player_pieces))
        return all_equal

    # This basically if we have 3 in a row across any possible rows at that
    # coordinate
    def Three_row(self,number,pieces_on_board,coordinate,Checker_object):
        if coordinate in [[0,0],[2,2]]:
            return ((self.All_the_same(number,pieces_on_board[coordinate[0]],Checker_object)) or\
                   (self.All_the_same(number,[pieces_on_board[0][coordinate[1]],\
                                              pieces_on_board[1][coordinate[1]],\
                                              pieces_on_board[2][coordinate[1]]],\
                                              Checker_object)) or\
                   (self.All_the_same(number,[pieces_on_board[0][0],\
                                              pieces_on_board[1][1],\
                                              pieces_on_board[2][2]],\
                                              Checker_object)))
        elif coordinate in [[0,2],[2,0]]:
            return ((self.All_the_same(number,pieces_on_board[coordinate[0]],Checker_object)) or\
                    (self.All_the_same(number,[pieces_on_board[0][coordinate[1]],\
                                               pieces_on_board[1][coordinate[1]],\
                                               pieces_on_board[2][coordinate[1]]],\
                                               Checker_object)) or\
                    (self.All_the_same(number,[pieces_on_board[0][2],\
                                               pieces_on_board[1][1],\
                                               pieces_on_board[2][0]],\
                                               Checker_object)))
        elif coordinate in [[0,1],[1,0],[1,2],[2,1]]:
            return ((self.All_the_same(number,pieces_on_board[coordinate[0]],Checker_object)) or\
                    (self.All_the_same(number,[pieces_on_board[0][coordinate[1]],\
                                               pieces_on_board[1][coordinate[1]],\
                                               pieces_on_board[2][coordinate[1]]],\
                                               Checker_object)))
        else:
            return ((self.All_the_same(number,pieces_on_board[coordinate[0]],Checker_object)) or\
                    (self.All_the_same(number,[pieces_on_board[0][coordinate[1]],\
                                               pieces_on_board[1][coordinate[1]],\
                                               pieces_on_board[2][coordinate[1]]],\
                                               Checker_object)) or\
                    (self.All_the_same(number,[pieces_on_board[0][2],\
                                               pieces_on_board[1][1],\
                                               pieces_on_board[2][0]],\
                                               Checker_object)) or\
                    (self.All_the_same(number,[pieces_on_board[0][0],\
                                               pieces_on_board[1][1],\
                                               pieces_on_board[2][2]],\
                                               Checker_object)))

    ''' Checks to see if we have 2 in a row, used in our fork function
    '''
    def Two_in_a_row(self,number, player_pieces):
        Times_number = 0
        Times_0 = 0

        for i in (range(len(player_pieces))):
            if (player_pieces[i] == number):
                Times_number += 1
            elif (player_pieces[i] == 0):
                Times_0 += 1

        if ((Times_number == 2) and (Times_0 == 1)):
            return True
        else:
            return False

    ''' We check take in 2 numbers to look for, the number, the other number, and our array of 3, we check if we
    have a combination of 2 and 1 for our preferred number, 'number'.
    So if we wanted to see if we had blocked their 1 pieces, 2 would be number and 1 would be the other number.
    We will use the maximizing player boolean to switch the order we enter 1, 2 in the function (because if
    we are switching turns like in algorithm, then we switch spots here)
    '''
    def Blocked_row_of_2(self,number,other_number,player_pieces):
        Times_number = 0
        Times_opposite = 0

        for i in (range(len(player_pieces))):
            if (player_pieces[i] == number):
                Times_number += 1
            elif (player_pieces[i] == other_number):
                Times_opposite += 1

        if ((Times_number == 1) and (Times_opposite == 2)):
            return True
        else:
            return False

    ''' Our function takes in coordinate, array, 3 boolean values for the vertical, horizontal, and diagonal directions
     and checks from where the coordinate is for rows of 2. We accordingly give back a list depending on if the list is vertical,
     horizontal, and diagonal and our corresponding boolean value is true. We then give back a list of indices for the row wherever
     we found the 2 in a row. We use the booleans to "turn off a direction" and look for two in a row in other directions. For example,
     this function could find 2 in a row horizontally, and if we don't turn the horizontal direction off, it'll just return the same row
     of indices in the same direction again.
    '''
    def Our_function(self,number,coordinate,player_pieces,horizontal,vertical,diagonal):
        if coordinate in [[0,0],[2,2]]:
            if ((self.Two_in_a_row(number,player_pieces[coordinate[0]])) and horizontal):
                return [[coordinate[0],0],[coordinate[0],1],[coordinate[0],2]]
            elif ((self.Two_in_a_row(number,[player_pieces[0][coordinate[1]],player_pieces[1][coordinate[1]],player_pieces[2][coordinate[1]]])) and\
                  vertical):
                return [[0,coordinate[1]],[1,coordinate[1]],[2,coordinate[1]]]
            elif ((self.Two_in_a_row(number,[player_pieces[0][0],player_pieces[1][1],player_pieces[2][2]])) and diagonal):
                return [[0,0],[1,1],[2,2]]
            else:
                return []
        elif coordinate in [[0,2],[2,0]]:
            if ((self.Two_in_a_row(number,player_pieces[coordinate[0]])) and horizontal):
                return [[coordinate[0],0],[coordinate[0],1],[coordinate[0],2]]
            elif ((self.Two_in_a_row(number,[player_pieces[0][coordinate[1]],player_pieces[1][coordinate[1]],player_pieces[2][coordinate[1]]])) and\
                  vertical):
                return [[0,coordinate[1]],[1,coordinate[1]],[2,coordinate[1]]]
            elif ((self.Two_in_a_row(number,[player_pieces[0][2],player_pieces[1][1],player_pieces[2][0]])) and diagonal):
                return [[0,2],[1,1],[2,0]]
            else:
                return []
        elif (coordinate == [1,1]):
            if ((self.Two_in_a_row(number,player_pieces[coordinate[0]])) and horizontal):
                return [[coordinate[0],0],[coordinate[0],1],[coordinate[0],2]]
            elif ((self.Two_in_a_row(number,[player_pieces[0][coordinate[1]],player_pieces[1][coordinate[1]],player_pieces[2][coordinate[1]]])) and\
                  vertical):
                return [[0,coordinate[1]],[1,coordinate[1]],[2,coordinate[1]]]
            elif ((self.Two_in_a_row(number,[player_pieces[0][0],player_pieces[1][1],player_pieces[2][2]])) and diagonal):
                return [[0,0],[1,1],[2,2]]
            elif ((self.Two_in_a_row(number,[player_pieces[0][2],player_pieces[1][1],player_pieces[2][0]])) and diagonal):
                return [[0,2],[1,1],[2,0]]
            else:
                return []
        else:
            if ((self.Two_in_a_row(number,player_pieces[coordinate[0]])) and horizontal):
                return [[coordinate[0],0],[coordinate[0],1],[coordinate[0],2]]
            elif ((self.Two_in_a_row(number,[player_pieces[0][coordinate[1]],player_pieces[1][coordinate[1]],player_pieces[2][coordinate[1]]])) and\
                  vertical):
                return [[0,coordinate[1]],[1,coordinate[1]],[2,coordinate[1]]]
            else:
                return []

    ''' Block takes in a number, the other number (what to use for blocked row of 2), a coordinate, and the
    array of numbers to use. from our coordinate we see if we have blocked any rows of 2, depending on where
    we are starting from. We will use this to find it such that it's main number once, and the opposite number
    twice. So if you're X, you're 1. So if you have [O,O,X], then it registers as [2,2,1], where 1 is the main number
    (number) and 2 is the other number (other_number). So we use the function a few lines above that found this to then
    determine if it's a block.
    '''
    def Block(self, coordinate, player_pieces, number, other_number):
        Its_a_block = False
        if coordinate in [[0,0], [2,2]]:
            Its_a_block = self.Blocked_row_of_2(number,other_number,player_pieces[coordinate[0]]) or\
                          self.Blocked_row_of_2(number,other_number,[player_pieces[0][coordinate[1]],\
                                                                player_pieces[1][coordinate[1]],\
                                                                player_pieces[2][coordinate[1]]]) or\
                          self.Blocked_row_of_2(number,other_number,[player_pieces[0][0],player_pieces[1][1],player_pieces[2][2]])
            return Its_a_block
        elif coordinate in [[0,2],[2,0]]:
            Its_a_block = self.Blocked_row_of_2(number,other_number,player_pieces[coordinate[0]]) or\
                          self.Blocked_row_of_2(number,other_number,[player_pieces[0][coordinate[1]],\
                                                                player_pieces[1][coordinate[1]],\
                                                                player_pieces[2][coordinate[1]]]) or\
                          self.Blocked_row_of_2(number,other_number,[player_pieces[2][0],player_pieces[1][1],player_pieces[0][2]])
            return Its_a_block
        elif coordinate is [1,1]:
            Its_a_block = self.Blocked_row_of_2(number,other_number,player_pieces[coordinate[0]]) or\
                          self.Blocked_row_of_2(number,other_number,[player_pieces[0][coordinate[1]],\
                                                                player_pieces[1][coordinate[1]],\
                                                                player_pieces[2][coordinate[1]]]) or\
                          self.Blocked_row_of_2(number,other_number,[player_pieces[0][0],player_pieces[1][1],player_pieces[2][2]]) or\
                          self.Blocked_row_of_2(number,other_number,[player_pieces[2][0],player_pieces[1][1],player_pieces[0][2]])
            return Its_a_block
        else:
            Its_a_block = self.Blocked_row_of_2(number,other_number,player_pieces[coordinate[0]]) or\
                          self.Blocked_row_of_2(number,other_number,[player_pieces[0][coordinate[1]],\
                                                                player_pieces[1][coordinate[1]],\
                                                                player_pieces[2][coordinate[1]]])
            return Its_a_block

    '''A fork is where we have 2 unblocked rows of 2. By definition we could have 2 separate unblocked rows of 2, though
    this will not happen by the design of our algorithm, as if there would be 4 pieces used when the player could just win on
     the third turn if it's not blocked (if we have row 1 and 3 are filled with 2 in a row, if for argument's sake they're never
     blocked, then we could win on the 3rd or 4th turn). For this reason, all our forks will be 2 connected unblocked rows of 2.
     We have a coordinate and we check if we have 2 unblocked rows of 2 from this coordinate.
    '''
    def Fork(self,coordinate,player_pieces,number):
        #print('Before mutation:')
        #print(coordinate)
        #print('After mutation')
        #for i in (range(len(array))):
        #    print(array[i])
        #New_coordinate = []
        List_1 = self.Our_function(number,coordinate,player_pieces,True,True,True)
        #print('List_1:',List_1)
        List_2 = []
        if ((len(List_1)) != 0):
            if List_1 in [[[0,0],[1,1],[2,2]],[[0,2],[1,1],[2,0]]]:
                for i in (range(len(List_1))):
                    List_2 = self.Our_function(number,List_1[i],player_pieces,True,True,False)
                    #print('List_2:',List_2)
                    if ((len(List_2)) != 0):
                        return True
                return False
            elif ((List_1[0][0] == List_1[1][0]) and (List_1[1][0] == List_1[2][0])):
                for i in (range(len(List_1))):
                    List_2 = self.Our_function(number,List_1[i],player_pieces,False,True,True)
                    #print('List_2:',List_2)
                    if ((len(List_2)) != 0):
                        return True
                return False
            else:
                for i in (range(len(List_1))):
                    List_2 = self.Our_function(number,List_1[i],player_pieces,True,False,True)
                    #print('List_2:',List_2)
                    if ((len(List_2)) != 0):
                        return True
                return False
        else:
            return False

    ''' This function is what returns whether or not there was an opposite corner. So if we have the situation that
    in the top left corner there's an X and in the bottom right corner there's an O, and the same for the other set of
    corners.
    '''
    def Opposite_corner(self, coordinate, player_pieces, other_number):
        if ((coordinate == [0,0]) and (player_pieces[2][2] == other_number)):
            return True
        elif ((coordinate == [2,2]) and (player_pieces[0][0] == other_number)):
            return True
        elif ((coordinate == [2,0]) and (player_pieces[0][2] == other_number)):
            return True
        elif ((coordinate == [0,2]) and (player_pieces[2][0] == other_number)):
            return True
        else:
            return False

    # So this is what we use to determine if there's a fork for the other side.
    # So if there is we should block it if we have nothing better to do.
    def Fork_for_them(self,coordinate,player_pieces,number,other_number):
        Fork_Opposite = False
        if (player_pieces[coordinate[0]][coordinate[1]] == other_number):
            player_pieces[coordinate[0]][coordinate[1]] = number
            Fork_Opposite = self.Fork(coordinate,player_pieces,number)
            player_pieces[coordinate[0]][coordinate[1]] = other_number
        #for i in (range(len(array))):
        #        print(array[i])
        return Fork_Opposite

    # This is the static evaluation function that puts everything together.
    # We basically check what the evaluation is at this spot based on a ranking
    # system of priorities I got from wikipedia: https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy
    # We return the result accordingly
    def Static_Evaluation(self,coordinate,player_pieces,number,other_number,Checker_object):
        Three = self.Three_row(number,player_pieces,coordinate,Checker_object)
        #print('Three in a row:',Three, 'for',coordinate)
        A_Block = self.Block(coordinate,player_pieces,number,other_number)
        #print('Block:',A_Block,'for',coordinate)
        Forks = self.Fork(coordinate,player_pieces,number)
        #print('Fork for us:',Forks,'for',coordinate)
        Opposite = self.Fork_for_them(coordinate,player_pieces,other_number,number)
        #print('Fork for them:',Opposite,'for',coordinate)

        if Three:
            return [coordinate,8]
        elif A_Block:
            return [coordinate,7]
        elif Forks:
            return [coordinate,6]
        elif Opposite:
            return [coordinate,5]
        elif coordinate == [1,1]:
            return [coordinate,4]
        elif self.Opposite_corner(coordinate,player_pieces,other_number):
            return [coordinate,3]
        elif coordinate in [[0,0],[0,2],[2,0],[2,2]]:
            return [coordinate,2]
        else:
            return [coordinate,1]

    # This is to check if nobody won. It returns false and the direction of the
    # win if it's the case. We use it in minimax
    def No_wins(self,Game_board,Checker_object):
        Horizontal = Checker_object.Three_in_a_row(Game_board)
        Vertical = Checker_object.Three_in_a_column(Game_board)
        Diagonal = Checker_object.Diagonals(Game_board)

        if ((not (Horizontal is None)) and (not(Horizontal == 0))):
            #print_board()
            #print('Player', Horizontal, 'wins!')
            return [False, Horizontal]
        elif ((not (Vertical is None)) and (not(Horizontal == 0))):
            #print_board()
            #print('Player', Vertical, 'wins!')
            return [False,Vertical]
        elif ((not (Diagonal is None)) and (not (Diagonal == 0))):
            #print_board()
            #print('Player', Diagonal, 'wins!')
            return [False,Diagonal]
        else:
            #print('Nothing in a row. Noone wins yet.')
            return [True,0]

    # This is my implementation of the minimax algorithm. Type 'minimax algorithm'
    # in YouTube/Google for more information. There's some helpful info on YouTube on
    # the concept behind it. I basically used the helper functions above to implement it.
    # Basically minimax says "look ahead x number of moves", x being the layers of
    # recursion of the function, and evaluate and score the various moves and
    # their outcomes based on the results of these outcomes. So if we found a way
    # to win in 3 moves with someone on the other side giving you a hard time,
    # then it's worth more than if you can find a way to win in 8 or 9 moves.
    # The computer tries to get the result that offers the highest
    # static score, while it assignes you to get the lowest static score. The
    # same results have equal magnitudes though. Through seeing ahead through this
    # back and forth struggle, it is supposed to find the best move to make. Oddly
    # enough, it works the opposite way where less layers of recursion
    # are harder to beat when the computer goes second.
    # Hence I switched it so that lower layers are higher levels of difficulty
    # on the version where the computer goes second. It works more normal when
    # the computer goes first, though it's easier to beat on medium than Easy
    # when you play according to the strategy programmed in our static Evaluation
    # function. So I switched it accordingly on the option where the computer
    # goes first
    def minimax(self,depth,player_pieces,maximizing_player,number,\
                Checker_object,other_number,coordinate,available_spots):
        #print('Layer of recursion:',depth)
        max_eval = - sys.maxsize
        min_eval = sys.maxsize
        Max_evaluation = [0,0]
        Min_Evaluation = [0,0]
        #Max_coordinate = []
        #Min_coordinate = []
        Win = self.No_wins(player_pieces,Checker_object)
        Filled_up = Checker_object.All_Filled_Up(available_spots)
        Evaluation = []
        if (((depth == 0) or (not Win[0])) or Filled_up): #Basically has someone won, or is the array filled, or is
            # the depth at 0
            if (not maximizing_player):
                Evaluation = self.Static_Evaluation(coordinate,\
                                                    player_pieces,\
                                                    other_number,\
                                                    number,\
                                                    Checker_object)
                Evaluation[1] *= (depth + 1)
                #print('Static evaluation at',coordinate,'is',Evaluation[1])
                return Evaluation
            else:
                Evaluation = self.Static_Evaluation(coordinate,\
                                                    player_pieces,\
                                                    other_number,\
                                                    number,\
                                                    Checker_object)
                Evaluation[1] *= (-1 * (depth + 1))
                #print('Static evaluation at',coordinate,'is',Evaluation[1])
                return Evaluation

        # We check to see if the spot's empty and we put the number in, and get its evaluation
        if maximizing_player:
            for i in (range(len(player_pieces))):
                for j in (range(len(player_pieces[i]))):
                    if (player_pieces[i][j] == 0):
                        player_pieces[i][j] = number
                        #for x in (range(len(array))):
                        #        print(array[x])
                        #print('\n')
                        #print('Coordinates max:',[i,j])
                        available_spots[i][j] = False
                        Evaluation = self.minimax(depth - 1,\
                                                  player_pieces,\
                                                  False,\
                                                  other_number,\
                                                  Checker_object,\
                                                  number,\
                                                  [i,j],\
                                                  available_spots)
                        #print('Choice with ' + (str(depth)) + ' layer of recursion at ' + (str([i,j]))+':', Evaluation)
                        #print(Evaluation)
                        if (Evaluation[1] > max_eval):
                            Max_evaluation = [[i,j],Evaluation[1]]
                        #    print('Max Evaluation:',Max_evaluation)
                        max_eval = max(max_eval,Evaluation[1])
                        player_pieces[i][j] = 0
                        available_spots[i][j] = True
                        #for i in (range(len(array))):
                        #    print(array[i])
                            #print('\n')'''
            #print('Max choice with ' + (str(depth)) + ' layer of recursion:', Max_evaluation)
            #print('Maximizing Player')
            return Max_evaluation

        #Else if it's not the maximizing player's turn, we see if it's empty and put in the other number
        else:
            for i in (range(len(player_pieces))):
                for j in (range(len(player_pieces[i]))):
                    if (player_pieces[i][j] == 0):
                        player_pieces[i][j] = number
                        available_spots[i][j] = False
                        #for x in (range(len(array))):
                        #    print(array[x])
                        #print('\n')
                        #print('Coordinates min:',[i,j])
                        Evaluation = self.minimax(depth - 1,\
                                                  player_pieces,\
                                                  True,\
                                                  other_number,\
                                                  Checker_object,\
                                                  number,\
                                                  [i,j],\
                                                  available_spots)
                        #print('Choice with ' + (str(depth)) + ' layer of recursion at ' + (str([i,j]))+':', Evaluation)
                        #print(Evaluation)
                        if (Evaluation[1] < min_eval):
                            Min_evaluation = [[i,j],Evaluation[1]]
                        #    print('Min Evaluation:', Min_evaluation)
                        min_eval = min(min_eval,Evaluation[1])
                        player_pieces[i][j] = 0
                        available_spots[i][j] = True
                        #for i in (range(len(array))):
                        #    print(array[i])
                        #print('\n')
            #print('Min choice with ' + (str(depth)) + ' layer of recursion:', Min_evaluation)
            #print('Minimizing player')
            return Min_evaluation
