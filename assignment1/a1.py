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
        self.row_count = {}
        self.col_count = {}

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
            print("= illegal move: {args} wrong number of arguments", file=sys.stderr)
            return False
        
        # Check if the arguments are integers
        try:
            self.width = int(args[0])
            self.height = int(args[1])
        except ValueError:
            print("= illegal move: wrong type of arguements", file=sys.stderr)
            return False
        
        # Check if the width and height are more than one
        # TODO: whats the min dimension size?------------------------
        if self.width <= 1 <= 20 or self.height <= 1 <= 20: 
            print("= illegal move: invalid dimensions", file=sys.stderr)
            return False
        
        # Initialize the grid
        for _ in range(self.height):
            temp = []
            for _ in range(self.width):
                temp.append(".")
                
            self.grid.append(temp)

        # initialize row and col counts
        for i in range(self. width):
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
            print("= illegal move: wrong number of arguments", file=sys.stderr)
            return False
        
        # Print grid
        for i in self.grid:
            for j in i:
                print(j, end="")
            print() # new line

        return True
    
    def play(self, args):
        # raise NotImplementedError("This command is not yet implemented.")

        # Check for correct number of arguments
        if len(args) != 3:
            print("= illegal move: wrong number of arguments", file=sys.stderr)
            return False

        # Check if the arguments are integers
        try:
            x = int(args[0])
            y = int(args[1])
            play = int(args[2])
            # print("x: ", x, "y: ", y, "play: ", play)
        except ValueError:
            print("= illegal move: wrong type of arguements", file=sys.stderr)
            return False
        
        # Check if the x and y are within the grid
        if x < 0 or x > self.width-1 or y < 0 or y > self.height-1:
            print("= illegal move: wrong coordinate", file=sys.stderr)
            return False
        
        #  Any third argument that is not a digit 0 or 1
        if play not in [0, 1]:
            print("= illegal move: wrong number", file=sys.stderr)
            return False
        
        # Check if the cell is empty
        if self.grid[y][x] != "." :
            print("= illegal move: occupied", file=sys.stderr)
            return False
        
        # check too many 0 or too many 1
        for k, v in self.row_count.items():
            if v[0] > math.ceil(self.height / 2) or v[1] > math.ceil(self.height / 2):
                print("= illegal move: too many 0", file=sys.stderr)
                return False
            
            if v[1] > math.ceil(self.height / 2):
                print("= illegal move: too many 1", file=sys.stderr)
                return False
            
        # update grid
        self.grid[y][x] = play
        
        # check three in a row
        for i in self.grid:
            tracker = 0
            prev = None

            for j in i:
                if j == prev and j.isdigit():
                    tracker += 1
                else:
                    tracker = 0

                if tracker == 2:
                    print("= illegal move: three in a row", file=sys.stderr)
                    self.grid[y][x] = "."
                    return False
                
                prev = j
        
        # check three in a col
        for col in range(len(self.grid[0])): 
            tracker = 0
            prev = None

            for row in range(len(self.grid)):
                if self.grid[row][col] == prev and self.grid[row][col].isdigit():
                    tracker += 1
                else:
                    tracker = 0

                if tracker == 2:
                    print("= illegal move: three in a row", file=sys.stderr)
                    self.grid[y][x] = "."
                    return False
                
                prev = self.grid[row][col]

        # Update the grid
        self.row_count[y][play] += 1
        self.col_count[x][play] += 1

        return True
    
    def legal(self, args):
        # raise NotImplementedError("This command is not yet implemented.")

        # Check for correct number of arguments
        if len(args) != 3:
            print("no", file=sys.stderr)
            return False

        # Check if the arguments are integers
        try:
            x = int(args[0])
            y = int(args[1])
            play = int(args[2])
        except ValueError:
            print("no", file=sys.stderr)
            return False
        
        # Check if the x and y are within the grid
        if x < 0 or x > self.width-1 or y < 0 or y > self.height-1:
            print("no", file=sys.stderr)
            return False
        
        #  Any third argument that is not a digit 0 or 1
        if play != 0 or play != 1:
            print("no", file=sys.stderr)
            return False
        
        # Check if the play is within the grid
        if play != 1 or play != 0:
            print("no", file=sys.stderr)
            return False
        
        # Check if the cell is empty
        if self.grid[y][x] != "." :
            print("no", file=sys.stderr)
            return False
        
        # check too many 0 or too many 1
        for k, v in self.row_count.items():
            if v[0] > math.ceil(self.height / 2) or v[1] > math.ceil(self.height / 2):
                print("no", file=sys.stderr)
                return False
            
            if v[1] > math.ceil(self.height / 2):
                print("no", file=sys.stderr)
                return False
            
        # update grid
        self.grid[y][x] = play
        
        # check three in a row
        for i in self.grid:
            tracker = 0
            prev = None

            for j in i:
                if j == prev and j.isdigit():
                    tracker += 1
                else:
                    tracker = 0

                if tracker == 2:
                    print("no", file=sys.stderr)
                    self.grid[y][x] = "."
                    return False
                
                prev = j
        
        # check three in a col
        for col in range(len(self.grid[0])): 
            tracker = 0
            prev = None

            for row in range(len(self.grid)):
                if self.grid[row][col] == prev and self.grid[row][col].isdigit():
                    tracker += 1
                else:
                    tracker = 0

                if tracker == 2:
                    print("no", file=sys.stderr)
                    self.grid[y][x] = "."
                    return False
                
                prev = self.grid[row][col]

        # revert back
        self.grid[y][x] = "."
        print("yes", file=sys.stderr)

        return True
    
    def genmove(self, args):
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    def winner(self, args):
        raise NotImplementedError("This command is not yet implemented.")
        return True
    
    #======================================================================================
    # End of functions requiring implementation
    #======================================================================================

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()