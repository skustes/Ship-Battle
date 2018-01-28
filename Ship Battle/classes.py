from random import randint, choice
import time
from functions import *

# Game class
# Gets the game setup and handles game play
class Game(object):
    def __init__(self):
        self.turn = "p1"
        self.players = 1        # Set a default
        self.difficulty = "ve"   # Set difficulty to hard by default
        self.status = 0         # 0 if game in progress, 1 if p1 wins, 2 if p2 wins
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
        # Setup the board and the players
        board = Board( 10 )
        self.how_many_players()
        p1 = Player( "Player 1" )
        
        if self.players == 2:
            p2 = Player( "Player 2" )
        else:
            self.set_difficulty_level()
            p2 = CPUPlayer( self.difficulty )

        # Clear the screen
        wipe()

        # Place the ships on the game board
        p1.place_ships( self.ships , board )
        time.sleep(1)
        p2.place_ships( self.ships , board )
        
        # Repeat until someone wins
        while self.status == 0:
            wipe()

            # Alternate turns
            if self.turn == "p1":
                shot = p1.bombs_away( board )
                shot_result = p2.check_shot( shot )
                p1.record_shot_result( shot , shot_result )
            else:
                shot = p2.bombs_away( board )
                shot_result = p1.check_shot( shot )
                p2.record_shot_result( shot , shot_result )
            

            # Output the results of the shot to the screen
            if shot_result[0] == False:
                print("Missed!")
            else:
                print("Hit" if shot_result[2] == True else "Sank",
                      p2.get_name( True ) if self.turn == "p1" else p1.get_name( True ),
                      self.get_ship_by_code( shot_result[1]) )
            

            if p1.get_ships_remaining() == 0:
                self.status = 2
                print(p2.get_name(),"wins!")
            elif p2.get_ships_remaining() == 0:
                self.status = 1
                print(p1.get_name(),"wins!")
            else:
                ships_remaining = p2.get_ships_remaining() if self.turn == "p1" else p1.get_ships_remaining()

                print(p2.get_name() if self.turn == "p1" else p1.get_name(),
                      "has",
                      ships_remaining,
                      "ships" if ships_remaining > 1 else "ship",
                      "still in the fight!")

            self.turn = "p2" if self.turn == "p1" else "p1"
            press_to_continue = input("Press enter to continue.")
    
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
        valid_entries = [ "ve" , "e" ]
        valid_difficulty = False
        while valid_difficulty == False:
            self.difficulty = input( "Very Easy or Easy? [ve/e] ")
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
        self.header = [num_to_chr(i).upper() for i in range(1,self.size+1)]

    # Returns a random coordinate on the board
    def random_coordinate(self):
        col = num_to_chr( randint(1,self.size) )
        row = randint(1,self.size)
        return col + str(row)

    # Checks if a coordinate input is valid format (Ex: a1, b5, j8)
    # Returns True or False
    def is_valid_format(self, coordinate):
        # Split the first character (presumably alphabetic) from the remaining characters (presumably integer)
        split = [ coordinate[:1] , coordinate[1:] ]

        # Ensure the second part of the coordinate is an integer
        try:
            split[1] = int( split[1] )
        except ValueError:
            return False

        # Ensure the first part is alphabetic
        if split[0].isalpha() == False:
            return False
        else:
            return True

    # Checks that the coordinate is on the board
    # Returns True or False
    def is_on_board(self, coordinate):
        split = self.split_coordinate( coordinate )
        row = split[0]
        col = split[1]
        if  row not in range(0,self.size) or col not in range(0,self.size):
            return False
        else:
            return True

    # Removes leading zeroes from the numeric portion
    # Returns the coordinate without leading zeroes, ex: A09 -> A9
    def strip_zeroes(self, coordinate):
        return self.join_coordinate( self.split_coordinate( coordinate) )

    # Ensure that ship fits on the board given the coordinate, length, and direction of placement
    # Returns True or False
    def does_ship_fit(self, coordinate, direction, length):
        split = self.split_coordinate( coordinate )
        row = split[0]
        col = split[1]

        # If the ship is being placed vertically and row + length falls off the board, return False
        # If the ship is being placed horizontally and col + length falls off the board, return False
        if ( direction == "v" and ( row + length ) > self.size ) or ( direction == "h" and ( col + length ) > self.size ):
            return False
        else:
            return True

    # Calculate the grid coordinates that a ship will occupy given the coordinate, length, and direction of placement
    # Assumes that coordinate has been checked by is_valid_format, is_on_board, and does_ship_fit prior to being called
    # Returns a list of grid coordinates
    def determine_ship_coordinates(self, coordinate, direction, length):
        ship_coordinates = [coordinate]
        split = self.split_coordinate( coordinate )
        row = split[0]
        col = split[1]
        for i in range(1,length):
            if direction == "v":
                next_coordinate = [ row+i , col ]
                ship_coordinates.append( self.join_coordinate( next_coordinate ) )
            else:
                next_coordinate = [ row , col+i ]
                ship_coordinates.append( self.join_coordinate( next_coordinate ) )
        return ship_coordinates

    # Splits a coordinate into its grid components
    # Returns [row,column]. Ex: a2 -> [1,0], j5 -> [4,9]
    def split_coordinate(self, coordinate):
        col = coordinate[:1]                    # First character
        row = coordinate[1:].lstrip("0")        # Remaining characters with leading zeroes stripped
        return [ int(row)-1 , chr_to_num(col) - 1 ]

    # Returns a coordinate string from its row and column components ex: [0,0] -> A1, [5,5] -> F6
    def join_coordinate(self, coordinate):
        return num_to_chr( coordinate[1]+1 ) + str( coordinate[0]+1 )

    # Prints the board with an optional overlay
    # Overlay is a list of tuples representing a coordinate and the character to overlay, ex: [ [A2,"X"] , [B5,"O"] ]
    def print_board(self, overlay = []):
        print( "  ", " ".join(self.header) )
        count = 1
        
        # If no overlay was passed, output the default board
        if not overlay:
            for row in self.board:
                count_output = str(count) if count >= 10 else str(count) + " "
                print( count_output, " ".join(row) )
                count += 1
        # Otherwise, output the board with the correct characters at the correct coordinates
        else:
            overlay_coordinates = []
            for key in overlay:
                overlay_coordinates.append( self.split_coordinate(key) )

            for row in range(0,len(self.board)):
                row_output = []

                for col in range(0,len(self.board[row])):
                    # If this coordinate is in the list of coordinates to overlay, append the overlay value
                    if [row,col] in overlay_coordinates:
                        row_output.append( overlay[self.join_coordinate([row,col])] )
                    # Otherwise, append the character at this spot on the default board
                    else:
                        row_output.append( self.board[row][col] )

                count_output = str(count) if count >= 10 else str(count) + " "
                print( count_output, " ".join(row_output) )
                count += 1

# Ship class
# Deals with all things related to location and alive/dead status of ships
class Ship(object):
    def __init__(self, name, length, code, coordinates):
        self.name = name
        self.length = length
        self.code = code
        self.coordinates = coordinates
        self.hits = [ "O" for i in range(1,length+1) ]

    # Records a hit at the given coordinate
    def record_hit_at(self, coordinate):
        self.hits[ self.coordinates.index( coordinate ) ] = "X"

    # Attribute access methods
    def get_name(self):
        return self.name
    def get_length(self):
        return self.length
    def get_code(self):
        return self.code
    def get_coordinates(self):
        return self.coordinates
    def is_alive(self):
        return True if self.hits.count("O") > 0 else False

# Player class
# Interface between Game, Board, and Ship classes
class Player(object):
    def __init__(self, default_name):
        self.name = self.set_name( default_name )
        self.ships = {}
        self.shot_results = { "shots": [], "results": [] }

    # Lets the player set their name and adds Admiral to it because I'm funny
    def set_name(self, default_name):
        valid_name = False
        while valid_name == False:
            new_name = input( default_name + ", what's your name? " )
            if all( x.isalpha() or x.isspace() for x in new_name ):
                valid_name = True
        return "Admiral " + str( new_name )

    # Creates a Ship object for each ship passed in from the Game object
    def create_ships(self, ships):
        ship_objects = {}
        for ship in ships:
            current_ship = ships[ship]
            ship_objects[ship] = Ship( current_ship["name"] , current_ship["length"] , current_ship["code"] )
        return ship_objects
    
    # Steps the player through placing each ship
    # Validates placement of ship, then creates Ship object and adds it to self.ships
    # No return value
    def place_ships(self, ships, board):
        print( self.name + ", time to place your ships.\n" )
        # Run a while loop to prevent progress until a valid y or n input is given
        valid_auto = False
        while valid_auto == False:
            auto_place_input = input( "Do you want me to place your ships automatically? (y/n) " ).lower()
            if auto_place_input in ["y","n"]:
                valid_auto = True

        if auto_place_input == "n":
            # Loop through the ships, allowing the player to place each one
            # Check to ensure coordinate input is valid format (Ex: a1, b5, j8) and
            # that ship won't run off the board or overlap another ship
            for key in ships:
                current_ship = ships[key]
                placement_result = []
                ship_coordinates = []

                print( "Here is your board: ")
                self.print_own_board( board )

                # Run a while loop to prevent progress until the current ship is validly placed
                ship_placed = False
                while ship_placed == False:
                    message = "Pick a coordinate for your " + current_ship["name"] + " (length: " + str( current_ship["length"] ) + ")"
                    coordinate = self.ask_coordinate( message , board )
                    ship_direction = self.ask_direction()

                    # Ensure the ship fits on the board
                    if not board.does_ship_fit( coordinate , ship_direction , current_ship["length"] ):
                        placement_result = [ False , "Sorry Admiral, part of your ship is off the board."]
                    else:
                        ship_coordinates = board.determine_ship_coordinates( coordinate, ship_direction , current_ship["length"] )
                        # Ensure the ship doesn't hit any ships already on the board
                        if set(ship_coordinates).intersection(self.all_ship_coordinates()):
                            placement_result = [ False , "Sorry Admiral, two of your ships will collide if you do that."]
                        else:
                            placement_result = [ True , "" ]
                            self.ships[key] = Ship( current_ship["name"] , current_ship["length"] , current_ship["code"] , ship_coordinates )

                    # If the ship was placed successfully, wipe the screen and move on to the next one
                    # Otherwise, output the error
                    if placement_result[0] == True:
                        wipe()
                        ship_placed = True
                    else:
                        print( placement_result[1] )
        else:
            self.auto_place( ships , board )

        self.print_own_board( board )

    # Get input of a coordinate
    # Ensure that it is in a valid format and is on the board
    # Returns a valid board coordinate
    def ask_coordinate(self, message, board):
        print(message)
        valid_coordinate = False
        while valid_coordinate == False:
            coordinate = input( "Ex: A10, F4, etc: ").lower()

            if not board.is_valid_format( coordinate ):
                print("Sorry Admiral, that coordinate doesn't make any sense.")
            elif not board.is_on_board( coordinate ):
                print("Sorry Admiral, that coordinate isn't even on the board.")
            else:
                valid_coordinate = True
        return board.strip_zeroes( coordinate )

    # Get direction input
    # Ensure that input is (v)ertical or (h)orizontal
    # Returns v = vertical or h = horizontal
    def ask_direction(self):
        # Run a while loop to prevent progress until a valid direction input (v or h) is input
        valid_direction = False
        while valid_direction == False:
            ship_direction = input( "Vertical or horizontal [v/h]: ").lower()
            if ship_direction in ["v","h"]:
                valid_direction = True
        return ship_direction

    # Automatically places the ships on the board using a random coordinate generator
    def auto_place(self, ships , board):
        for key in ships:
            current_ship = ships[key]
            ship_coordinates = []

            # Run a while loop to prevent progress until the current ship is validly placed
            ship_placed = False
            while ship_placed == False:
                # Get a random point on the grid and a random direction
                coordinate = board.random_coordinate()
                ship_direction = choice( ["v","h"] )

                # Ensure the ship fits on the board
                if board.does_ship_fit( coordinate , ship_direction , current_ship["length"] ):
                    ship_coordinates = board.determine_ship_coordinates( coordinate, ship_direction , current_ship["length"] )
                    # Ensure the ship doesn't hit any ships already on the board
                    if not set(ship_coordinates).intersection(self.all_ship_coordinates()):
                        ship_placed = True
                        self.ships[key] = Ship( current_ship["name"] , current_ship["length"] , current_ship["code"] , ship_coordinates )

    # Shoot at the other player
    # Returns the coordinate of the shot, validated to ensure it is properly formatted and isn't a duplicate shot
    def bombs_away(self, board):
        print("Here is what you know about your opponent's ships:")
        self.print_shot_board( board )

        # Print information about the last shot and the last hit
        if len( self.shot_results["shots"] ) > 0:
            # Find the last shot that was a hit
            # all_hits = [i for i, x in enumerate( self.shot_results["results"] ) if x == 'h']
            print("Your last shot was a","miss" if self.shot_results["results"][-1] == "m" else "hit","at",self.shot_results["shots"][-1])

        message = self.name + ", where do you want to shoot?"
        is_duplicate_shot = True
        while is_duplicate_shot == True:
            shot_coordinate = self.ask_coordinate( message , board )

            if self.is_duplicate_shot( shot_coordinate ):
                message = "You already shot there, Admiral.  Check your shot board before you get us all killed!"
            else:
                is_duplicate_shot = False
        return shot_coordinate

    # Determines if a shot has already been placed at the passed coordinate
    # Returns True or False
    def is_duplicate_shot(self, coordinate):
        return True if coordinate in self.shot_results["shots"] else False

    # Checks whether a shot was a hit or miss
    # Returns 3 item list:
    #   1st element: True (hit) or False (miss)
    #   2nd element: The letter code of the ship that was hit
    #   3rd element: Is ship alive? True (still in the game), False (sunk)
    def check_shot(self, coordinate):
        shot_result = [False] # Default

        for key in self.ships:
            if coordinate in self.ships[key].get_coordinates():
                # Update the ship that was hit
                self.ships[key].record_hit_at( coordinate )
                # Create the return value
                shot_result = [True,self.ships[key].get_code(),self.ships[key].is_alive()]

        return shot_result

    # Updates the shot board and shot_results lists
    # Expects grid coordinate shot at and shot_result list returned from opponent's check_shot method
    def record_shot_result(self, shot, shot_result):
        self.shot_results["shots"].append(shot)
        self.shot_results["results"].append("m" if shot_result[0] == False else "h")

    # Attribute access methods
    def get_name(self, possessive = False):
        if not possessive:
            return self.name
        else:
            return self.name + "'s"
    # Returns a list with the coordinates of all of the player's ships
    def all_ship_coordinates(self):
        return [ coordinate for key in self.ships for coordinate in self.ships[key].get_coordinates() ]
    # Prints the board with the player's ships overlaid on the proper coordinates
    def print_own_board(self, board):
        overlay = {}
        for key in self.ships:
            ship_code = self.ships[key].get_code()
            for coordinate in self.ships[key].get_coordinates():
                overlay[coordinate] = ship_code
        board.print_board( overlay )
    # Prints the board with the results of the player's shots overlaid on the proper coordinates
    def print_shot_board(self, board):
        overlay = {}
        for index in range(0,len(self.shot_results["shots"])):
            overlay[self.shot_results["shots"][index]] = self.shot_results["results"][index]
        board.print_board( overlay )

    # Returns an integer indicating how many of the player's ships are still floating
    def get_ships_remaining(self):
        ships_afloat = 0
        for key in self.ships:
            if self.ships[key].is_alive():
                ships_afloat += 1
        return ships_afloat

# CPUPlayer class
# Extends Player class with functionality necessary for CPU play
class CPUPlayer(Player):
    def __init__(self, difficulty):
        self.name = "CPU"
        self.ships = {}
        self.shot_results = { "shots": [] , "results": [] }

        # CPU Player extended attributes
        self.difficulty = difficulty
        self.kill_mode = {
            "status": "off"
            }

    # Use auto-place to put down the CPU ships
    def place_ships(self, ships, board):
        print("Placing CPU ships...")
        self.auto_place( ships , board )
        time.sleep(1)

    # Ensures shot is not a duplicate, then returns the coordinate
    def bombs_away(self, board):
        if self.difficulty == "ve":
            shot_coordinate = self.shot_very_easy( board )
        elif self.difficulty == "e":
            shot_coordinate = self.shot_easy( board )
        elif self.difficulty == "m":
            shot_coordinate = self.shot_medium( board )
        elif self.difficulty == "h":
            shot_coordinate = self.shot_hard( board )
        elif self.difficulty == "vh":
            shot_coordinate = self.shot_very_hard( board )
        return shot_coordinate
        
    # Returns the shot for Very Easy difficulty
    # Random shots with no Kill mode when a ship is hit
    # Like playing against someone that doesn't understand the objective of the game
    def shot_very_easy(self, board):
        duplicate_shot = True
        while duplicate_shot == True:
            shot_coordinate = board.random_coordinate()
            duplicate_shot = self.is_duplicate_shot( shot_coordinate )
        return shot_coordinate

    # Returns the shot for Easy difficulty
    # Random shots with Kill mode when a ship is hit
    # Like playing against a 7-year old that understands the objective, but not the basics of strategy
    def shot_easy(self, board):
        pass

    # Returns the shot for Medium difficulty
    # Shoots only at every other square since the shortest ship is 2 squares long, uses Kill mode when a ship is hit
    # Like playing against someone with a basic strategy
    def shot_medium(self, board):
        pass

    # Returns the shot for Hard difficulty
    # Bases next shot on shortest remaining opponent ship, uses Kill mode when a ship is hit
    # Like playing against someone with a solid strategy based on knowledge of the opponent's ships
    def shot_hard(self, board):
        pass

    # Returns the shot for Very Hard difficulty
    # Probability model
    def shot_very_hard(self, board):
        pass