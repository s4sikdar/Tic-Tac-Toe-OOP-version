# These are saved as .txt files most likely. Copy the text onto your python IDE
# (preferrably use Atom) and save this as "File_and_menu.py"
import os
import Game_module
import Variables
from Variables import *
from Game_module import *

# This class is for our database and file systems to keep track of individual profiles
# and their scores
class File_and_database_object:
    # We initialize our variables we use to keep track of the players, their scores,
    # and who's signed in
    def __init__(self):
        self.Database = []
        self.Players_signed_in =[None,None]

    # We find the number of elements in the database with players who haven't played
    # and thus have all 0s in their profile
    def Number_of_nones(self,Numbered_list):
        i = 0
        for item in Numbered_list:
            if (item == None):
                i += 1
        return i

    def median(self,list_of_numbers):
        ordered_list = []
        list_min = 0

        while ((len(list_of_numbers)) > 0):
            list_min = list_of_numbers.pop(list_of_numbers.index(min(list_of_numbers)))
            print('New list is', list_of_numbers)
            ordered_list.append(list_min)
            print('New ordered list:', ordered_list)

        if ((len(ordered_list)) % 2) == 0:
            return (ordered_list[(len(ordered_list)) // 2] + ordered_list[((len(ordered_list)) // 2) - 1]) / 2
        else:
            return ordered_list[(len(ordered_list)) // 2]

    #median([2,3,4,3.5,4,5,7])

    # This basically ranks the database, according to the ranking system we use.
    # We do the grunt work in the database list we create each time, so we just
    # have to transcribe everything onto the text document
    def New_Rank(self,Database_list):
        a = 0
        Place_holder = []
        List_of_scores = []
        New_List = []
        Max = None
        for j in (range(len(Database_list))):
            List_of_scores.append(Database_list[j][4])
        List_of_scores_copy = List_of_scores.copy()
        while ((len(List_of_scores_copy)) > 0):
            Max = max(List_of_scores_copy)
            #print('Iteration:', (a+1), 'Max:',Max)
            #print('List of scores copy before remove:', List_of_scores_copy)
            New_List.append(Database_list[List_of_scores_copy.index(Max)])
            Database_list.pop(List_of_scores_copy.index(Max))
            #print('List:',List)
            #print('New List:', New_List)
            List_of_scores_copy.remove(Max)
            #print('List of scores copy:', List_of_scores_copy)
            a += 1
        for i in (range(len(New_List) - 1)):
            if (New_List[i][4] == New_List[i + 1][4]):
                #print('Index:',i)
                #print(('New_List[%d][0]:' % i), New_List[i][0])
                #print(('New_List[%d][0]:' % (i + 1)), New_List[i + 1][0])
                if ((New_List[i][0].casefold()) > (New_List[i + 1][0].casefold())):
                    Place_holder = New_List[i + 1]
                    #print('New List[i + 1]',Place_holder)
                    #print('New List[i]',New_List[i])
                    #print('Placeholder:',Place_holder)
                    New_List[i + 1] = New_List[i]
                    New_List[i] = Place_holder
                    #print(('New_List[%d][0]:' % i), New_List[i][0])
                    #print(('New_List[%d][0]:' % (i + 1)), New_List[i + 1][0])
        #print(New_List)
        return New_List

    # This is what we use to remove all the elements of the list that have only
    # 0s, which we can then order by themselves. This is then appended to the
    # ranked list in the Rank_Database function below
    def Remove_all_zeros(self):
        i = 0
        All_zeros = None
        List_of_zeros = []
        Element = None
        length = len(self.Database)
        while (i < length):
            All_zeros = ((0 == self.Database[i][1])\
                         and (self.Database[i][1] == self.Database[i][2])\
                         and (self.Database[i][3] == self.Database[i][2])\
                         and (self.Database[i][3] == self.Database[i][4]))
            if All_zeros:
                Element = self.Database[i]
                self.Database.pop(i)
                List_of_zeros.append(Element)
            else:
                i += 1
            length = len(self.Database)

        return List_of_zeros

    # This is what we use to rank the current database
    def Rank_Database(self):
        Players_not_played_yet = self.Remove_all_zeros()
        List_of_profiles = []
        #print('Player not played yet:',Players_not_played_yet)
        #print('Database inside Rank Database:',Database)
        self.Database = self.New_Rank(self.Database)
        #print('Database past new rank:',Database)
        Players_not_played_yet = self.New_Rank(Players_not_played_yet)
        #print('Database past players not played yet:',Database)
        for i in (range(len(Players_not_played_yet))):
            #print(('Iteration %d:' % (i+1)),Players_not_played_yet[i])
            self.Database.append(Players_not_played_yet[i])
        List_of_profiles = self.Database
        return List_of_profiles

    # Once single player comes back, we adjust the according results to the
    # according profile.
    def Result_Score_Single_Player(self,Name,difficulty,win,loss,tie,Variable_object):
        a = 0
        if (Name == None):
            return None
        for i in (range(len(self.Database))):
            if ((self.Database[i][0].casefold()) == Name.casefold()):
                a = i
                break
        if win:
            self.Database[a][1] += 1
            if (difficulty == Variable_object.Difficulty['Hard']):
                self.Database[a][4] += 6
            elif (difficulty == Variable_object.Difficulty['Medium']):
                self.Database[a][4] += 5
            else:
                self.Database[a][4] += 4
        elif loss:
            self.Database[a][2] += 1
            if (difficulty == Variable_object.Difficulty['Hard']):
                self.Database[a][4] += -4
            elif (difficulty == Variable_object.Difficulty['Medium']):
                self.Database[a][4] += -5
            else:
                self.Database[a][4] += -6
        else:
            self.Database[a][3] += 1
            if (difficulty == Variable_object.Difficulty['Hard']):
                self.Database[a][4] += 3
            elif (difficulty == Variable_object.Difficulty['Medium']):
                self.Database[a][4] += 2
            else:
                self.Database[a][4] += 1

    # This does the same thing as the Result_Score_Single_Player functions but for
    # the multiplayer version. The additions or subtractions to the individuals'
    # scores are different than Result_Score_Single_Player because the scoring system
    # adds differently. There's a function down below that prints the rules.
    def Result_Score_Multiplayer(self,Name,Second_Name,Win,Loss,Tie):
        a = 0
        j = 0
        if (Name == ''):
            return None
        for i in (range(len(self.Database))):
            if ((Name.casefold()) == (self.Database[i][0].casefold())):
                a = i
            elif ((Second_Name.casefold()) == (self.Database[i][0].casefold())):
                j = i
        if Win:
            self.Database[a][4] += 2
            self.Database[j][4] -= 2
            self.Database[a][1] += 1
            self.Database[j][2] += 1
        elif Loss:
            self.Database[a][4] -= 2
            self.Database[j][4] += 2
            self.Database[a][2] += 1
            self.Database[j][1] += 1
        else:
            self.Database[a][4] += 1
            self.Database[j][4] += 1
            self.Database[a][3] += 1
            self.Database[j][3] += 1

    # This checks to make sure that a leaderboards file exists, which if it doesn't
    # then we create the text file
    def Leaderboards_check(self):
        #print('before')
        if (not os.path.exists('Leaderboards.txt')):
            #print('file does not exist. Creating file.')
            Leaderboards = open('Leaderboards.txt','w')
            #x = Leaderboards.mode
            Leaderboards.write('                             Leaderboards                             \n')
            Leaderboards.write('Username             Wins          Losses          Ties          Score\n')
            Leaderboards.write('----------------------------------------------------------------------\n')
            Leaderboards.close()
            #Leaderboards = open('Leaderboards.txt','r')
            #Contents = Leaderboards.read()
            #print(Contents)
            #Contents = Leaderboards.readline()
            #print(Contents)
            #Leaderboards.close()
        #print('after')

    # Basically we read in strings from our text file and display our leaderboards
    def Print_Leaderboards(self):
        with open('Leaderboards.txt') as Leaderboards:
            for line in Leaderboards:
                print(line,end='')

    # This is a helper function for create string
    def Add_spaces(self,x):
        if x <= 0:
            x = 1
        empty = ''
        for i in range(x):
            empty += ' '
        #empty += 'a'
        #print(empty)
        return empty

    # This is what we use to create a new string that we add to the text file,
    # using the elements in our database, or new inputs if it's a new profile
    def Create_string(self,Name,Wins,Losses,Ties,Score):
        New_Line = Name
        New_Line += ((self.Add_spaces(21 - (len(list(New_Line))))) + (str(Wins)))
        New_Line += ((self.Add_spaces(35 - (len(list(New_Line))))) + (str(Losses)))
        New_Line += ((self.Add_spaces(51 - (len(list(New_Line))))) + (str(Ties)))
        New_Line += ((self.Add_spaces(65 - (len(list(New_Line))))) + (str(Score)) + '\n')
        return New_Line

    # Check makes sure that we have no invalid characters in our string that we
    # use to create our new profile
    def Check(self,Our_string):
        Input_string = Our_string.casefold()
        List_of_chars = list(Input_string)

        if (Input_string == ('username'.casefold())):
            return False

        if (((len(List_of_chars)) > 15) and ((len(List_of_chars)) == 0)):
            return False

        for i in (range((len(List_of_chars)) - 1)):
            if (List_of_chars[i] == ' '):
                if (List_of_chars[i + 1] == ' '):
                    return False

        for i in (range(len(List_of_chars))):
            if (not ('a' <= List_of_chars[i] <= 'z')):
                if (not ('0' <= List_of_chars[i] <= '9')):
                    if (not (List_of_chars[i] == '_')):
                        if (not (List_of_chars[i] == '-')):
                            if (not (List_of_chars[i] == ' ')):
                                return False
        del List_of_chars
        del Input_string
        return True

    # We use this to create a new username and according profile
    def New_username(self):
        Username = input('Enter a username with the following conditions:\n1) It must have alphabets.\n2) It may have\
 numbers.\n3) It may have underscores or dashes.\n4) It must be between 1 and 15 characters long.\n5) It may use one\
 space at a time before a new word/letter.\n6) It can\'t be username.\n')
        Fits_requirements = self.Check(Username)

        while (not (Fits_requirements)):
            Username = input('Invalid Input. Remember the following conditions:\n1) It must have alphabets.\n2) It may have\
 numbers.\n3) It may have underscores or dashes.\n4) It must be up to 15 characters max.\n5) It may use one space at a time\
 before a new word/letter.\n6)It can\'t be username.\n')
            Fits_requirements = self.Check(Username)

        return Username

    # Basically we add a new username to the leaderboards
    def Add_a_username(self):
        Username = self.New_username()
        #Spaces = Add_spaces(spaces)
        self.Leaderboards_check()
        #print('Leaderboards before:')
        #Print_Leaderboards()
        print('Leaderboards before username added:')
        self.Print_Leaderboards()
        New_Line = self.Create_string(Username,0,0,0,0)
        #print(Database)
        self.Database.append([Username,0,0,0,0])
        #print(Database)
        #print(New_Line)
        with open('Leaderboards.txt','a') as Leaderboards:
            Leaderboards.write(New_Line)
        print('Leaderboards after username added:')
        #with open('Leaderboards.txt','r') as Leaderboards:
        #    print(Leaderboards.readlines())
        self.Print_Leaderboards()

    # get_name, get_wins, get_losses, get_ties and get_scores are all helper functions
    # for our get_profile function. They use the right spaces to get what should be there
    # for our database
    def get_name(self,Line):
        Name = ''

        for i in (range(len(Line))):
            if (Line[i] == ' '):
                if (Line[i+1] == ' '):
                    del Line
                    return Name
            Name += Line[i]

    def get_wins(self,Line):
        Wins = ''
        for i in (range(21,(len(Line)))):
            if ('0' <= Line[i] <= '9'):
                Wins += Line[i]
            else:
                del Line
                return (int(Wins))

    def get_losses(self,Line):
        Losses = ''
        for i in (range(35,(len(Line)))):
            if ('0' <= Line[i] <= '9'):
                Losses += Line[i]
            else:
                del Line
                return (int(Losses))

    def get_ties(self,Line):
        Ties = ''
        for i in (range(51,(len(Line)))):
            if ('0' <= Line[i] <= '9'):
                Ties += Line[i]
            else:
                del Line
                return (int(Ties))

    def get_scores(self,Line):
        Scores = ''
        for i in (range(65,(len(Line)))):
            if ('0' <= Line[i] <= '9'):
                Scores += Line[i]
            else:
                del Line
                return (int(Scores))

    # This is what we use to get the profile out of a line read in from the file
    def get_profile(self,Line):
        Name = self.get_name(Line)
        Wins = self.get_wins(Line)
        Losses = self.get_losses(Line)
        Ties = self.get_ties(Line)
        Score = self.get_scores(Line)
        Profile = [Name,Wins,Losses,Ties,Score]
        return Profile

    # We adjust an entry based on a result we get
    def adjust_entry(self,Username,Result,Win,Loss,Tie):
        for i in (range(len(self.Database))):
            if ((self.Database[i][0].casefold()) == (Username.casefold())):
                if Win:
                    self.Database[i][1] += 1
                    self.Database[i][4] += Result
                elif Loss:
                    self.Database[i][2] += 1
                    self.Database[i][4] += Result
                else:
                    self.Database[i][3] += 1
                    self.Database[i][4] += Result

    '''We have our database entries which we write to our leaderboards to now print. We have ranked the database
    from earlier, so this is used in such a way that the Leaderboards will be printed exactly in the order they
    should. Seeking a character does not seem to work with the write method as much as the read method though.
    '''
    def Write_to_file(self):
        #l = 215
        with open('Leaderboards.txt','w') as Leaderboards:
            Leaderboards.write('                             Leaderboards                             \n')
            Leaderboards.write('Username             Wins          Losses          Ties          Score\n')
            Leaderboards.write('----------------------------------------------------------------------\n')
            #print('Wrote 1st 3 lines')
            for Entry in self.Database:
                Leaderboards.write(self.Create_string(Entry[0],Entry[1],Entry[2],Entry[3],Entry[4]))
                #print('Wrote:',Entry)

    ''' So we have our text file with strings. We must get these profiles for our sign in process, and
    basically everything else we do with the Leaderboards. We seek the end of the third line which is where
    we start reading in strings to create the profiles from, which we add to our database for use
    during the game.
    '''
    def Get_Profiles(self):
        self.Leaderboards_check()
        l = 216
        Line = None
        with open('Leaderboards.txt','r') as Leaderboards:
            Leaderboards.seek(l)
            Line = Leaderboards.readline()
            #print(Line)
            while ((len(Line)) > 0):
                self.Database.append(self.get_profile(Line))
                l += (len(Line))
                Line = Leaderboards.readline()
        #print('In get profiles:',Database)

    # We check to see if the name is there in thd database, as a helper function
    # for when they enter a new name
    def Name_is_there(self,Name):
        for Entry in self.Database:
            if ((Name.casefold()) == (Entry[0].casefold())):
                return Name
        return ''

    # This is our function to enter a new name
    def Enter_new_name(self):
        self.Database = self.Rank_Database()
        self.Leaderboards_check()
        self.Write_to_file()
        #Print_Leaderboards()
        New_Name = self.New_username()
        Name_in_database = self.Name_is_there(New_Name)
        while ((len(Name_in_database)) != 0):
            print('Sorry, that name\'s taken, or you entered nothing.',end='')
            New_Name = self.New_username()
            Name_in_database = self.Name_is_there(New_Name)
        self.Database.append([New_Name,0,0,0,0])
        self.Database = self.Rank_Database()
        self.Write_to_file()
        #Print_Leaderboards()

    #Enter_new_name()

    # This is our function to sign with a new username
    def Sign_in(self):
        i = 0
        Player_to_sign_in = ''
        String_input = input('Press \'s\' to sign in, press \'n\' to enter a new name.\n')
        while (not((String_input.casefold()) in ['s','n'])):
            String_input = input('Invalid input. Press \'s\' to sign in, press \'n\' to enter a new name.\n')
        if ((String_input.casefold()) == 's'):
                Mode = input('Press \'s\' for single player \'m\' for multiplayer (which mode you plan to play as).\n')
                while (not((Mode.casefold()) in ['s','m'])):
                    Mode = input('Invalid input. Press \'s\' for single player \'m\' for multiplayer (which mode you plan to play as).\n')
                if ((Mode.casefold()) == 's'):
                    if ((len(self.Database)) == 0):
                        print('No entry in the leaderboard.',end='')
                        self.Enter_new_name()
                        print('This is the name you will be signed in as.')
                        return[self.Database[0][0].casefold(),None]
                    else:
                        Nones = self.Number_of_nones(self.Players_signed_in)
                        if (Nones == 0):
                            Player_to_sign_in = input('There are 2 people signed in. Select 1 of \'{First_name}\' and\
 \'{Second_name}\' to remove:'.format(First_name = self.Players_signed_in[0],Second_name = self.Players_signed_in[1]))
                            while (not (Player_to_sign_in.casefold() in self.Players_signed_in)):
                                Player_to_sign_in = input('Invalid input. Select 1 of \'{First_name}\' and\
 \'{Second_name}\' to remove:'.format(First_name = self.Players_signed_in[0],Second_name = self.Players_signed_in[1]))
                            self.Players_signed_in[self.Players_signed_in.index(Player_to_sign_in.casefold())] = None
                            if (self.Players_signed_in[0] == None):
                                self.Players_signed_in[0] = self.Players_signed_in[1].casefold()
                                self.Players_signed_in[1] = None
                            return self.Players_signed_in
                        elif (Nones == 1):
                            #print('Placceholder statement')
                            if (self.Players_signed_in[0] == None):
                                i = 1
                            else:
                                i = 0
                            Player_to_sign_in = input('There is only \'{First_name}\' signed in. Continue(Y/N)?'.format\
                                                     (First_name = self.Players_signed_in[i]))
                            while (not((Player_to_sign_in.casefold()) in  ['y','n'])):
                                Player_to_sign_in = input('Invalid input. Press \'y\' to stay signed in as \'{First_name}\'\
 or press \'n\' otherwise.'.format(First_name = self.Players_signed_in[i]))
                            if ((Player_to_sign_in.casefold()) == 'y'):
                                return self.Players_signed_in
                            else:
                                if ((len(self.Database)) == 1):
                                    print('Only one person in the database. You can only be signed in as what you are now.')
                                    return self.Players_signed_in
                                Name = input('Enter a username.\n')
                                Is_there = self.Name_is_there(Name)
                                while (((len(Is_there)) == 0) or (self.Players_signed_in[i] == Name)):
                                    Name = input('The name you registered as is not there or\
 has already been signed in. Enter a different name.\n')
                                    Is_there = self.Name_is_there(Name)
                                return [Name.casefold(),None]
                        else:
                            Name = input('Enter a username.\n')
                            Is_there = self.Name_is_there(Name)
                            while ((len(Is_there)) == 0):
                                Name = input('The name you registered as is not there. Enter a different name.\n')
                                Is_there = self.Name_is_there(Name)
                            return [Name.casefold(),None]
                else:
                    if ((len(self.Database)) == 0):
                        print('The leaderboards are empty. You will have to enter 2 names.')
                        self.Enter_new_name()
                        self.Enter_new_name()
                        print('These 2 names will be signed in when playing.')
                        return [self.Database[0][0].casefold(),self.Database[1][0].casefold()]
                    elif ((len(self.Database)) == 1):
                        print('Not enough names in the leaderboard. You must enter another.')
                        self.Enter_new_name()
                        print('These 2 names will be signed in when playing.')
                        return [self.Database[0][0].casefold(),self.Database[1][0].casefold()]
                    else:
                        Nones = self.Number_of_nones(self.Players_signed_in)
                        if (Nones == 0):
                            print('Two people are signed in already.')
                            return self.Players_signed_in
                        elif (Nones == 1):
                            if (self.Players_signed_in[0] == None):
                                i = 1
                            else:
                                i = 0
                            Name = input('One person signed in. Sign in another:')
                            Is_there = self.Name_is_there(Name)
                            while (((len(Is_there)) == 0) or (Name == self.Players_signed_in[i])):
                                Name = input('The name you registered as is not there or signed in. Enter a different name.\n')
                                Is_there = self.Name_is_there(Name)
                            self.Players_signed_in = [self.Players_signed_in[i].casefold(),Name.casefold()]
                            return self.Players_signed_in
                        else:
                            Name = input('Enter the first username.\n')
                            Is_there = self.Name_is_there(Name)
                            while ((len(Is_there)) == 0):
                                Name = input('The name you registered as is not there. Enter a different name.\n')
                                Is_there = self.Name_is_there(Name)
                            Second_name = input('Enter the second username.\n')
                            Also_there = self.Name_is_there(Second_name)
                            while (((len(Also_there)) == 0) or (Second_name == Name)):
                                Second_name = input('The name you registered is not there or already entered. Enter a new name.\n')
                                Also_there = self.Name_is_there(Second_name)
                            return [Name.casefold(),Second_name.casefold()]
        else:
            self.Enter_new_name()
            return [None,None]

    # All profiles have 0 now
    def Clear(self):
        for Entry in self.Database:
            Entry[1] = 0
            Entry[2] = 0
            Entry[3] = 0
            Entry[4] = 0
        Database = self.Rank_Database()
        self.Write_to_file()

    # We clear all the names if we want
    def Clear_names(self):
        self.Database = []
        self.Write_to_file()

    # Clear a name() basically takes in a username and removes it from database, ranks it and writes it to file
    def Clear_a_name(self):
        if ((len(self.Database)) == 0):
            print('Nothing to clear')
            return None
        Name = input('Enter a username to remove:')
        Is_there = self.Name_is_there(Name)
        while ((len(Is_there)) == 0):
            Name = input('This username does not exist. Enter another one:')
            Is_there = self.Name_is_there(Name)
        for i in (range(len(self.Database))):
            #print(i)
            #print(Database[i][0])
            #print(Name)
            if ((self.Database[i][0].casefold()) == (Name.casefold())):
                #print('Gets in for', Database[i][0])
                self.Database.pop(i)
                self.Database = self.Rank_Database()
                self.Write_to_file()
                break

    # This is our sign out function, to sign out a signed in name
    def sign_out(self):
        String_input = ''
        Nones = self.Number_of_nones(self.Players_signed_in)
        if (Nones == 0):
            String_input = input('Two people signed in. Press \'1\' to sign out 1 or \'2\' to sign out both.')
            while (not((String_input.casefold()) in ['1','2'])):
                String_input = input('Invalid input. Select \'1\' or \'2\' to sign out 1 or 2.')
            if (String_input == '1'):
                Player_to_sign_in = input('Select 1 of \'{First_name}\' and\
     \'{Second_name}\' to remove:'.format(First_name = self.Players_signed_in[0],Second_name = self.Players_signed_in[1]))
                while (not (Player_to_sign_in.casefold() in self.Players_signed_in)):
                    Player_to_sign_in = input('Invalid input. Select 1 of \'{First_name}\' and\
     \'{Second_name}\' to remove:'.format(First_name = self.Players_signed_in[0],Second_name = self.Players_signed_in[1]))
                self.Players_signed_in[self.Players_signed_in.index(Player_to_sign_in.casefold())] = None
                if (self.Players_signed_in[0] == None):
                    i = 1
                else:
                    i = 0
                self.Players_signed_in = [self.Players_signed_in[i].casefold(),None]
                return self.Players_signed_in
            else:
                self.Players_signed_in = [None,None]
                return self.Players_signed_in
        elif (Nones == 1):
            String_input = input('One person signed in. Sign them out?(Y/N)')
            while (not((String_input.casefold()) in ['y','n'])):
                String_input = input('Invalid input. Select \'Y\' or \'N\' to sign them out or not.')
            if (String_input == 'y'):
                self.Players_signed_in = [None,None]
                return self.Players_signed_in
            else:
                return self.Players_signed_in
        else:
            print('Nobody is signed in')
            return [None,None]

class Game_object:
    # This selects the difficulty when we play in single player
    def Select_Difficulty(self,Variable_object):
        String_input = input('Enter a level of difficulty. Enter either \'Easy\', \'Medium\', or \'Hard\':')
        while (not((String_input.casefold()) in Variable_object.Difficulties)):
            String_input = input('Invalid input. Enter either \'Easy\', \'Medium\', or \'Hard\':')
        if ((String_input.casefold()) == Variable_object.Difficulties[0]):
            return Variable_object.Difficulty['Easy']
        elif ((String_input.casefold()) == Variable_object.Difficulties[1]):
            return Variable_object.Difficulty['Medium']
        else:
            return Variable_object.Difficulty['Hard']

    # This is the main game where we can choose a mode of play, and the difficulty
    # to play at, and then play at that difficulty. The end results are logged into
    # the database, the database is ranked again, and the new order is written to the
    # text file.
    def Select_Player_Option(self,Variable_object,File_and_database,Game,\
                             Multiplayer_game,AI_object,Checker_object,\
                             Input_object,Print_object):
        X = None
        Nones = File_and_database.Number_of_nones(File_and_database.Players_signed_in)
        Result = []
        String_input = input('Select \'s\' for single player, \'m\' for multiplayer:')
        while (not((String_input.casefold()) in Variable_object.Player_Options)):
            String_input = input('Invalid input. Enter either \'s\' for single player, or \'m\' for multiplayer:')
        if ((String_input.casefold()) == Variable_object.Player_Options[0]):
            if (Nones == 0):
                String_input = input('There are 2 people signed in. Select 1 of \'{First_name}\' and\
 \'{Second_name}\' to play as:'.format(First_name = File_and_database.Players_signed_in[0],Second_name = File_and_database.Players_signed_in[1]))
                while (not((String_input.casefold()) in File_and_database.Players_signed_in)):
                    String_input = input('Invalid input. Select 1 of \'{First_name}\' and\
 \'{Second_name}\' to play as:'.format(First_name = File_and_database.Players_signed_in[0],Second_name = File_and_database.Players_signed_in[1]))
                X = self.Select_Difficulty(Variable_object)
                Result = Game.Run_Single_player(String_input,X,AI_object,Checker_object,\
                                                Input_object,Print_object,Variable_object)
                File_and_database.Result_Score_Single_Player(Result[0],Result[1],\
                                                             Result[2],Result[3],\
                                                             Result[4],\
                                                             Variable_object)
                File_and_database.Database = File_and_database.Rank_Database()
                File_and_database.Write_to_file()
                Checker_object.Reset_the_board(Variable_object)
                Print_object.Clear_the_board(Variable_object)
            elif (Nones == 1):
                if (File_and_database.Players_signed_in[0] == None):
                    X = self.Select_Difficulty(Variable_object)
                    Result = Game.Run_Single_player(File_and_database.Players_signed_in[1],\
                                                    X,AI_object,Checker_object,Input_object,\
                                                    Print_object,Variable_object)
                    File_and_database.Result_Score_Single_Player(Result[0],Result[1],\
                                                                 Result[2],Result[3],\
                                                                 Result[4],\
                                                                 Variable_object)
                    File_and_database.Database = File_and_database.Rank_Database()
                    File_and_database.Write_to_file()
                    Checker_object.Reset_the_board(Variable_object)
                    Print_object.Clear_the_board(Variable_object)
                else:
                    X = self.Select_Difficulty(Variable_object)
                    Result = Game.Run_Single_player(File_and_database.Players_signed_in[0],\
                                                    X,AI_object,Checker_object,Input_object,\
                                                    Print_object,Variable_object)
                    File_and_database.Result_Score_Single_Player(Result[0],Result[1],\
                                                                 Result[2],Result[3],\
                                                                 Result[4],\
                                                                 Variable_object)
                    File_and_database.Database = File_and_database.Rank_Database()
                    File_and_database.Write_to_file()
                    Checker_object.Reset_the_board(Variable_object)
                    Print_object.Clear_the_board(Variable_object)
            else:
                print('You will be signed in as nobody.')
                X = self.Select_Difficulty(Variable_object)
                Result = Game.Run_Single_player(None,X,AI_object,\
                                                Checker_object,Input_object,\
                                                Print_object,Variable_object)
                File_and_database.Result_Score_Single_Player(Result[0],Result[1],\
                                                             Result[2],Result[3],\
                                                             Result[4],\
                                                             Variable_object)
                File_and_database.Database = File_and_database.Rank_Database()
                File_and_database.Write_to_file()
                Checker_object.Reset_the_board(Variable_object)
                Print_object.Clear_the_board(Variable_object)
        else:
            if (Nones == 1):
                if (File_and_database.Players_signed_in[0] == None):
                    i = 1
                    j = 0
                else:
                    i = 0
                    j = 1
                Name = input('One person signed in. Sign in another:')
                Is_there = File_and_database.Name_is_there(Name)
                while (((len(Is_there)) == 0) or (Name.casefold() == File_and_database.Players_signed_in[i].casefold())):
                    Name = input('The name you registered as is not there or signed in. Enter a different name.\n')
                    Is_there = File_and_database.Name_is_there(Name)
                File_and_database.Players_signed_in[j] = Name.casefold()
                print('[{First_name},{Second_name}]'.format\
                (First_name = File_and_database.Players_signed_in[0],Second_name = File_and_database.Players_signed_in[1]))
                print('These are the two names signed in. The second name signed in is the second player.')
                Result = Multiplayer_game.Run_Game(File_and_database.Players_signed_in[i],Name,\
                                                   Checker_object,Variable_object,Print_object,\
                                                   Input_object)
                File_and_database.Result_Score_Multiplayer(Result[0],Result[1],\
                                                           Result[2],Result[3],\
                                                           Result[4])
                File_and_database.Database = File_and_database.Rank_Database()
                File_and_database.Write_to_file()
                Checker_object.Reset_the_board(Variable_object)
                Print_object.Clear_the_board(Variable_object)
            elif (Nones == 0):
                print('[{First_name},{Second_name}]'.format\
                (First_name = File_and_database.Players_signed_in[0],Second_name = File_and_database.Players_signed_in[1]))
                print('The first person signed in above is player 1, and 2 for the second player')
                Result = Multiplayer_game.Run_Game(File_and_database.Players_signed_in[0],\
                                                   File_and_database.Players_signed_in[1],\
                                                   Checker_object,Variable_object,\
                                                   Print_object,Input_object)
                File_and_database.Result_Score_Multiplayer(Result[0],Result[1],\
                                                           Result[2],Result[3],\
                                                           Result[4])
                File_and_database.Database = File_and_database.Rank_Database()
                File_and_database.Write_to_file()
                Checker_object.Reset_the_board(Variable_object)
                Print_object.Clear_the_board(Variable_object)
            else:
                print('Nobody is signed in, so the game will continue without anyone signed in.')
                Result = Multiplayer_game.Run_Game('','',Checker_object,Variable_object,\
                                                   Print_object,Input_object)
                Checker_object.Reset_the_board(Variable_object)
                Print_object.Clear_the_board(Variable_object)

class Main_Menu_class:
    # this function prints the rules of how we organize our leaderboards, when the player requests it.
    def Print_Rules(self):
        print('We have 3 levels of difficulty: Easy, Medium, Hard. Winning on these levels gives +4,5,6 respectively. Losing on\n\
Easy, Medium, Hard gives -6,-5,-4 respectively. Tying on Easy, Medium, Hard gives +1,2,3 respectively. This is\n\
added to your existing score to give you your score. Players who haven\'t played are given a score of 0, and are\n\
placed below the standings of anyone who has played. When scores are tied, they are listed from top down in alphabetical\n\
order. When you play multiplayer and win, it\'s +2, when you lose it\'s -2, and when you tie yo get +1.\n')

    # This is our leaderboards function which what the leaderboards option leads to in the
    # main menu. You can clear names, clear a name, read the rules,set all profiles back to 0,
    # print the leaderboards, or go back to the main menu.
    def Leaderboards(self,File_and_database,Variable_object,Game,Multiplayer_game,\
                     Full_game,AI_object,Checker_object,Input_object,Print_object):
        String_input = input('Press \'r\' for rules, \'c\' to clear the scores (everyone starts at 0 again), \'clear\' to clear\n\
all names, \'clear name\' to clear a name, \'b\' to go back to main menu, and \'p\' to print the leaderboards.\n')
        while (not((String_input.casefold()) in ['r','c','clear','b','clear name','p'])):
            String_input = input('Invalid input Press \'r\' for rules, \'c\' to clear the scores (everyone starts at 0 again),\n\'clear\'\
to clear all names, \'clear name\' to clear a name, \'b\' to go back to main menu, amd \'p\' to print the leaderboards.\n')
        if ((String_input.casefold()) == 'r'):
            self.Print_Rules()
            self.Leaderboards(File_and_database,Variable_object,Game,Multiplayer_game,\
                              Full_game,AI_object,Checker_object,Input_object,Print_object)
        elif ((String_input.casefold()) == 'c'):
            File_and_database.Clear()
            self.Leaderboards(File_and_database,Variable_object,Game,Multiplayer_game,\
                              Full_game,AI_object,Checker_object,Input_object,Print_object)
        elif ((String_input.casefold()) == 'clear'):
            File_and_database.Clear_names()
            self.Leaderboards(File_and_database,Variable_object,Game,Multiplayer_game,\
                              Full_game,AI_object,Checker_object,Input_object,Print_object)
        elif ((String_input.casefold()) == 'b'):
            self.Main_Menu(File_and_database,Variable_object,Game,Multiplayer_game,\
                           Full_game,AI_object,Checker_object,Input_object,Print_object)
        elif ((String_input.casefold()) == 'p'):
            File_and_database.Print_Leaderboards()
            self.Leaderboards(File_and_database,Variable_object,Game,Multiplayer_game,\
                              Full_game,AI_object,Checker_object,Input_object,Print_object)
        else:
            File_and_database.Clear_a_name()
            self.Leaderboards(File_and_database,Variable_object,Game,Multiplayer_game,\
                              Full_game,AI_object,Checker_object,Input_object,Print_object)

    # This is our start menu to start from. You can quit, sign in, play the game, sign out,
    # or go to the leaderboards option explained above.
    def Main_Menu(self,File_and_database,Variable_object,Game,Multiplayer_game,\
                  Full_game,AI_object,Checker_object,Input_object,Print_object):
        if ((len(File_and_database.Database)) == 0):
            File_and_database.Get_Profiles()
        File_and_database.Database = File_and_database.Rank_Database()
        File_and_database.Write_to_file()
        File_and_database.Print_Leaderboards()
        #print(Database)
        #print(Players_signed_in)
        #Database = Rank_Database()
        #Write_to_file()
        String_input = input('Welcome to Tic Tac Toe. Press \'l\' for leaderboards, \'q\' to quit, \'s\' to sign in or enter a new\
 username,\n\'g\' to play the game and \'o\' to sign out.\n')
        while (not ((String_input.casefold()) in ['l','q','s','g','o'])):
            String_input = input('Invalid input. Press \'l\' for leaderboards, \'q\' to quit,\'s\' to sign in or enter a new username,\
    \n\'g\' to play the game and \'o\' to sign out.\n')
        if ((String_input.casefold()) == 'l'):
            self.Leaderboards(File_and_database,Variable_object,Game,Multiplayer_game,\
                              Full_game,AI_object,Checker_object,Input_object,Print_object)
        elif ((String_input.casefold()) == 's'):
            File_and_database.Players_signed_in = File_and_database.Sign_in()
            #print(Players_signed_in)
            self.Main_Menu(File_and_database,Variable_object,Game,Multiplayer_game,\
                           Full_game,AI_object,Checker_object,Input_object,Print_object)
        elif ((String_input.casefold()) == 'o'):
            File_and_database.Players_signed_in = File_and_database.sign_out()
            self.Main_Menu(File_and_database,Variable_object,Game,Multiplayer_game,\
                           Full_game,AI_object,Checker_object,Input_object,Print_object)
        elif ((String_input.casefold()) == 'g'):
            Full_game.Select_Player_Option(Variable_object,File_and_database,Game,\
                                      Multiplayer_game,AI_object,Checker_object,\
                                      Input_object,Print_object)
            self.Main_Menu(File_and_database,Variable_object,Game,Multiplayer_game,\
                           Full_game,AI_object,Checker_object,Input_object,Print_object)
        else:
            File_and_database.Database = File_and_database.Rank_Database()
            #print(Database)
            File_and_database.Write_to_file()
            File_and_database.Clear()
            #print(Database)
            return None

File_obj = File_and_database_object()
Variable = Output_array()
Game = Run_games()
Multi = Multiplayer()
AI = The_AI_program()
Checkers = Checker()
Inputs = Input_fns()
Print_obj = Print_Functions()
Main = Main_Menu_class()
Main_game = Game_object()
Main.Main_Menu(File_obj,Variable,Game,Multi,Main_game,AI,Checkers,Inputs,Print_obj)
