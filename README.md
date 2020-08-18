<h1 align = "center">Tic Tac Toe<h1>
<p>
This is a Tic Tac Toe game I wrote. I created a multiplayer version, and a single player version using the minimax algorithm. I also created a system that allows users to create 
profiles to play as, after which the game would save their progress and rank users based on their performances in the single and multiplayer arenas. 
</p>
<h2 align = "center">Program Structure</h2>
<p>
The program was desiged in OOP design, with modules that contained classes representing various functionalities the game would have. For example, you have the game_tracking_variables
 module that stored all the variables essential for the game to operate, as the game would be modifying these variables. The input_methods module represents anything that was 
related to user interaction - such as getting data from the user. The print_methods module did the same but with anything related to output. The checker_fns module was anything 
that related to checking the state of the game. The artificial_intelligence module was anything related to the A.I. The game_module module was the game in itself. The 
file_and_database_module had to do with the system that kept track of user profiles and ranked them. The main_menu module is the one that put it all together and is the one that 
you should run in command line. One option I had instead of writing to text files in the file_and_database module was using an sqlite database. However, at the time I designed 
the program I had no working knowledge of SQL, let alone the SQLite database. I have since taken a course in SQL using SQLite, so in the future you may see this implementation 
time willing. 
</p>
<h2 align = "center">Program Installation Instructions</h2>
<p>
1) Download all the files and save them in the same directory. Don't change any of the names!<br>
2) Make sure there is no file called "Leaderboards.txt" in this directory. If there is, delete it! It WILL destroy the program otherwise!<br>
3) Navigate to this directory in the command line.<br>
4) Type this word for word: "python main_menu.py"<br>
5) Enjoy!
</p>
