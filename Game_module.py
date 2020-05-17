# These are saved as .txt files most likely. Copy the text onto your python IDE
# (preferrably use Atom) and save this as "Game_module.py"
import Artificial_Intelligence
from Print_fns import Input_fns

# This class is for the single-player version of Tic Tac Toe
class Run_games:
    #This is when the person goes first when playing against the computer
    def person_goes_first(self,Name,difficulty,Artificial_Intelligence_object,\
                          Checker_object,Input_object,Print_object,\
                          Variable_object):
        Variable_object.player_1 = Input_object.Who_starts(False)
        Nobody_has_won = Artificial_Intelligence_object.No_wins(Variable_object.Array_of_player_pieces,\
                                                                Checker_object)
        Nobody_Wins = None
        Coordinates = None
        while Nobody_has_won[0]:
            Print_object.print_board(Variable_object)
            Coordinates = Input_object.Nothing_There(Variable_object.player_1,Variable_object,False)
            Print_object.Mutate_Board(Variable_object,Coordinates)
            Nobody_has_won = Artificial_Intelligence_object.No_wins(Variable_object.Array_of_player_pieces,\
                                                                    Checker_object)
            All_filled = Checker_object.All_Filled_Up(Variable_object.Array_of_available_spots)
            Nobody_Wins = ((Nobody_has_won[0]) and All_filled)
            if (not (Nobody_has_won[0])):
                Print_object.print_board(Variable_object)
                if (Variable_object.player_1):
                    print('X wins')
                else:
                    print('O wins')
                return [Name,difficulty,True,False,False]
                break
            if (Nobody_Wins):
                Print_object.print_board(Variable_object)
                print('Nobody wins.')
                return [Name,difficulty,False,False,True]
                break
            #X = input('Do you wish to exit?')
            #if (X == 'Y'):
            #    print('Out before the AI')
            #    break
            #elif (X == 'N'):
            #    print('Moving to the AI')
            #print_board()
            #for i in (range(len(Array_of_player_pieces))):
            #    print(Array_of_player_pieces[i])
            if (Variable_object.player_1):
                Coordinates = Artificial_Intelligence_object.minimax(difficulty,\
                                      Variable_object.Array_of_player_pieces,\
                                      True,2,Checker_object,1,[0,0],\
                                      Variable_object.Array_of_available_spots)
            else:
                Coordinates = Artificial_Intelligence_object.minimax(difficulty,\
                                      Variable_object.Array_of_player_pieces,\
                                      True,1,Checker_object,2,[0,0],\
                                      Variable_object.Array_of_available_spots)
            #print(Coordinates)
            #print(Coordinates)
            Variable_object.player_1 = not(Variable_object.player_1)
            Print_object.Mutate_Board(Variable_object,\
                                      [Variable_object.Number_legend.get(int(Coordinates[0][0])),\
                                      (Coordinates[0][1] + 1)])
            Nobody_has_won = Artificial_Intelligence_object.No_wins(Variable_object.Array_of_player_pieces,\
                                                                    Checker_object)
            All_filled = Checker_object.All_Filled_Up(Variable_object.Array_of_available_spots)
            Nobody_Wins = ((Nobody_has_won[0]) and All_filled)
            if (not (Nobody_has_won[0])):
                Print_object.print_board(Variable_object)
                if (Variable_object.player_1):
                    print('X wins')
                else:
                    print('O wins')
                return [Name,difficulty,False,True,False]
                break
            if (Nobody_Wins):
                Print_object.print_board(Variable_object)
                print('Nobody wins.')
                return [Name,difficulty,False,False,True]
                break
            Variable_object.player_1 = not(Variable_object.player_1)


    # I added functionality for when the computer goes first. The minimax function
    # result works differently when the person goes first vs when the computer
    # goes second. When it goes first, it works moreso as to how it should with the
    # layers of recursion, except it seems easier to beat on medium than easy mode,
    # so I gave the "medium" layer of recursion when in easy mode.
    def computer_goes_first(self,Name,difficulty,Artificial_Intelligence_object,\
                            Checker_object,Input_object,Print_object,\
                            Variable_object):
        Variable_object.player_1 = Input_object.Who_starts(False)
        Nobody_has_won = Artificial_Intelligence_object.No_wins(Variable_object.Array_of_player_pieces,\
                                                                Checker_object)
        Nobody_Wins = None
        Coordinates = None
        while Nobody_has_won[0]:

            if (Variable_object.player_1):
                Coordinates = Artificial_Intelligence_object.minimax(difficulty,\
                                      Variable_object.Array_of_player_pieces,\
                                      True,2,Checker_object,1,[0,0],\
                                      Variable_object.Array_of_available_spots)
            else:
                Coordinates = Artificial_Intelligence_object.minimax(difficulty,\
                                      Variable_object.Array_of_player_pieces,\
                                      True,1,Checker_object,2,[0,0],\
                                      Variable_object.Array_of_available_spots)

            Variable_object.player_1 = not(Variable_object.player_1)
            Print_object.Mutate_Board(Variable_object,\
                                      [Variable_object.Number_legend.get(int(Coordinates[0][0])),\
                                      (Coordinates[0][1] + 1)])
            Nobody_has_won = Artificial_Intelligence_object.No_wins(Variable_object.Array_of_player_pieces,\
                                                                    Checker_object)
            All_filled = Checker_object.All_Filled_Up(Variable_object.Array_of_available_spots)
            Nobody_Wins = ((Nobody_has_won[0]) and All_filled)
            if (not (Nobody_has_won[0])):
                Print_object.print_board(Variable_object)
                if (Variable_object.player_1):
                    print('X wins')
                else:
                    print('O wins')
                if (difficulty == Variable_object.Difficulty['Easy']):
                    return [Name,Variable_object.Difficulty['Hard'],False,True,False]
                elif (difficulty == Variable_object.Difficulty['Medium']):
                    return [Name,Variable_object.Difficulty['Easy'],False,True,False]
                else:
                    return [Name,Variable_object.Difficulty['Medium'],False,True,False]
                break
            if (Nobody_Wins):
                Print_object.print_board(Variable_object)
                print('Nobody wins.')
                if (difficulty == Variable_object.Difficulty['Easy']):
                    return [Name,Variable_object.Difficulty['Hard'],False,False,True]
                elif (difficulty == Variable_object.Difficulty['Medium']):
                    return [Name,Variable_object.Difficulty['Easy'],False,False,True]
                else:
                    return [Name,Variable_object.Difficulty['Medium'],False,False,True]
                break
            Variable_object.player_1 = not(Variable_object.player_1)

            Print_object.print_board(Variable_object)
            Coordinates = Input_object.Nothing_There(Variable_object.player_1,Variable_object,False)
            Print_object.Mutate_Board(Variable_object,Coordinates)
            Nobody_has_won = Artificial_Intelligence_object.No_wins(Variable_object.Array_of_player_pieces,\
                                                                    Checker_object)
            All_filled = Checker_object.All_Filled_Up(Variable_object.Array_of_available_spots)
            Nobody_Wins = ((Nobody_has_won[0]) and All_filled)
            if (not (Nobody_has_won[0])):
                Print_object.print_board(Variable_object)
                if (Variable_object.player_1):
                    print('X wins')
                else:
                    print('O wins')
                if (difficulty == Variable_object.Difficulty['Easy']):
                    return [Name,Variable_object.Difficulty['Hard'],True,False,False]
                elif (difficulty == Variable_object.Difficulty['Medium']):
                    return [Name,Variable_object.Difficulty['Easy'],True,False,False]
                else:
                    return [Name,Variable_object.Difficulty['Medium'],True,False,False]
                break
            if (Nobody_Wins):
                Print_object.print_board(Variable_object)
                print('Nobody wins.')
                if (difficulty == Variable_object.Difficulty['Easy']):
                    return [Name,Variable_object.Difficulty['Hard'],False,False,True]
                elif (difficulty == Variable_object.Difficulty['Medium']):
                    return [Name,Variable_object.Difficulty['Easy'],False,False,True]
                else:
                    return [Name,Variable_object.Difficulty['Medium'],True,False,False]
                break


    # This is the full single player version against the computer
    def Run_Single_player(self,Name,difficulty,Artificial_Intelligence_object,\
                          Checker_object,Input_object,Print_object,\
                          Variable_object):
        X = None
        Y = None

        In_put = input("Enter '1' to go first, enter '2' for the computer to go first: ")
        while (not((In_put.casefold()) in ['1','2'])):
            In_put = input("Invalid input. Enter '1' to go first, enter '2' for the computer to go first: ")

        if ((In_put.casefold()) == '1'):
            X = self.person_goes_first(Name,difficulty,Artificial_Intelligence_object,\
                                       Checker_object,Input_object,Print_object,\
                                       Variable_object)
            return X
        else:
            if (difficulty == Variable_object.Difficulty['Hard']):
                X = self.computer_goes_first(Name,Variable_object.Difficulty['Easy'],\
                                             Artificial_Intelligence_object,\
                                             Checker_object,Input_object,Print_object,\
                                             Variable_object)
                return X
            elif (difficulty == Variable_object.Difficulty['Easy']):
                X = self.computer_goes_first(Name,Variable_object.Difficulty['Medium'],\
                                             Artificial_Intelligence_object,\
                                             Checker_object,Input_object,Print_object,\
                                             Variable_object)
                return X
            else:
                X = self.computer_goes_first(Name,4,\
                                             Artificial_Intelligence_object,\
                                             Checker_object,Input_object,Print_object,\
                                             Variable_object)
                return X

# This is the multiplayer version of Tic Tac Toe.
class Multiplayer:
    #Our Multiplayer game function
    def Run_Game(self,Name,Second_Name,Checker_object,Variable_object,\
                 Print_object,Input_object):
        Variable_object.player_1 = Input_object.Who_starts(True)
        Nobody_has_won = True
        Nobody_Wins = None
        Coordinates = None
        All_filled = False
        while (Nobody_has_won):
            Print_object.print_board(Variable_object)
            Coordinates = Input_object.Nothing_There(Variable_object.player_1,Variable_object,\
                                                     True)
            #for i in (range(len(Array_of_available_spots))): #Test  code
            #    print(Array_of_player_pieces[i])
            Print_object.Mutate_Board(Variable_object,Coordinates)
            #for i in (range(len(Array_of_available_spots))):#Test  code
            #    print(Array_of_player_pieces[i])
            Nobody_has_won = Checker_object.No_one_wins(Variable_object.Array_of_player_pieces,\
                                                        Print_object,\
                                                        Variable_object)
            if (not(Nobody_has_won)):
                if Variable_object.player_1:
                    #print([Name,Second_Name,True,False,False]) #Test code
                    return [Name,Second_Name,True,False,False]
                else:
                    #print([Name,Second_Name,False,True,False]) #Test code
                    return [Name,Second_Name,False,True,False]
            All_filled = Checker_object.All_Filled_Up(Variable_object.Array_of_available_spots)
            Nobody_Wins = (Nobody_has_won and All_filled)
            if (Nobody_Wins):
                Print_object.print_board(Variable_object)
                print('Nobody wins.')
                return [Name,Second_Name,False,False,True]
                break
            Variable_object.player_1 = not(Variable_object.player_1)
        #print('Done!') #Test  code

    # This was a version of the game where we could repeatedly run the Multiplayer
    # option as much as we wanted, until we opted not to continue
    def Tic_Tac_Toe_Interactive_Version(self,Name,Second_Name,Checker_object,\
                                        Variable_object,Print_object,Input_object):
        Results = None
        Continue = True
        while Continue:
            Results = self.Run_Game(Name,Second_Name,Checker_object,\
                                    Variable_object,Print_object,Input_object)
            Continue = Input_object.keep_playing()
            if Continue:
                Checker_object.Reset_the_board(Variable_object)
                Print_object.Clear_the_board(Variable_object)
        #print('Done!')

'''
AI = The_AI_program()
Check = Checker()
Inputs = Input_fns()
Print_obj = Print_Functions()
Variables_object = Output_array()
The_game = Run_games()
The_game.Run_Single_player('Sailer',3,AI,Check,Inputs,Print_obj,Variables_object)
'''

'''
Multi = Multiplayer()
Name1 = 'Wallis'
Name2 = 'Sailer'
Checkers = Checker()
Vars = Output_array()
Printer = Print_Functions()
Inputs = Input_fns()
#Multi.Run_Game(Name1,Name2,Checkers,Vars,Printer,Inputs)
Multi.Tic_Tac_Toe_Interactive_Version(Name1,Name2,Checkers,Vars,Printer,Inputs)
'''
# All test code. Nothing to see here.
