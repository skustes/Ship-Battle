# Other classes the Game class needs to function
from random import randint, choice
import time
from functions import *

# Game class
class Game(object):
    def __init__(self):
        self.turn = "p1"
        self.players = 1    # Set a default
        self.difficulty = "h"   # Set difficulty to hard by default
        self.ships = {
            "carrier": {
                "name": "Aircraft Carrier",
                "length": 5,
                "code": "A"
                },
            "battleship": {
                "name": "Battleship",
                "length": 4,
                "code": "B"
                },
            "cruiser": {
                "name": "Cruiser",
                "length": 3,
                "code": "C"
                },
            "submarine": {
                "name": "Submarine",
                "length": 3,
                "code": "S"
                },
            "destroyer": {
                "name": "Destroyer",
                "length": 2,
                "code": "D"
                },
            }
        self.status = 0 # 0 if game in progress, 1 if p1 wins, 2 if p2 wins

    def play(self):
        # Setup the players
        self.how_many_players()
        p1 = Player( "Player 1" )
        if self.players == 2:
            p2 = Player( "Player 2" )
        else:
            self.set_difficulty_level()
            p2 = CPUPlayer( self.difficulty )

        # Clear the screen
        # wipe()

        # Place the ships on the game board
        p1.place_ships( self.ships )
        time.sleep(1)
        p2.place_ships( self.ships )

        while self.status == 0:
            wipe()

            # Alternate turns
            if self.turn == "p1":
                shot = p1.bombs_away()
                shot_result = p2.check_shot( shot )
                p1.update_shot_board( shot , shot_result )
            else:
                shot = p2.bombs_away()
                shot_result = p1.check_shot( shot )
                p2.update_shot_board( shot , shot_result )
            

            # Output the results of the shot to the screen
            if shot_result[0] == False:
                print("Missed!")
            else:
                print("Hit" if shot_result[2] > 0 else "Sank",
                      p2.get_name() if self.turn == "p1" else p1.get_name() + "'s",
                      self.get_ship_by_code(shot_result[1]))
            

            if p1.get_ships_remaining() == 0:
                self.status = 2
                print(p2.get_name(),"wins!")
            elif p2.get_ships_remaining() == 0:
                self.status = 1
                print(p1.get_name(),"wins!")
            else:
                print(p2.get_name() if self.turn == "p1" else p1.get_name(),
                      "has",
                      p2.get_ships_remaining() if self.turn == "p1" else p1.get_ships_remaining(),
                      "ships still in the fight!")

            self.turn = "p2" if self.turn == "p1" else "p1"
            press_to_continue = input("Press a key to continue.")
    
    # Set the number of players
    def how_many_players(self):
        valid_number = False
        while valid_number == False:
            try: 
                self.players = int( input("1 or 2 players? ") )
                if self.players in [1,2]:
                    valid_number = True
            except ValueError:
                print("Please enter a valid number")

    # Set the difficulty level
    def set_difficulty_level(self):
        valid_entries = ["e","m","h"]
        valid_difficulty = False
        while valid_difficulty == False:
            self.difficulty = input( "Easy, Medium, or Hard [e/m/h]: ")
            if self.difficulty in valid_entries:
                valid_difficulty = True

    # Returns the name of a ship given the board code for a ship
    def get_ship_by_code(self, code):
        for key in self.ships:
            if self.ships[key]["code"] == code:
                return self.ships[key]["name"]

# Board class
# Manages grid coordinates and layout
class Board(object):
    def __init__(self, size):
        self.size = size
        self.default = "~"
        # Create blank board
        self.board = [ [ self.default for i in range(0,self.size) ] for j in range(0,self.size) ]
        # Create a header of letters
        self.header = ["A","B","C","D","E","F","G","H","I","J"]
    
    """
    Grid functions to receive input, access, and check coordinates
    """
    def random_coordinate(self):
        col = num_to_chr( randint(1,self.size) )
        row = randint(1,self.size)
        return col + str(row)

    # Check that a ship can be placed at the coordinate given without hitting another ship
    # Coordinate format and validity was checked when requested in Player class, function ask_coordinate()
    # If so, place the ship on the board
    def place_ship(self, coordinate, direction, length, code):
        placement_result = []
        # Split the column letter from the row number
        split = self.split_coordinate( coordinate )

        # Check that the ship physically fits without going off the board or hitting another ship
        if self.does_ship_fit( split , direction , length ):
            self.put_ship_on_board( split, direction , length , code.upper())
            placement_result = [True,"Successfully placed!"]
        else:
            placement_result = [False,"Part of your ship is off the board or hits another ship."]

        return placement_result

    # Automatically places the ships on the board using a random coordinate generator
    def auto_place(self, ships):
        for key in ships:
            # Run a while loop to prevent progress until the current ship is validly placed
            ship_placed = False
            while ship_placed == False:
                # Get a random point on the grid and a random direction
                coordinate = self.random_coordinate()
                ship_direction = choice( ["v","h"] )

                # Try placing the ship on the board
                placement_result = self.place_ship( coordinate , ship_direction , ships[key]["length"] , ships[key]["code"] )
                # If the ship was placed successfully, wipe the screen and move on to the next one
                # Otherwise, output the error
                if placement_result[0] == True:
                    ship_placed = True

    # Places the ship on the board, replacing the default character with the code for the ship for each spot the ship covers
    # Expects coordinate parameter to be a list with two components (run self.split_coordinate on input)
    # Always returns True
    def put_ship_on_board(self, coordinate, direction, length, code):
        col = chr_to_num( coordinate[0] ) - 1
        row = int( coordinate[1] ) - 1

        for i in range(0,length):
            if direction == "v":
                self.board[row+i][col] = code
            else:
                self.board[row][col+i] = code
        
        return True

    # Checks that the coordinate is in a valid format such as A5, F8, B10
    # Expects coordinate parameter to be a list with two components (run self.split_coordinate on input)

    def is_valid_format(self, coordinate):
        # Ensure the second part of the coordinate is an integer
        try:
            coordinate[1] = int( coordinate[1] )
        except ValueError:
            return False

        # Ensure the first part is alphabetic
        if coordinate[0].isalpha() == False:
            return False
        else:
            return True
    # Checks that the coordinate is on the board
    # Expects coordinate parameter to be a list with two components (run self.split_coordinate on input)

    def is_on_board(self, coordinate):
        col = chr_to_num( coordinate[0] )
        row = int( coordinate[1] )
        if  col not in range(1,self.size+1) or row not in range(1,self.size+1):
            return False
        else:
            return True
    # Ensures that the ship will fit without falling off the board or hitting another ship
    # Expects coordinate parameter to be a list with two components (run self.split_coordinate on input)

    # Returns True or False
    def does_ship_fit(self, coordinate, direction, length):
        col = chr_to_num( coordinate[0] ) - 1
        row = int( coordinate[1] ) - 1

        # If the ship is being placed vertically and row + length falls off the board, return False
        # If the ship is being placed horizontally and col + length falls off the board, return False
        if ( direction == "v" and ( row + length ) > self.size ) or ( direction == "h" and ( col + length ) > self.size ):
            return False
        # Finally check that no other ships are in the way
        else:
            # Determine which coordinates the ship will fall on for its entire length
            ship_coordinates = [[row, col]]
            for i in range(1,length):
                if direction == "v":
                    ship_coordinates.append([row+i,col])
                else:
                    ship_coordinates.append([row,col+i])

            # Check if those coordinates are still the default character '^' (i.e., don't have a ship placed there)
            for coordinate in ship_coordinates:
                if self.board[coordinate[0]][coordinate[1]] != self.default:
                    return False

            # If we reach this point, return True because it's all good
            return True

    # Splits a coordinate into its components, ex: E10 -> ["E","10"]
    def split_coordinate(self, coordinate):
        col = coordinate[:1] # First character
        row = coordinate[1:] # Remaining characters
        return [col,row]

    # Determines if a ship is at a given coordinate
    # Returns a 2 item list, 1st item is True or False based on if the shot was a hit or miss, 2nd item is the ship code if shot was a hit
    def check_coordinate(self, coordinate):
        split = self.split_coordinate( coordinate )
        col = chr_to_num( split[0] ) - 1
        row = int( split[1] ) - 1
        result = [True if self.board[row][col] != self.default else False,self.board[row][col]]

        return result

    # Updates a passed coordinate to a passed value and returns True
    def update_coordinate(self, coordinate, value):
        split = self.split_coordinate( coordinate )
        col = chr_to_num( split[0] ) - 1
        row = int( split[1] ) - 1
        self.board[row][col] = value
        return True

    # Determines if a shot has already been placed at the passed coordinate
    def check_duplicate_shot(self, coordinate):
        split = self.split_coordinate( coordinate )
        col = chr_to_num( split[0] ) - 1
        row = int( split[1] ) - 1
        return False if self.board[row][col] == self.default else True

    """
    Attribute access methods
    """
    def print_board(self):
        print( "  ", " ".join(self.header) )
        count = 1
        for row in self.board:
            count_output = str(count) if count >= 10 else str(count) + " "
            print( count_output, " ".join(row) )
            count += 1

# Ship class
# Deals with all things related to location and alive/dead status of ships
class Ship(object):
    pass

# Player class
# Interface between Game, Board, and Ship classes
class Player(object):
    def __init__(self, default_name):
        self.player_board = Board(10)
        self.shot_board = Board(10)
        self.name = self.set_name( default_name )
        self.ships = {}
        self.shot_results = { "shots": [], "results": [] }

    def set_name(self, default_name):
        valid_name = False
        while valid_name == False:
            new_name = input( default_name + ", what's your name? " )
            if new_name.isalnum():
                valid_name = True
        return "Admiral " + str( new_name )
    
    # Steps the player through placing each ship as defined in Game class
    def place_ships(self, ships):
        self.set_ship_dictionary( ships )

        print( self.name + ", time to place your ships.\n" )
        # Run a while loop to prevent progress until a valid y or n input is given
        valid_auto = False
        while valid_auto == False:
            auto_place_input = input( "Do you want me to place your ships automatically? (y/n) " ).lower()
            if auto_place_input in ["y","n"]:
                valid_auto = True

        if auto_place_input == "n":
            # Loop through the ships, allowing the player to place each one
            # Checks are run after each entry to ensure the coordinates input are in a valid format and the ship can be physically placed
            for key in ships:
                print( "Here is your board: ")
                self.print_own_board()
                placement_result = []

                # Run a while loop to prevent progress until the current ship is validly placed
                ship_placed = False
                while ship_placed == False:
                    message = "Pick a coordinate for your " + ships[key]["name"] + " (length: " + str(ships[key]["length"]) + ")"
                    coordinate = self.ask_coordinate( message )
                    ship_direction = self.ask_direction()

                    # Try placing the ship on the board
                    placement_result = self.player_board.place_ship( coordinate , ship_direction , ships[key]["length"] , ships[key]["code"] )
                    # If the ship was placed successfully, wipe the screen and move on to the next one
                    # Otherwise, output the error
                    if placement_result[0] == True:
                        wipe()
                        ship_placed = True
                    else:
                        print( placement_result[1] )
        else:
            self.player_board.auto_place( ships )

        self.print_own_board()

    # Get input of a coordinate
    def ask_coordinate(self, message):
        print(message)
        valid_coordinate = False
        while valid_coordinate == False:
            coordinate = input( "Ex: A10, F4, etc: ").upper()
            split = self.player_board.split_coordinate( coordinate )

            if not self.player_board.is_valid_format( split ):
                print("Invalid coordinate format. Try again.")
            elif not self.player_board.is_on_board( split ):
                print("That coordinate isn't on the board. Try again.")
            else:
                valid_coordinate = True
        return coordinate

    # Get direction input
    def ask_direction(self):
        # Run a while loop to prevent progress until a valid direction input (v or h) is input
        valid_direction = False
        while valid_direction == False:
            ship_direction = input( "Vertical or horizontal [v/h]: ").lower()
            if ship_direction in ["v","h"]:
                valid_direction = True
        return ship_direction

    # Shoot at the other player
    def bombs_away(self):
        print("Here is what you know about your opponent's ships:")
        self.print_shot_board()

        # Print information about the last shot and the last hit
        if len( self.shot_results["shots"] ) > 0:
            # Find the last shot that was a hit
            # all_hits = [i for i, x in enumerate( self.shot_results["results"] ) if x == 'h']
            print("Your last shot was a","miss" if self.shot_results["results"][-1] == "m" else "hit","at",self.shot_results["shots"][-1])

        message = self.name + ", where do you want to shoot?"
        is_duplicate_shot = True
        while is_duplicate_shot == True:
            shot_coordinate = self.ask_coordinate( message )
            if self.shot_board.check_duplicate_shot( shot_coordinate ):
                message = "You already shot there, Admiral.  Check your shot board before you get us all killed!"
            else:
                is_duplicate_shot = False
        return shot_coordinate

    # Create a dictionary of ships for keeping track of sunk ships
    def set_ship_dictionary(self, ships):
        for key in ships:
            ship_code = ships[key]["code"]
            self.ships[ship_code] = ships[key]["length"]

    # Checks whether a shot was a hit or miss
    # Returns 3 item list:
    #   1st element is True or False
    #   2nd element is the code of the ship type that was hit
    #   3rd element is the number of spots remaining on the ship or -1 if hit was a miss
    def check_shot(self, coordinate):
        shot_result = self.player_board.check_coordinate( coordinate )
        # If the shot was a hit, reduce the number of spots left on that ship
        if shot_result[0] == True:
            self.ships[shot_result[1]] -= 1
            shot_result.append(self.ships[shot_result[1]])
        else:
            shot_result.append(-1)
        return shot_result

    # Updates the shot board and shot_results lists
    # Expect grid coordinate shot at and shot_result 2 item list returned from opponent's check_shot method
    def update_shot_board(self, shot, shot_result):
        self.shot_results["shots"].append(shot)
        self.shot_results["results"].append("m" if shot_result[0] == False else "h")
        self.shot_board.update_coordinate( shot , "O" if shot_result[0] == False else "X" )
        
    """
    Attribute access methods
    """
    def get_name(self):
        return self.name
    def get_own_board(self):
        return self.player_board
    def get_shot_board(self):
        return self.shot_board
    # Returns an integer indicating how many of the player's ships are still floating
    def get_ships_remaining(self):
        ships_afloat = 0
        for key in self.ships:
            if self.ships[key] > 0:
                ships_afloat += 1
        return ships_afloat
    def print_own_board(self):
        self.player_board.print_board()
    def print_shot_board(self):
        self.shot_board.print_board()

# CPUPlayer class
# Extends Player class with functionality necessary for CPU play
class CPUPlayer(Player):
    def __init__(self, difficulty):
        self.player_board = Board(10)
        self.shot_board = Board(10)
        self.name = "CPU"
        self.difficulty = difficulty
        self.ships = {}
        self.shot_results = { "shots": [], "results": [] }

        # Determine which strategy will be used
        self.strategy = self.set_strategy()

    # Determine which strategy is being used
    def set_strategy(self):
        easy = {
            "first_shot": "a1",
            "shot_increment": 2
            }

        print("setting strategy")
        pass
        # Different placement and shot strategies
        # https://www.wikihow.com/Win-at-Battleship
        # 

    # Use auto-place to put down the CPU ships
    def place_ships(self, ships):
        self.set_ship_dictionary( ships )
        print("Placing CPU ships...")
        self.player_board.auto_place( ships )
        time.sleep(1)

    # Ensures shot is not a duplicate, then returns the coordinate
    def bombs_away(self):
        duplicate_shot = True
        while duplicate_shot == True:
            shot_coordinate = self.shot_board.random_coordinate()
            duplicate_shot = self.shot_board.check_duplicate_shot( shot_coordinate )
        return shot_coordinate