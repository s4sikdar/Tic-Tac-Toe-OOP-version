import os

class FileAndDatabaseObject:
    """
        This class is for our database and file systems that keep track of individual
        profiles and their scores.
    """

    def __init__(self):
        """
            We initialize our variables we use to keep track of the players, their scores,
            and who's signed in.
        """
        self.instance_database = []
        self.instance_players_signed_in =[None,None]

    def number_of_nones(self,numbered_list):
        """
            This function finds how many None values are in the instance_players_signed_in list.
        """
        i = 0
        for item in numbered_list:
            if (item == None):
                i += 1
        return i

    def new_rank(self,database_list):
        """
            This basically ranks the database, according to the ranking system we use.
            We do the grunt work in the database list we create each time, so we just
            have to transcribe everything onto the text document.
        """
        a = 0
        place_holder = []
        list_of_scores = []
        newly_ranked_list = []
        max_score = None
        # Append the scores of the database_list to a new list of scores and copy it
        # into another list.
        for j in (range(len(database_list))):
            list_of_scores.append(database_list[j][4])
        list_of_scores_copy = list_of_scores.copy()
        # Sort out the copy of the list into a new list so as to order by score.
        while ((len(list_of_scores_copy)) > 0):
            max_score = max(list_of_scores_copy)
            newly_ranked_list.append(database_list[list_of_scores_copy.index(max_score)])
            database_list.pop(list_of_scores_copy.index(max_score))
            list_of_scores_copy.remove(max_score)
            a += 1
        # Sort out the aspects of the list where the scores are equal, in which case
        # we are going by alphabetical order of their name.
        for i in (range(len(newly_ranked_list) - 1)):
            if (newly_ranked_list[i][4] == newly_ranked_list[i + 1][4]):
                if ((newly_ranked_list[i][0].casefold()) > (newly_ranked_list[i + 1][0].casefold())):
                    place_holder = newly_ranked_list[i + 1]
                    newly_ranked_list[i + 1] = newly_ranked_list[i]
                    newly_ranked_list[i] = place_holder
        return newly_ranked_list

    def remove_all_zeros(self):
        """
            This is what we use to remove all the elements of the list that have only
            0s, which we can then order by themselves. This is then appended to the
            ranked list in the rank_database function below.
        """
        current_player_number = 0
        all_zeros = None
        list_of_zeros = []
        element = None
        length = len(self.instance_database)
        # Loop to pop all entries that have zeros outside the name into a second
        # database
        while (current_player_number < length):
            all_zeros = ((0 == self.instance_database[current_player_number][1])\
                         and (self.instance_database[current_player_number][1] ==\
                              self.instance_database[current_player_number][2])\
                         and (self.instance_database[current_player_number][3] ==\
                              self.instance_database[current_player_number][2])\
                         and (self.instance_database[current_player_number][3] ==\
                              self.instance_database[current_player_number][4]))
            if all_zeros:
                element = self.instance_database[current_player_number]
                self.instance_database.pop(current_player_number)
                list_of_zeros.append(element)
            else:
                current_player_number += 1
            length = len(self.instance_database)

        return list_of_zeros

    # This is what we use to rank the current database
    def rank_database(self):
        """
            This function ranks the current database.
        """
        # Remove the database of players who haven't played yet, rank the
        # separate databases and then add them back together.
        players_not_played_yet = self.remove_all_zeros()
        list_of_profiles = []
        self.instance_database = self.new_rank(self.instance_database)
        players_not_played_yet = self.new_rank(players_not_played_yet)
        for i in (range(len(players_not_played_yet))):
            self.instance_database.append(players_not_played_yet[i])
        list_of_profiles = self.instance_database
        return list_of_profiles

    def result_score_single_player(self,name,difficulty,win,loss,tie,game_variable_object):
        """
            Once single player comes back, we adjust the according results to the
            according profile when the single player version of the game is run.
        """
        the_single_player = 0
        if (name == None):
            return None
        # If no name was registered, exit above. Otherwise, find the index with the
        # according name and use it to update their profile in the database according
        # to the result.
        for i in (range(len(self.instance_database))):
            if ((self.instance_database[i][0].casefold()) == name.casefold()):
                the_single_player = i
                break
        if win:
            self.instance_database[the_single_player][1] += 1
            if (difficulty == game_variable_object.instance_translate_difficulty_to_recursion_levels['Hard']):
                self.instance_database[the_single_player][4] += 6
            elif (difficulty == game_variable_object.instance_translate_difficulty_to_recursion_levels['Medium']):
                self.instance_database[the_single_player][4] += 5
            else:
                self.instance_database[the_single_player][4] += 4
        elif loss:
            self.instance_database[the_single_player][2] += 1
            if (difficulty == game_variable_object.instance_translate_difficulty_to_recursion_levels['Hard']):
                self.instance_database[the_single_player][4] += -4
            elif (difficulty == game_variable_object.instance_translate_difficulty_to_recursion_levels['Medium']):
                self.instance_database[the_single_player][4] += -5
            else:
                self.instance_database[the_single_player][4] += -6
        else:
            self.instance_database[the_single_player][3] += 1
            if (difficulty == game_variable_object.instance_translate_difficulty_to_recursion_levels['Hard']):
                self.instance_database[the_single_player][4] += 3
            elif (difficulty == game_variable_object.instance_translate_difficulty_to_recursion_levels['Medium']):
                self.instance_database[the_single_player][4] += 2
            else:
                self.instance_database[the_single_player][4] += 1

    # The additions or subtractions to the individuals' scores are different
    # than result_score_single_player because the scoring system
    # adds differently. There's a function down below that prints the rules.
    def result_score_multiplayer(self,name,second_name,win,loss,tie):
        """
            This function takes care of adjusting the according results to the according
            players when the multiplayer version is run.
        """
        first_player = 0
        second_player = 0
        if (name == ''):
            return None
        # If nobody was registered, then we're done above. Otherwise, find the
        # indices according to who was playing and then update their profiles
        # according to the results.
        for i in (range(len(self.instance_database))):
            if ((name.casefold()) == (self.instance_database[i][0].casefold())):
                first_player = i
            elif ((second_name.casefold()) == (self.instance_database[i][0].casefold())):
                second_player = i
        if win:
            self.instance_database[first_player][4] += 2
            self.instance_database[second_player][4] -= 2
            self.instance_database[first_player][1] += 1
            self.instance_database[second_player][2] += 1
        elif loss:
            self.instance_database[first_player][4] -= 2
            self.instance_database[second_player][4] += 2
            self.instance_database[first_player][2] += 1
            self.instance_database[second_player][1] += 1
        else:
            self.instance_database[first_player][4] += 1
            self.instance_database[second_player][4] += 1
            self.instance_database[first_player][3] += 1
            self.instance_database[second_player][3] += 1

    def leaderboards_check(self):
        """
            This function checks to make sure that a leaderboards file exists,
            which if it doesn't then we create the according text file.
        """
        if (not os.path.exists('Leaderboards.txt')):
            leaderboards = open('Leaderboards.txt','w')
            leaderboards.write('                             Leaderboards                             \n')
            leaderboards.write('Username             Wins          Losses          Ties          Score\n')
            leaderboards.write('----------------------------------------------------------------------\n')
            leaderboards.close()

    def print_leaderboards(self):
        """
            This function reads in strings from our text file and displays our Leaderboards.
        """
        with open('Leaderboards.txt') as leaderboards:
            for line in leaderboards:
                print(line,end='')

    def add_spaces(self,number_of_spaces):
        """
            This is a helper function to add spaces for our create_string function.
        """
        # If for whatever reason a negative number is thrown in, add set the spaces
        # to 1 by default
        if number_of_spaces <= 0:
            number_of_spaces = 1
        empty = ''
        for i in range(number_of_spaces):
            empty += ' '
        # Run a for loop to add spaces to a string and then return it
        return empty

    def create_string(self,name,wins,losses,ties,score):
        """
            This function creates a new string that is added to the text file using
            elements in our database, or new inputs if we're adding a new profile.
        """
        # We create the string with the correct spaces and input values, so that
        # the lines have the same formatting when printed.
        new_line = name
        new_line += ((self.add_spaces(21 - (len(list(new_line))))) + (str(wins)))
        new_line += ((self.add_spaces(35 - (len(list(new_line))))) + (str(losses)))
        new_line += ((self.add_spaces(51 - (len(list(new_line))))) + (str(ties)))
        new_line += ((self.add_spaces(65 - (len(list(new_line))))) + (str(score)) + '\n')
        return new_line

    def check(self,our_string):
        """
            This function checks to make sure that we have no invalid characters in our
            string that is used to create our new profile.
        """
        input_string = our_string.casefold()
        list_of_chars = list(input_string)

        # They can't enter username.
        if (input_string == ('username'.casefold())):
            return False

        # We can't end with a space.
        if (list_of_chars[((len(list_of_chars)) - 1)] == ' '):
            return False

        # If we have input strings that don't fit length constraints, return false
        if (((len(list_of_chars)) > 15) and ((len(list_of_chars)) == 0)):
            return False

        # If we have a double space in the name, return false.
        for i in (range((len(list_of_chars)) - 1)):
            if (list_of_chars[i] == ' '):
                if (list_of_chars[i + 1] == ' '):
                    return False

        # Each character has to be one of the characters in the conditionals.
        # Otherwise the input string is invalid
        for i in (range(len(list_of_chars))):
            if (not ('a' <= list_of_chars[i] <= 'z')):
                if (not ('0' <= list_of_chars[i] <= '9')):
                    if (not (list_of_chars[i] == '_')):
                        if (not (list_of_chars[i] == '-')):
                            if (not (list_of_chars[i] == ' ')):
                                return False

        # We passed the other tests. Return true.
        del list_of_chars
        del input_string
        return True

    def new_username(self):
        """
            This function creates a new username and according profile.
        """
        username = input('Enter a username with the following conditions:\n1) It must have alphabets.\n2) It may have\
 numbers.\n3) It may have underscores or dashes.\n4) It must be between 1 and 15 characters long.\n5) It may use one\
 space at a time before a new word/letter.\n6) It can\'t be username.\n')
        fits_requirements = self.check(username)

        while (not (fits_requirements)):
            username = input('Invalid Input. Remember the following conditions:\n1) It must have alphabets.\n2) It may have\
 numbers.\n3) It may have underscores or dashes.\n4) It must be up to 15 characters max.\n5) It may use one space at a time\
 before a new word/letter.\n6)It can\'t be username.\n')
            fits_requirements = self.check(username)

        return username

    def add_a_username(self):
        """
            This function adds a new username to the Leaderboards.
        """
        username = self.new_username()
        self.leaderboards_check()
        print('Leaderboards before username added:')
        self.print_leaderboards()
        new_line = self.create_string(username,0,0,0,0)
        self.instance_database.append([username,0,0,0,0])
        with open('Leaderboards.txt','a') as leaderboards:
            leaderboards.write(new_line)
        print('Leaderboards after username added:')
        self.print_leaderboards()

    def get_name(self,line):
        """
            This function gets the names as a helper function to our get_profile function,
            out of a string from our text file representing a profile.
        """
        name = ''

        for i in (range(len(line))):
            # We add the string characters to the name variable, until we
            # reach multiple spaces, at which point the name ended.
            if (line[i] == ' '):
                if (line[i+1] == ' '):
                    del line
                    return name
            name += line[i]

    def get_wins(self,line):
        """
            This function gets the number of wins out of a string from our text file
            representing a profile as a helper to our get_profile function.
        """
        wins = ''
        for i in (range(21,(len(line)))):
            # Go to the right index spot in the line, and get the integers
            # till you have no numbers left. Then return the string converted into
            # an integer.
            if ('0' <= line[i] <= '9'):
                wins += line[i]
            else:
                del line
                return (int(wins))

    def get_losses(self,line):
        """
            This function gets the number of losses out of a string from our text file
            representing a profile as a helper to our get_profile function.
        """
        losses = ''
        for i in (range(35,(len(line)))):
            # The same thing as get_wins, but at the spot where the losses are stored
            if ('0' <= line[i] <= '9'):
                losses += line[i]
            else:
                del line
                return (int(losses))

    def get_ties(self,line):
        """
            This function gets the number of ties out of a string from our text file
            representing a profile as a helper to our get_profile function.
        """
        ties = ''
        for i in (range(51,(len(line)))):
            # same thing as get_losses but where the ties are stored
            if ('0' <= line[i] <= '9'):
                ties += line[i]
            else:
                del line
                return (int(ties))

    def get_scores(self,line):
        """
            This function gets the total score out of a string from our text file
            representing a profile as a helper to our get_profile function.
        """
        scores = ''
        for i in (range(65,(len(line)))):
            # same thing as get ties, but where the score is stored
            if ('0' <= line[i] <= '9'):
                scores += line[i]
            else:
                del line
                return (int(scores))

    def get_profile(self,line):
        """
            This function gets a profile out of a line read from the file, and returns
            it in a list.
        """
        # Get the name, wins, losses, ties, and score using the above functions
        # and then put it into a profile that will be put into our database.
        name = self.get_name(line)
        wins = self.get_wins(line)
        losses = self.get_losses(line)
        ties = self.get_ties(line)
        score = self.get_scores(line)
        profile = [name,wins,losses,ties,score]
        return profile

    def adjust_entry(self,username,result,win,loss,tie):
        """
            This function adjusts an entry based on the result we get.
        """
        for i in (range(len(self.instance_database))):
            if ((self.instance_database[i][0].casefold()) == (username.casefold())):
                if win:
                    self.instance_database[i][1] += 1
                    self.instance_database[i][4] += result
                elif loss:
                    self.instance_database[i][2] += 1
                    self.instance_database[i][4] += result
                else:
                    self.instance_database[i][3] += 1
                    self.instance_database[i][4] += result


    def write_to_file(self):
        """
            This function writes the contents of our database into our text file.
        """
        with open('Leaderboards.txt','w') as leaderboards:
            leaderboards.write('                             Leaderboards                             \n')
            leaderboards.write('Username             Wins          Losses          Ties          Score\n')
            leaderboards.write('----------------------------------------------------------------------\n')
            for entry in self.instance_database:
                leaderboards.write(self.create_string(entry[0],entry[1],entry[2],entry[3],entry[4]))

    def get_profiles(self):
        """
            This function reads in all the profiles from the text file and adds
            to the database.
        """
        self.leaderboards_check()
        l = 216
        line = None
        with open('Leaderboards.txt','r') as leaderboards:
            leaderboards.seek(l)
            line = leaderboards.readline()
            while ((len(line)) > 0):
                self.instance_database.append(self.get_profile(line))
                l += (len(line))
                line = leaderboards.readline()

    def name_is_there(self,name):
        """
            This function checks to see if the name is there in the database, as
            a helper function for when they enter a new name.
        """
        for entry in self.instance_database:
            if ((name.casefold()) == (entry[0].casefold())):
                return name
        return ''

    def enter_new_name(self):
        """
            This function enters a new name into our database.
        """
        self.instance_database = self.rank_database()
        self.leaderboards_check()
        self.write_to_file()
        new_name = self.new_username()
        name_in_database = self.name_is_there(new_name)
        while ((len(name_in_database)) != 0):
            print('Sorry, that name\'s taken, or you entered nothing.',end='')
            new_name = self.new_username()
            name_in_database = self.name_is_there(new_name)
        self.instance_database.append([new_name,0,0,0,0])
        self.instance_database = self.rank_database()
        self.write_to_file()

    def sign_in(self):
        """
            This function signs a player in based on their username.
        """
        i = 0
        player_to_sign_in = ''
        string_input = input('Press \'s\' to sign in, press \'n\' to enter a new name.\n')
        while (not((string_input.casefold()) in ['s','n'])):
            string_input = input('Invalid input. Press \'s\' to sign in, press \'n\' to enter a new name.\n')
        if ((string_input.casefold()) == 's'):
                mode = input('Press \'s\' for single player \'m\' for multiplayer (which mode you plan to play as).\n')
                while (not((mode.casefold()) in ['s','m'])):
                    mode = input('Invalid input. Press \'s\' for single player \'m\' for multiplayer (which mode you plan to play as).\n')
                if ((mode.casefold()) == 's'):
                    if ((len(self.instance_database)) == 0):
                        print('No entry in the leaderboard.',end='')
                        self.enter_new_name()
                        print('This is the name you will be signed in as.')
                        return[self.instance_database[0][0].casefold(),None]
                    else:
                        nones = self.number_of_nones(self.instance_players_signed_in)
                        if (nones == 0):
                            player_to_sign_in = input('There are 2 people signed in. Select 1 of \'{First_name}\' and\
 \'{second_name}\' to remove:'.format(First_name = self.instance_players_signed_in[0],second_name = self.instance_players_signed_in[1]))
                            while (not (player_to_sign_in.casefold() in self.instance_players_signed_in)):
                                player_to_sign_in = input('Invalid input. Select 1 of \'{First_name}\' and\
 \'{second_name}\' to remove:'.format(First_name = self.instance_players_signed_in[0],second_name = self.instance_players_signed_in[1]))
                            self.instance_players_signed_in[self.instance_players_signed_in.index(player_to_sign_in.casefold())] = None
                            if (self.instance_players_signed_in[0] == None):
                                self.instance_players_signed_in[0] = self.instance_players_signed_in[1].casefold()
                                self.instance_players_signed_in[1] = None
                            return self.instance_players_signed_in
                        elif (nones == 1):
                            if (self.instance_players_signed_in[0] == None):
                                i = 1
                            else:
                                i = 0
                            player_to_sign_in = input('There is only \'{First_name}\' signed in. Continue(Y/N)?'.format\
                                                     (First_name = self.instance_players_signed_in[i]))
                            while (not((player_to_sign_in.casefold()) in  ['y','n'])):
                                player_to_sign_in = input('Invalid input. Press \'y\' to stay signed in as \'{First_name}\'\
 or press \'n\' otherwise.'.format(First_name = self.instance_players_signed_in[i]))
                            if ((player_to_sign_in.casefold()) == 'y'):
                                return self.instance_players_signed_in
                            else:
                                if ((len(self.instance_database)) == 1):
                                    print('Only one person in the database. You can only be signed in as what you are now.')
                                    return self.instance_players_signed_in
                                name = input('Enter a username.\n')
                                is_there = self.name_is_there(name)
                                while (((len(is_there)) == 0) or (self.instance_players_signed_in[i] == name)):
                                    name = input('The name you registered as is not there or\
 has already been signed in. Enter a different name.\n')
                                    is_there = self.name_is_there(name)
                                return [name.casefold(),None]
                        else:
                            name = input('Enter a username.\n')
                            is_there = self.name_is_there(name)
                            while ((len(is_there)) == 0):
                                name = input('The name you registered as is not there. Enter a different name.\n')
                                is_there = self.name_is_there(name)
                            return [name.casefold(),None]
                else:
                    if ((len(self.instance_database)) == 0):
                        print('The leaderboards are empty. You will have to enter 2 names.')
                        self.enter_new_name()
                        self.enter_new_name()
                        print('These 2 names will be signed in when playing.')
                        return [self.instance_database[0][0].casefold(),self.instance_database[1][0].casefold()]
                    elif ((len(self.instance_database)) == 1):
                        print('Not enough names in the leaderboard. You must enter another.')
                        self.enter_new_name()
                        print('These 2 names will be signed in when playing.')
                        return [self.instance_database[0][0].casefold(),self.instance_database[1][0].casefold()]
                    else:
                        nones = self.number_of_nones(self.instance_players_signed_in)
                        if (nones == 0):
                            print('Two people are signed in already.')
                            return self.instance_players_signed_in
                        elif (nones == 1):
                            if (self.instance_players_signed_in[0] == None):
                                i = 1
                            else:
                                i = 0
                            name = input('One person signed in. Sign in another:')
                            is_there = self.name_is_there(name)
                            while (((len(is_there)) == 0) or (name == self.instance_players_signed_in[i])):
                                name = input('The name you registered as is not there or signed in. Enter a different name.\n')
                                is_there = self.name_is_there(name)
                            self.instance_players_signed_in = [self.instance_players_signed_in[i].casefold(),name.casefold()]
                            return self.instance_players_signed_in
                        else:
                            name = input('Enter the first username.\n')
                            is_there = self.name_is_there(name)
                            while ((len(is_there)) == 0):
                                name = input('The name you registered as is not there. Enter a different name.\n')
                                is_there = self.name_is_there(name)
                            second_name = input('Enter the second username.\n')
                            also_there = self.name_is_there(second_name)
                            while (((len(also_there)) == 0) or (second_name == name)):
                                second_name = input('The name you registered is not there or already entered. Enter a new name.\n')
                                also_there = self.name_is_there(second_name)
                            return [name.casefold(),second_name.casefold()]
        else:
            self.enter_new_name()
            return [None,None]

    def clear(self):
        """
            This function clears all profiles to have a 0.
        """
        for entry in self.instance_database:
            entry[1] = 0
            entry[2] = 0
            entry[3] = 0
            entry[4] = 0
        database = self.rank_database()
        self.write_to_file()


    def clear_names(self):
        """
            This function clears all the names in the database and writes accordingly
            to the file.
        """
        self.instance_database = []
        self.write_to_file()


    def clear_a_name(self):
        """
            This function takes in a username and removes it from the database,
            ranks the new database, and writes it to the file.
        """
        if ((len(self.instance_database)) == 0):
            print('Nothing to clear')
            return None
        name = input('Enter a username to remove:')
        is_there = self.name_is_there(name)
        while ((len(is_there)) == 0):
            name = input('This username does not exist. Enter another one:')
            is_there = self.name_is_there(name)
        for i in (range(len(self.instance_database))):
            if ((self.instance_database[i][0].casefold()) == (name.casefold())):
                self.instance_database.pop(i)
                self.instance_database = self.rank_database()
                self.write_to_file()
                break

    def sign_out(self):
        """
            This function signs a player out who is signed in.
        """
        string_input = ''
        nones = self.number_of_nones(self.instance_players_signed_in)
        if (nones == 0):
            string_input = input('Two people signed in. Press \'1\' to sign out 1 or \'2\' to sign out both.')
            while (not((string_input.casefold()) in ['1','2'])):
                string_input = input('Invalid input. Select \'1\' or \'2\' to sign out 1 or 2.')
            if (string_input == '1'):
                player_to_sign_in = input('Select 1 of \'{First_name}\' and\
     \'{second_name}\' to remove:'.format(First_name = self.instance_players_signed_in[0],second_name = self.instance_players_signed_in[1]))
                while (not (player_to_sign_in.casefold() in self.instance_players_signed_in)):
                    player_to_sign_in = input('Invalid input. Select 1 of \'{First_name}\' and\
     \'{second_name}\' to remove:'.format(First_name = self.instance_players_signed_in[0],second_name = self.instance_players_signed_in[1]))
                self.instance_players_signed_in[self.instance_players_signed_in.index(player_to_sign_in.casefold())] = None
                if (self.instance_players_signed_in[0] == None):
                    i = 1
                else:
                    i = 0
                self.instance_players_signed_in = [self.instance_players_signed_in[i].casefold(),None]
                return self.instance_players_signed_in
            else:
                self.instance_players_signed_in = [None,None]
                return self.instance_players_signed_in
        elif (nones == 1):
            string_input = input('One person signed in. Sign them out?(Y/N)')
            while (not((string_input.casefold()) in ['y','n'])):
                string_input = input('Invalid input. Select \'Y\' or \'N\' to sign them out or not.')
            if (string_input == 'y'):
                self.instance_players_signed_in = [None,None]
                return self.instance_players_signed_in
            else:
                return self.instance_players_signed_in
        else:
            print('Nobody is signed in')
            return [None,None]
