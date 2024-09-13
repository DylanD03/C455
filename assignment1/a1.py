# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification here: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/assignments/a1.html

import sys
import math

class CommandInterface:
    # The following is already defined and does not need modification
    # However, you may change or add to this code as you see fit, e.g. adding class variables to init

    def __init__(self):
        # Define the string to function command mapping
        self.command_dict = {
            "help" : self.help,
            "game" : self.game,
            "show" : self.show,
            "play" : self.play,
            "legal" : self.legal,
            "genmove" : self.genmove,
            "winner" : self.winner
        }

        self.grid = []
        self.width = 0
        self.height = 0
        self.player = 1
        self.row_count = {} # ex: { {row_num : {0: 0, 1: 0}}, {row_num_2 : {0: 0, 1: 0}} } 
        self.col_count = {}

        self.DEBUG = False # Set to False before submission
        self.ERROR = ""    # Error to output

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
    # Commands will automatically print '= 1' at the end of execution on success
    def main_loop(self):
        while True:
            str = input()
            if str.split(" ")[0] == "exit":
                print("= 1\n")
                return True
            if self.process_command(str):
                print("= 1\n")

    # List available commands
    def help(self, args):
        for command in self.command_dict:
            if command != "help":
                print(command)
        print("exit")
        return True

    #======================================================================================
    # End of predefined functionality. You will need to implement the following functions.
    # Arguments are given as a list of strings
    # We will only test error handling of the play command
    #======================================================================================

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

        if not self.canPlay(args, update=True):
            print(f"= illegal move: {' '.join(args)} {self.ERROR}") # illegal move: [input] [error]
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
                if self.canPlay([col, row, 0], update=True):
                    print(f"{col} {row} {0}")
                    return True
                if self.canPlay([col, row, 1], update=True):
                    print(f"{col} {row} {1}")
                    return True
                
        print("resign")
        return False
    
    def winner(self, args):
        # Iterate through every cell and see if available
        for row in range(self.height):      # row = y
            for col in range(self.width):   # col = x
                if self.canPlay([col, row, 0], update=False):
                    print("unfinished")
                    return True
                if self.canPlay([col, row, 1], update=False):
                    print("unfinished")
                    return True
                
        # print the winning player
        print(self.player + 1) 
        return True    
    
    def canPlay(self, args, update = False):
        # Check [errors] in the order given and save the first error only:

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
        
        # 4. Check if the cell is occupied
        if self.grid[y][x] != "." :
            if self.DEBUG: print("4.")
            self.ERROR = "occupied"
            return False
        
        # 5.1 check three in a row
        row = self.grid[y] # Only check the row being played
        tracker = 0
        for i in range(max(0, x - 2), min(self.width, x + 3)):  # Only check the range around [x-2,x+2] inclusive
            if (row[i] == play):  # If it's the same as the current play
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
        row_dict = self.row_count[y] # Retrieve Row being played # ex: row_dict={0: 2, 1: 0} 
        if row_dict[play]+1 > math.ceil(self.width / 2):
            if self.DEBUG: print("6.1")
            self.ERROR = f"too many {play}"
            return False
        # 6.2 Check for too many 0 or too many 1 in Column
        col_dict = self.col_count[x] # Retrieve Column being played  # ex: col_dict={0: 0, 1: 0} }
        if col_dict[play]+1 > math.ceil(self.height / 2):
            if self.DEBUG: print("6.2")
            self.ERROR = f"too many {play}"
            return False
        
        # Update Grid if neccessary
        if update == True:
            # update grid
            self.grid[y][x] = play
            self.row_count[y][play] += 1
            self.col_count[x][play] += 1
            self.player = not self.player # switch player

        return True
    
    #======================================================================================
    # End of functions requiring implementation                                                             
    #======================================================================================

if __name__ == "__main__":
    interface = CommandInterface()

    # Check if '--DEBUG' is used as a command line argument. ex usage: python3 a1.py --DEBUG
    if len(sys.argv)>1 and sys.argv[1]=="--DEBUG":
        print("Debugging mode activated")
        interface.DEBUG=True 

    interface.main_loop()