import os
import sqlite3

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
        self.instance_constraints = ['username TEXT NOT NULL UNIQUE',\
                                     'wins INTEGER NOT NULL',\
                                     'losses INTEGER NOT NULL',\
                                     'ties INTEGER NOT NULL',\
                                     'score INTEGER NOT NULL']
        self.instance_leaderboards_header = \
        ['                             Leaderboards                             ',\
         'username             wins          losses          ties          score',\
         '----------------------------------------------------------------------']

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

    def create_leaderboards(self):
        """
            This function creates a new database from scratch. This is used as a helper
            for our protocol when making sure that the necessary .db files are both there
            an are as they should be.
        """
        with sqlite3.connect("Leaderboards.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE Leaderboards(
                              username TEXT NOT NULL UNIQUE,
                              wins INTEGER NOT NULL,
                              losses INTEGER NOT NULL,
                              ties INTEGER NOT NULL,
                              score INTEGER NOT NULL
                              )
                           """)
            connection.commit()

    def check_constraints(self):
        """
            This function checks to ensure the proper constraints are in the database.
            This is used as a helper function to the check_validity_of_database function
            below.
        """
        # Code to grab the constraints for the database found here:
        # https://stackoverflow.com/questions/9636053/is-there-a-way-to-get-the-constraints-of-a-table-in-sqlite
        with sqlite3.connect("Leaderboards.db") as connection:
            cur = connection.cursor()
            cur.execute("select sql from sqlite_master where type='table' and name='Leaderboards'")
            schema = cur.fetchone()
        # So check that there are only five constraints, check and that all of them are
        # what we set beforehand.
        database_constraints = [ tmp.strip(", ") for tmp in schema[0].splitlines() if\
                                 tmp.find("NOT NULL")>=0 or tmp.find("UNIQUE")>=0 ]
        only_5_constraints = ((len(database_constraints)) == 5)
        # So we filter out the database constraints based on if they are in the
        # class property in the beginning that has all constraints. We turn this
        # iterable into a list, and then check to make sure that the length of
        # the filtered list is the length of the global list we have, which is 5.
        all_constraints_valid = ((len(list(filter(lambda constraint : constraint in self.instance_constraints,\
                                                  database_constraints)))) == 5)
        return (all_constraints_valid and only_5_constraints)

    def check_validity_of_database(self):
        """
            If we have established the database exists, this function is run to check
            the validity of the database.
        """
        cursor = None
        with sqlite3.connect("Leaderboards.db") as connection:
            cursor = connection.cursor()
            # Fetch all the tables from the database we found.
            tables_in_db_file = cursor.execute("""SELECT name FROM sqlite_master
                                                  WHERE type = \"table\"
                                                  """)
            total_tables = tables_in_db_file.fetchall()
            one_table_only = ((len(total_tables)) == 1)
            # Check that we have one table, and that this table is called Leaderboards
            if (one_table_only and (total_tables[0][0] == 'Leaderboards')):
                # Code for column names below found here:
                # https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite
                # We find the column names, and check that they match what they should
                # be. We check that these are also the only columns that exist. We
                # do all this to check and make sure that we have only one table
                # and it holds up to what it should be. If not, the data has possibly
                # been corrupted, and we can't trust it. We delete it and create another
                # database.
                iterable = cursor.execute('select * from Leaderboards')
                names = list(map(lambda x: x[0], iterable.description))
                valid_columns_in_table = (("username" in names) and\
                                          ("wins" in names) and ("losses" in names) and\
                                          ("ties" in names) and ("score" in names))
                five_columns_only = ((len(names)) == 5)
                valid_constraints = self.check_constraints()
            else:
                # Otherwise return false since we don't have only one table named
                # what it should be
                return False
        # Returns true if the table has valid columns, only 5 columns, and all
        # constraints are valid.
        return (valid_columns_in_table and five_columns_only and valid_constraints)

    def check_leaderboards(self):
        """
            This function checks that a valid leaderboard database exists in the
            surrounding directory, then creates one in the event that it doesn't
            exist.
        """
        present_directory = os.getcwd()
        file_exists_in_directory = os.path.exists(present_directory + '\\Leaderboards.db')
        valid_existing_database = None
        if (file_exists_in_directory):
            valid_existing_database = self.check_validity_of_database()
            if (not valid_existing_database):
                # If the existing leaderboards database does not pass our test, we can
                # assume the data has been corrupted and thus delete and recreate the database
                os.remove('Leaderboards.db')
                # We remove it in a separate function, since python throws an error
                # if we ran it with a context manager to our Leaderboards database.
                self.create_leaderboards()
        else:
            # File does not exist, so create it
            self.create_leaderboards()

    def get_and_sort_profiles(self):
        """
            This function sorts our profiles based on their scores, and then on alphabetical
            order if scores are equal.
        """
        self.check_leaderboards()
        index = 0
        # we execute the select query and assign to transferring_list, then send it to
        # equal_entries_list as equal to transferring_list.fetchall()
        transferring_list = None
        equal_entries_list = None
        with sqlite3.connect("Leaderboards.db") as connection:
            cursor = connection.cursor()
            entries = cursor.execute("SELECT rowid, * FROM Leaderboards ORDER BY score DESC")
            total_entries = entries.fetchall()
            # We have the total entries in a list, ordered by score. From here, we have
            # to sort out profiles with identical scores by the alphabetical order of their
            # username. We do this by checking if the current profile matches the score of the
            # next. We then run a select query from our database where the score equals
            # this score and order by the username. Once we did the above, we then
            # increment the index, and place the returned results into the database.
            # We now have that profiles with the same scores are alphabetically ordered by
            # their username. I'm not sure, but I believe SQLite is better suited
            # for sorting, especially with hundreds of thousands of entries, so
            # I want SQLite to do as much of this as possible.
            while (index < ((len(total_entries)) - 1)):
                if (total_entries[index][5] == total_entries[index + 1][5]):
                    transferring_list = cursor.execute("SELECT rowid, * FROM Leaderboards\
                    WHERE score = " + str(total_entries[index][5]) + " ORDER BY username")
                    equal_entries_list = transferring_list.fetchall()
                    for entry in equal_entries_list:
                        total_entries[index] = entry
                        index += 1
                else:
                    index += 1
            return total_entries

    def update_records(self, username, wins, losses, ties, score):
        with sqlite3.connect("Leaderboards.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""UPDATE Leaderboards SET wins = ?, losses = ?, ties = ?,
            score = ? WHERE username = ?""", (wins, losses, ties, score, username))
            connection.commit()

    def clear(self):
        """
            This function clears all profiles to have a 0.
        """
        for entry in self.instance_database:
            self.update_records(entry[1], 0, 0, 0, 0)
        self.instance_database = self.get_and_sort_profiles()
        #self.write_to_file()

    def delete_records(self, username = None):
        """
            This function deletes your records, and is used when the user asks to clear the
            leaderboards. The function takes an optional argument for the username to delete.
            If it's set to its default value of none, everything is removed. Otherwise
            that specific username is gone.
        """
        with sqlite3.connect("Leaderboards.db") as connection:
            cursor = connection.cursor()
            if (username == None):
                cursor.execute("DELETE FROM Leaderboards")
                connection.commit()
            else:
                cursor.execute("DELETE FROM Leaderboards WHERE username = " + "\""\
                                + username + "\"")
                connection.commit()

    def create_record(self, username, wins, losses, ties, score):
        """
            This function creates a new record in the database.
        """
        with sqlite3.connect("Leaderboards.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO Leaderboards VALUES(?,?,?,?,?)""",\
                           (username, wins, losses, ties, score))

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
            if ((self.instance_database[i][1].casefold()) == name.casefold()):
                the_single_player = i
                break
        username = self.instance_database[the_single_player][1]
        wins = self.instance_database[the_single_player][2]
        losses = self.instance_database[the_single_player][3]
        ties = self.instance_database[the_single_player][4]
        score = self.instance_database[the_single_player][5]
        # Duplication with the function is necessary, as different fields are updated
        # based on the case.
        hard = game_variable_object.instance_translate_difficulty_to_recursion_levels['Hard']
        medium = game_variable_object.instance_translate_difficulty_to_recursion_levels['Medium']
        if win:
            wins += 1
            if (difficulty == hard):
                score += 6
            elif (difficulty == medium):
                score += 5
            else:
                score += 4
        elif loss:
            losses += 1
            if (difficulty == hard):
                score -= 4
            elif (difficulty == medium):
                score -= 5
            else:
                score -= 6
        else:
            ties += 1
            if (difficulty == hard):
                score += 3
            elif (difficulty == medium):
                score += 2
            else:
                score += 1
        self.update_records(username, wins, losses, ties, score)
        self.instance_database = self.get_and_sort_profiles()

    # The additions or subtractions to the individuals' scores are different
    # than result_score_single_player because the scoring system
    # adds differently. There's a function down below that prints the rules.
    def result_score_multiplayer(self,name,second_name,win,loss,tie):
        """
            This function takes care of adjusting the according results to the according
            players when the multiplayer version is run.
        """
        first_player = None
        second_player = None
        if (name == ''):
            return None
        # If nobody was registered, then we're done above. Otherwise, find the
        # indices according to who was playing and then update their profiles
        # according to the results.
        for i in (range(len(self.instance_database))):
            if ((name.casefold()) == (self.instance_database[i][1].casefold())):
                first_player = i
            elif ((second_name.casefold()) == (self.instance_database[i][1].casefold())):
                second_player = i
            if (not ((first_player == None) or (second_player == None))):
                break

        first_player_name = self.instance_database[first_player][1]
        first_player_wins = self.instance_database[first_player][2]
        first_player_losses = self.instance_database[first_player][3]
        first_player_ties = self.instance_database[first_player][4]
        first_player_score = self.instance_database[first_player][5]

        second_player_name = self.instance_database[second_player][1]
        second_player_wins = self.instance_database[second_player][2]
        second_player_losses = self.instance_database[second_player][3]
        second_player_ties = self.instance_database[second_player][4]
        second_player_score = self.instance_database[second_player][5]

        if win:
            first_player_wins += 1
            second_player_losses += 1
            first_player_score += 2
            second_player_score -= 2
        elif loss:
            first_player_losses += 1
            first_player_score -= 2
            second_player_wins += 1
            second_player_score += 2
        else:
            first_player_ties += 1
            second_player_ties += 1
            second_player_score += 1
            first_player_score += 1
        self.update_records(first_player_name, first_player_wins, first_player_losses,\
                            first_player_ties, first_player_score)
        self.update_records(second_player_name, second_player_wins, second_player_losses,\
                            second_player_ties, second_player_score)
        self.instance_database = self.get_and_sort_profiles()

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
        new_line += ((self.add_spaces(65 - (len(list(new_line))))) + (str(score)))
        return new_line

    def print_leaderboards(self):
        """
            This function reads in strings from our text file and displays our Leaderboards.
        """
        for line in self.instance_leaderboards_header:
            print(line)
        self.instance_database = self.get_and_sort_profiles()
        for line in self.instance_database:
            print(self.create_string(line[1], line[2], line[3], line[4], line[5]))


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

    def name_is_there(self,name):
        """
            This function checks to see if the name is there in the database, as
            a helper function for when they enter a new name.
        """
        for entry in self.instance_database:
            if ((name.casefold()) == (entry[1].casefold())):
                return name
        return ''

    def enter_new_name(self):
        """
            This function enters a new name into our database.
        """
        #self.instance_database = self.rank_database()
        #self.leaderboards_check()
        #self.write_to_file()
        self.check_leaderboards()
        self.instance_database = self.get_and_sort_profiles()
        new_name = self.new_username()
        name_in_database = self.name_is_there(new_name)
        while ((len(name_in_database)) != 0):
            print('Sorry, that name\'s taken, or you entered nothing.',end='')
            new_name = self.new_username()
            name_in_database = self.name_is_there(new_name)
        self.create_record(new_name, 0, 0, 0, 0)

    def single_player_case(self):
        """
            This is a helper function that handles the single player case when
            the user wants to sign in and presses s.
        """
        # When there's no names in the database.
        if ((len(self.instance_database)) == 0):
            print('No entry in the leaderboard.',end='')
            self.enter_new_name()
            print('This is the name you will be signed in as.')
            return [self.instance_database[0][0].casefold(),None]
        else:
            nones = self.number_of_nones(self.instance_players_signed_in)
            # If there are 0 nones, or 2 people signed in, do this,choose to remove one of them.
            if (nones == 0):
                player_to_sign_in = input('There are 2 people signed in. Select 1 of \'{First_name}\' and\
\'{second_name}\' to remove. Be case sensitive: '.format(\
                First_name = self.instance_players_signed_in[0],\
                second_name = self.instance_players_signed_in[1]))
                while (not (player_to_sign_in.casefold() in self.instance_players_signed_in)):
                    player_to_sign_in = input('Invalid input. Select 1 of \'{First_name}\' and\
\'{second_name}\' to remove. Be case sensitive: '.format(\
                    First_name = self.instance_players_signed_in[0],\
                    second_name = self.instance_players_signed_in[1]))
                self.instance_players_signed_in[self.instance_players_signed_in.index(player_to_sign_in.casefold())] = None
                # If the name is at the second spot of the list, cut and paste it into
                # the first spot.
                if (self.instance_players_signed_in[0] == None):
                    self.instance_players_signed_in[0] = self.instance_players_signed_in[1].casefold()
                    self.instance_players_signed_in[1] = None
                return self.instance_players_signed_in
            elif (nones == 1):
                # If we have only one person signed in, we do this.
                i = 0
                if (self.instance_players_signed_in[0] == None):
                    i = 1
                # They can continue as this person, or be someone else so long
                # as someone else is in the database.
                player_to_sign_in = input('There is only \'{First_name}\' signed in. Continue(Y/N)?'.format\
                                         (First_name = self.instance_players_signed_in[i]))
                while (not((player_to_sign_in.casefold()) in  ['y','n'])):
                    player_to_sign_in = input('Invalid input. Press \'y\' to stay signed in as \'{First_name}\'\
or press \'n\' otherwise.'.format(First_name = self.instance_players_signed_in[i]))
                if ((player_to_sign_in.casefold()) == 'y'):
                    return self.instance_players_signed_in
                else:
                    # If they say no but there's only one person, they have to sign out
                    # and enter a new name. Otherwise, they can enter a new name in the
                    # database.
                    if ((len(self.instance_database)) == 1):
                        print('Only one person in the database.\
 You can only be signed in as what you are now, or sign out of this name in the\
 main menu and enter a new username in the database.')
                        return self.instance_players_signed_in
                    name = input('Enter a username.\n')
                    is_there = self.name_is_there(name)
                    while (((len(is_there)) == 0) or (self.instance_players_signed_in[i] == name)):
                        name = input('The name you registered as is not there or\
has already been signed in. Enter a different name.\n')
                        is_there = self.name_is_there(name)
                    return [name.casefold(),None]
            else:
                name = input('Nobody is signed in. Enter a username.\n')
                is_there = self.name_is_there(name)
                while ((len(is_there)) == 0):
                    name = input('The name you registered as is not there.\
 Enter a different name.\n')
                    is_there = self.name_is_there(name)
                return [name.casefold(),None]

    def multiplayer_case(self):
        """
            This helper function is called the event that the user wants to play multiplayer,
            and thus 2 names need to be signed in.
        """
        # When the database has no names, enter 2 names.
        if ((len(self.instance_database)) == 0):
            print('The leaderboards are empty. You will have to enter 2 names.')
            self.enter_new_name()
            self.enter_new_name()
            print('These 2 names will be signed in when playing.')
            return [self.instance_database[0][0].casefold(),self.instance_database[1][0].casefold()]
        # If the database has 1 name, enter another.
        elif ((len(self.instance_database)) == 1):
            print('Not enough names in the leaderboard. You must enter another.')
            self.enter_new_name()
            print('These 2 names will be signed in when playing.')
            return [self.instance_database[0][0].casefold(),self.instance_database[1][0].casefold()]
        # Go through cases of various people signed in
        else:
            nones = self.number_of_nones(self.instance_players_signed_in)
            # nones represents how many none values are in the instance_players_signed_in
            # instance variable. If there are 0, then 2 people are signed in already
            if (nones == 0):
                print('Two people are signed in already.')
                return self.instance_players_signed_in
            # If there's one person signed in, sign in another.
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
            # If there is nobody signed in, then enter 2 names and verify that the entries
            # are valid.
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

    def sign_in(self):
        """
            This function signs a player in based on their username.
        """
        self.instance_database = self.get_and_sort_profiles()
        # Make sure no values from previous players signed in have been deleted.
        name_not_deleted = False
        second_name_not_deleted = False
        for entry in self.instance_database:
            # Extra conditionals to make sure that we don't search for
            # something after it has already been found
            if (not name_not_deleted):
                if ((entry[1].casefold()) ==\
                    (self.instance_players_signed_in[0].casefold())):
                    name_not_deleted = True
                    self.instance_players_signed_in[0] = None
            if (not second_name_not_deleted):
                if ((entry[1].casefold()) ==\
                    (self.instance_players_signed_in[1].casefold())):
                    second_name_not_deleted = True
                    self.instance_players_signed_in[1] = None
            if (name_not_deleted and second_name_not_deleted):
                break
        i = 0
        player_to_sign_in = ''
        string_input = input('Press \'s\' to sign in, press \'n\' to enter a new name.\n')
        while (not((string_input.casefold()) in ['s','n'])):
            string_input = input('Invalid input. Press \'s\' to sign in,\
 press \'n\' to enter a new name.\n')
        if ((string_input.casefold()) == 's'):
                mode = input('Press \'s\' for single player \'m\'\
 for multiplayer (which mode you plan to play as).\n')
                while (not((mode.casefold()) in ['s','m'])):
                    mode = input('Invalid input. Press \'s\' for single player \'m\'\
 for multiplayer (which mode you plan to play as).\n')
                if ((mode.casefold()) == 's'):
                    return self.single_player_case()
                else:
                    return self.multiplayer_case()
        else:
            self.enter_new_name()
            return [None,None]


    def clear_names(self):
        """
            This function clears all the names in the database and writes accordingly
            to the file.
        """
        self.delete_records()
        self.instance_database = []
        #self.write_to_file()


    def clear_a_name(self):
        """
            This function takes in a username and removes it from the database,
            ranks the new database, and writes it to the file.
        """
        self.instance_database = self.get_and_sort_profiles()
        if ((len(self.instance_database)) == 0):
            print('Nothing to clear')
            return None
        name = input('Enter a username to remove:')
        is_there = self.name_is_there(name)
        while ((len(is_there)) == 0):
            name = input('This username does not exist. Enter another one. It is case sensitive: ')
            is_there = self.name_is_there(name)
        self.delete_records(is_there)

    def sign_out(self):
        """
            This function signs a player out who is signed in.
        """
        self.instance_database = self.get_and_sort_profiles()
        # Make sure no values from previous players signed in have been deleted.
        name_not_deleted = False
        second_name_not_deleted = False
        for entry in self.instance_database:
            # Extra conditionals to make sure that we don't search for
            # something after it has already been found
            if (not name_not_deleted):
                if ((entry[1].casefold()) ==\
                    (self.instance_players_signed_in[0].casefold())):
                    name_not_deleted = True
                    self.instance_players_signed_in[0] = None
            if (not second_name_not_deleted):
                if ((entry[1].casefold()) ==\
                    (self.instance_players_signed_in[1].casefold())):
                    second_name_not_deleted = True
                    self.instance_players_signed_in[1] = None
            if (name_not_deleted and second_name_not_deleted):
                break
        string_input = ''
        nones = self.number_of_nones(self.instance_players_signed_in)
        if (nones == 0):
            string_input = input('Two people signed in. Press \'1\' to sign out 1\
 or \'2\' to sign out both.')
            while (not((string_input.casefold()) in ['1','2'])):
                string_input = input('Invalid input. Select \'1\' or \'2\' to sign out 1 or 2.')
            if (string_input == '1'):
                player_to_sign_in = input('Select 1 of \'{First_name}\' and\
 \'{second_name}\' to remove:'.format(First_name = self.instance_players_signed_in[0],\
                                      second_name = self.instance_players_signed_in[1]))
                while (not (player_to_sign_in.casefold() in self.instance_players_signed_in)):
                    player_to_sign_in = input('Invalid input. Select 1 of \'{First_name}\' and\
 \'{second_name}\' to remove:'.format(First_name = self.instance_players_signed_in[0],\
                                      second_name = self.instance_players_signed_in[1]))
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
                string_input = input('Invalid input. Select \'Y\' or \'N\' to sign\
 them out or not.')
            if (string_input == 'y'):
                self.instance_players_signed_in = [None,None]
                return self.instance_players_signed_in
            else:
                return self.instance_players_signed_in
        else:
            print('Nobody is signed in')
            return [None,None]
