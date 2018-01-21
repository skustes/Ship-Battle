from random import randint, choice
import time
from functions import *

# Game class
class Game(object):
    def __init__(self):
        self.turn = "p1"
        self.players = 1    # Set a default
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

    def play(self):
        # Setup the players
        self.how_many_players()
        p1 = Player( "Player 1" )
        if self.players == 2:
            p2 = Player( "Player 2" )
        else:
            p2 = CPUPlayer()

        # Clear the screen
        wipe()

        # Place the ships on the game board
        p1.place_ships( self.ships )
        time.sleep(2)
        p2.place_ships( self.ships )

    def how_many_players(self):
        valid_number = False
        while valid_number == False:
            try: 
                self.players = int( input("1 or 2 players? ") )
                if self.players in [1,2]:
                    valid_number = True
            except ValueError:
                print("Please enter a valid number")

class Board(object):
    def __init__(self, size):
        self.size = size
        # Create blank board
        self.board = [ [ "^" for i in range(0,self.size) ] for j in range(0,self.size) ]
        # Create a header of letters
        self.header = ["A","B","C","D","E","F","G","H","I","J"]
    
    """
    Grid functions to receive input, access, and check coordinates
    """
    def random_coordinate(self):
        col = num_to_chr( randint(1,self.size) )
        row = randint(1,self.size)
        return col + str(row)

    # Check that a ship can be placed at the coordinate given
    # If so, place the ship on the board
    def place_ship(self, coordinate, direction, length, code):
        placement_result = []
        # Split the column letter from the row number
        split = self.split_coordinate( coordinate )

        # First check that the coordinate was input in a valid format (A5, F8, B3, etc)
        if self.is_valid_format( split ):
            # Now check that it's on the board
            if self.is_on_board( split ):
                # Now check that the ship physically fits
                if self.does_ship_fit( split , direction , length ):
                    self.put_ship_on_board( split, direction , length , code.upper())
                    placement_result = [True,"Successfully placed!"]
                else:
                    placement_result = [False,"Part of your ship is off the board or hits another ship."]
            else:
                placement_result = [False,"That coordinate isn't on the board.  Try again."]
        else:
            placement_result = [False,"Invalid coordinate format"]

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
        row = coordinate[1] - 1

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
        row = coordinate[1] - 1

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
                if self.board[coordinate[0]][coordinate[1]] != "^":
                    return False

            # If we reach this point, return True because it's all good
            return True
    # Splits a coordinate into its components, ex: E10 -> ["E","10"]
    def split_coordinate(self, coordinate):
        return [coordinate[:1],coordinate[1:]]
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

# Player class
class Player(object):
    def __init__(self, default_name):
        self.player_board = Board(10)
        self.shot_board = Board(10)
        self.name = self.set_name( default_name )

    def set_name(self, default_name):
        valid_name = False
        while valid_name == False:
            new_name = input( default_name + ", what's your name? " )
            if new_name.isalnum():
                valid_name = True
        return "Admiral " + str( new_name )
    
    # Steps the player through placing each ship as defined in Game class
    def place_ships(self, ships):
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
                    print( "Pick a coordinate for your", ships[key]["name"], "(length:", ships[key]["length"], ")" )
                    coordinate = input( "Ex: A10, F4, etc: ").upper()

                    # Run a while loop to prevent progress until a valid direction input (v or h) is input
                    valid_direction = False
                    while valid_direction == False:
                        ship_direction = input( "Vertical or horizontal [v/h]: ").lower()
                        if ship_direction in ["v","h"]:
                            valid_direction = True

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
            self.auto_place( ships )

        self.print_own_board()

    # Passes the ships along to the player's board for auto-placement
    def auto_place(self, ships):
        self.player_board.auto_place( ships )

    """
    Attribute access methods
    """
    def get_name(self):
        return self.name
    def get_own_board(self):
        return self.player_board
    def get_shot_board(self):
        return self.shot_board
    def print_own_board(self):
        self.player_board.print_board()
    def print_shot_board(self):
        self.shot_board.print_board()

class CPUPlayer(Player):
    def __init__(self):
        self.player_board = Board(10)
        self.shot_board = Board(10)
        self.name = "CPU"

    def place_ships(self, ships):
        print("Placing CPU ships...")
        self.auto_place( ships )
        time.sleep(2)