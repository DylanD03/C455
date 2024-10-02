# CMPUT 455 Assignment 2 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification here: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/assignments/a2.html

import sys
import random
import signal
import math
import time


class TranspositionTable:
# Table is stored in a dictionary, with board code as key, 
# Source: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/python/transposition_table_simple.py

    # Empty dictionary
    def __init__(self):
        self.table = {}

    # Used to print the whole table with print(tt)
    def __repr__(self):
        return self.table.__repr__()

    def store(self, code, score):
        # Score is either True (Win) or False (Loss)
        # Code is used as a key
        self.table[code] = score

    # Python dictionary returns 'None' if key not found by get()
    def lookup(self, code):
        return self.table.get(code)
    


class CommandInterface:

    def __init__(self):
        # Define the string to function command mapping
        self.command_dict = {
            "help" : self.help,
            "game" : self.game,
            "show" : self.show,
            "play" : self.play,
            "legal" : self.legal,
            "genmove" : self.genmove,
            "winner" : self.winner,
            "timelimit" : self.timelimit,
            "solve" : self.solve
        }

        # Assignment 2 Variables
        self.solvertimelimit = 1  # Before the first timelimit command is given, the default should be set to 1 second.
        self.winning_move = None  # [x, y, play]

        # Assignment 1 Variables
        self.grid = []
        self.width = 0
        self.height = 0
        self.player = 1     
        self.row_count = {} # ex: { {row_num : {0: 0, 1: 0}}, {row_num_2 : {0: 0, 1: 0}} } 
        self.col_count = {}

        self.DEBUG = False # Set to False before submission
        self.ERROR = ""    # Error to output
    
    #===============================================================================================
    # VVVVVVVVVV START of PREDEFINED FUNCTIONS. DO NOT MODIFY. VVVVVVVVVV
    #===============================================================================================

    # Convert a raw string to a command and a list of arguments
    def process_command(self, str):
        str = str.lower().strip()
        command = str.split(" ")[0]
        args = [x for x in str.split(" ")[1:] if len(x) > 0]
        if command not in self.command_dict:
            print("? Uknown command.\nType 'help' to list known commands.", file=sys.stderr)
            print("= -1\n")
            return False
        try:
            return self.command_dict[command](args)
        except Exception as e:
            print("Command '" + str + "' failed with exception:", file=sys.stderr)
            print(e, file=sys.stderr)
            print("= -1\n")
            return False
        
    # Will continuously receive and execute commands
    # Commands should return True on success, and False on failure
    # Every command will print '= 1' or '= -1' at the end of execution to indicate success or failure respectively
    def main_loop(self):
        while True:
            str = input()
            if str.split(" ")[0] == "exit":
                print("= 1\n")
                return True
            if self.process_command(str):
                print("= 1\n")

    # Will make sure there are enough arguments, and that they are valid numbers
    # Not necessary for commands without arguments
    def arg_check(self, args, template):
        converted_args = []
        if len(args) < len(template.split(" ")):
            print("Not enough arguments.\nExpected arguments:", template, file=sys.stderr)
            print("Recieved arguments: ", end="", file=sys.stderr)
            for a in args:
                print(a, end=" ", file=sys.stderr)
            print(file=sys.stderr)
            return False
        for i, arg in enumerate(args):
            try:
                converted_args.append(int(arg))
            except ValueError:
                print("Argument '" + arg + "' cannot be interpreted as a number.\nExpected arguments:", template, file=sys.stderr)
                return False
        args = converted_args
        return True

    # List available commands
    def help(self, args):
        for command in self.command_dict:
            if command != "help":
                print(command)
        print("exit")
        return True

    #===============================================================================================
    # ɅɅɅɅɅɅɅɅɅɅ END OF PREDEFINED FUNCTIONS. ɅɅɅɅɅɅɅɅɅɅ
    #===============================================================================================

    #===============================================================================================
    # VVVVVVVVVV START OF ASSIGNMENT 2 FUNCTIONS. ADD/REMOVE/MODIFY AS NEEDED. VVVVVVVV
                    # Dylan: I optimized and tested these functions 
    #===============================================================================================
    def game(self, args):
        # raise NotImplementedError("This command is not yet implemented.")

        # Check for correct number of arguments
        if len(args) != 2:
            if self.DEBUG: print("= illegal move: {args} wrong number of arguments", file=sys.stderr) # TODO: Check if neccesary: "[game] only requires the command status as output."
            return False
        
        # Check if the arguments are integers
        try:
            self.width = int(args[0])
            self.height = int(args[1])
        except ValueError:
            if self.DEBUG: print("= illegal move: wrong type of arguements", file=sys.stderr) # TODO: Check if necessary: "[game] only requires the command status as output."
            return False
        
        # Check if the width and height are in the range [1,20], inclusive.
        if not (1 <= self.width <= 20) or not (1 <= self.height <= 20): 
            if self.DEBUG: print("= illegal move: invalid dimensions", file=sys.stderr) # TODO: Check if necessary: "[game] only requires the command status as output."
            return False
        
        # Initialize the grid
        self.grid=[] # Reset grid
        for _ in range(self.height):
            temp = []
            for _ in range(self.width):
                temp.append(".")
            self.grid.append(temp)

        # initialize row and col counts
        for i in range(self.width):
            self.col_count[i] = {0: 0, 1: 0}

        for i in range(self.height):
            self.row_count[i] = {0: 0, 1: 0}

        # Initialize the player
        self.player = 1
        return True
    
    def show(self, args):
        # raise NotImplementedError("This command is not yet implemented.")

        # Check for correct number of arguments
        if len(args) != 0:
            if self.DEBUG: print("= illegal move: wrong number of arguments", file=sys.stderr) # TODO: Double check necessity
            return False
        
        # Print grid # grid is 2D array, self.grid[0] represents row 1.
        for i in self.grid: # For each row:  
            for j in i:     # For column in row:
                print(j, end="")
            print() # new line

        return True
    
    def play(self, args):
        if not self.validInput(args):
            print(f"= illegal move: {' '.join(args)} {self.ERROR}") #= illegal move: [input] [error]
            return False

        if not self.canPlay(args, update=True):
            print(f"= illegal move: {' '.join(args)} {self.ERROR}") #= illegal move: [input] [error]
            return False

        return True
    
    def legal(self, args):
       
        if self.canPlay(args):
            print("yes")
        else:
            print("no")

        return True

    def genmove(self, args):
        # Iterate through every cell and try playing it
        for row in range(self.height):      # row = y
            for col in range(self.width):   # col = x
                # Try playing 0
                if self.canPlay([col, row, 0], update=True):
                    print(f"{col} {row} {0}")
                    return True
                # Try playing 1
                if self.canPlay([col, row, 1], update=True):
                    print(f"{col} {row} {1}")
                    return True
                
        print("resign")
        return True
    
    def winner(self, args):
        # Iterate through every cell and see if available
        for row in range(self.height):      # row = y
            for col in range(self.width):   # col = x
                # Check if playing 0 is possible
                if self.canPlay([col, row, 0], update=False):
                    print("unfinished")
                    return True
                # Check if playing 1 is possible
                if self.canPlay([col, row, 1], update=False):
                    print("unfinished")
                    return True
                
        # print the winning player
        print(self.otherPlayer())  # Print the other player
        return True    

    def validInput(self, args):
        # 1. Check for correct number of arguments:
        if len(args) != 3:
            if self.DEBUG: print("1.")
            self.ERROR = "wrong number of arguments"
            return False

        # 2.1 Check if the x or y coordinates are integers:
        try:
            x = int(args[0])
            y = int(args[1])
        except ValueError:
            if self.DEBUG: print("2.1")
            self.ERROR = "wrong coordinate"
            return False

        # 2.2 Check if the x and y are within the grid
        if x < 0 or x > self.width-1 or y < 0 or y > self.height-1:
            if self.DEBUG: print("2.2")
            self.ERROR = "wrong coordinate"
            return False
        
        # 3.1 Check if the third argument is an Integer:
        try:
            play = int(args[2])
        except ValueError:
            if self.DEBUG: print("3.1")
            self.ERROR = "wrong number"
            return False
        
        # 3.2 Check if the third argument that a digit 0 or 1
        if play not in [0, 1]:
            if self.DEBUG: print("3.2")
            self.ERROR = "wrong number"
            return False
        
        return True
    
    def canPlay(self, args, update = False):
        # Assumption: input is already validated
        x = int(args[0])
        y = int(args[1])
        play = int(args[2])
        
        # 4. Check if the cell is occupied
        if self.grid[y][x] != "." :
            if self.DEBUG: print("4.")
            self.ERROR = "occupied"
            return False
        
        # 5.1 check three in a row
        tracker = 0
        for i in range(max(0, x - 2), min(self.width, x + 3)):  # Only check the range around [x-2,x+2] inclusive
            if (self.grid[y][i] == play):  # If it's the same as the current play
                tracker += 1
            elif i == x : # If we are looking at the play location
                tracker += 1
            else:
                tracker = 0  

            if tracker == 3: 
                if self.DEBUG: print("5.1")
                self.ERROR = "three in a row"
                return False
        
        # 5.2 check three in a col
        tracker = 0
        for col in range(max(0, y - 2), min(self.height, y + 3)):  # Only check the range around [y-2,y+2] inclusive
            if (self.grid[col][x] == play):  # If it's the same as the current play
                tracker += 1
            elif col == y: # If we are looking at the play location
                tracker += 1
            else:
                tracker = 0

            if tracker == 3:
                if self.DEBUG: print("5.2")
                self.ERROR = "three in a row"
                return False
            
        # 6.1 Check for too many 0 or too many 1 in Row
        if self.row_count[y][play]+1 > math.ceil(self.width / 2):
            if self.DEBUG: print("6.1")
            self.ERROR = f"too many {play}"
            return False
        # 6.2 Check for too many 0 or too many 1 in Column
        if self.col_count[x][play]+1 > math.ceil(self.height / 2):
            if self.DEBUG: print("6.2")
            self.ERROR = f"too many {play}"
            return False
        
        # Update Grid if neccessary
        if update == True:
            # update grid
            self.grid[y][x] = play
            self.row_count[y][play] += 1
            self.col_count[x][play] += 1
            self.player = self.otherPlayer() # Swap players 1->2 or 2->1

        return True

    def otherPlayer(self):
        return 2 if self.player == 1 else 1
    
    #===============================================================================================
    # ɅɅɅɅɅɅɅɅɅɅ NEW ASSIGNMENT 2 FUNCTIONS. ɅɅɅɅɅɅɅɅɅɅ
    #===============================================================================================

    # Set a timeout period
    def timelimit(self, args):
        # This function is called by typing "timeout [seconds]" into the game interface, where seconds is an integer.
        seconds = int(args[0]) # seconds is an integer in the range [1,100]
        self.solvertimelimit = seconds
        return True
    
    # Handles timeout signal
    def handler(self, signum, frame):
        # This function is called when the time limit is reached.
        raise TimeoutError() 
    
    def endOfGame(self):
        # Iterate through every cell and see if available
        for row in range(self.height):      # row = y
            for col in range(self.width):   # col = x
                # Check if playing 0 is possible
                if self.canPlay([col, row, 0], update=False):
                    return False
                # Check if playing 1 is possible
                if self.canPlay([col, row, 1], update=False):
                    return False
        # No Possible moves for the player
        return True    
    
    def getLegalMoves(self):
        all_moves = []
        # Iterate through every cell and see if available
        for row in range(self.height):      # row = y
            for col in range(self.width):   # col = x
                # Check if playing 0 is possible
                if self.canPlay([col, row, 0], update=False):
                    all_moves.append([col, row, 0])
                # Check if playing 1 is possible
                if self.canPlay([col, row, 1], update=False):
                     all_moves.append([col, row, 1])
        return all_moves
    
    def undoMove(self, last_move):
        # Read arguments # last_move = [col, row, 0]
        x = last_move[0] # col = x
        y = last_move[1] # row = y
        play = last_move[2]

        # Undo move
        self.grid[y][x] = "."
        self.row_count[y][play] -= 1
        self.col_count[x][play] -= 1
        self.player = self.otherPlayer() # undo player

    
    def storeResult(self, tt, result):
        # Stores our current state into the transposition table.
        # Credit: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/python/boolean_negamax_tt.py
        tt.store(self.code(), result)

        # TODO: tt.store Reflections and Rotations
            # Rotate/Reflect the board and store it. Much faster than recomputing from scratch.

        # TODO: tt.store Flipped versions (i.e. 1->0 and 0->1)
            # Suppose we had the board ([[1,0],[0,0]], self.player=1)
            # We could store ([[0,1], [1,1]], self.player=1)
        return result
    
    def code(self):
        # Returns the encoded (tuple) version of our current state
        # Map each row into a tuple. Then wrap all rows in a tuple.
        board_tuple = tuple(map(tuple, self.grid))  # Ex: ((1, 0), ('.', 1))
        return (board_tuple, self.player) 
        
    def negamaxBoolean(self, tt):
        # negamaxBoolean is always in perspective of current player (self.player)
        result = tt.lookup(self.code())
        if result != None:
            return result # Negamax result found in tt
        if self.endOfGame():
            result = self.staticallyEvaluateForToPlay()
            return self.storeResult(tt, result) 
        for move in self.getLegalMoves():
            self.play(move)
            success = not self.negamaxBoolean(tt)
            self.winning_move = move
            self.undoMove(move)
            if success:
                return self.storeResult(tt, True) # Store for later
        return self.storeResult(tt, False) 
    
    def staticallyEvaluateForToPlay(self):
        # At end of Binary Game, whoever is the current player loses
        return False # current player loses
    

    # New function to be implemented for assignment 2
    def solve(self, args):
        # Instantiate our Transposition Table
        tt = TranspositionTable()

        # Raise a TimeoutError after a certain time limit is reached.
        signal.signal(signal.SIGALRM, self.handler)
        signal.alarm(self.solvertimelimit) # set time limit

        try:    
            # Solving always starts with the current player (toPlay) going first
            if self.negamaxBoolean(tt):
                # Current Player has a winning solution
                print(f'{self.player} {self.winning_move[0]} {self.winning_move[1]} {self.winning_move[2]}')  # Output: winner <move>. Where move is formatted as: x y digit
            else:
                # See if other player has a winning solution
                for move in self.getLegalMoves():
                    self.play(move) 

                    # Find a winning response
                    if not self.negamaxBoolean(tt):
                        # Other player cannot find a winning solution
                        print("unknown") # Neither perspective is solved.
                        self.undoMove(move)
                        break # exit loop
                    
                    # Try another move.
                    self.undoMove(move)

                # Other player has a winning solution for every move Current Player can make. 
                print(f'{self.otherPlayer()}') # Print the winning player's number
        
        except TimeoutError:
             # Write unknown if your solver cannot solve the game within the current time limit. 
            print("unknown")
        finally: 
            signal.alarm(0) # disable signal timer

        return True

    
    #===============================================================================================
    # ɅɅɅɅɅɅɅɅɅɅ END OF ASSIGNMENT 2 FUNCTIONS. ɅɅɅɅɅɅɅɅɅɅ
    #===============================================================================================
    
if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()









