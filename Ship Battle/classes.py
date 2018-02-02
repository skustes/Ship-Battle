from random import randint, choice, shuffle
import time
from functions import *

# Game class
# Sets up the game and handles game play
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
                p1.record_shot_result( shot , shot_result , board )
            else:
                shot = p2.bombs_away( board )
                shot_result = p1.check_shot( shot )
                p2.record_shot_result( shot , shot_result , board )
                # If P2 is CPU, output some info about the shot
                if p2.is_cpu():
                    print("Here is your board with",p2.get_name(True),"shots:")
                    p2.print_opponent_board( board , p1.get_ships() )
                    print(p2.get_name(),"shoots at:",shot)

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
        row = coordinate[1:].lstrip("0") if len( coordinate[1:] ) > 1 else coordinate[1:]       # Remaining characters with leading zeroes stripped
        return [ int(row)-1 , chr_to_num(col) - 1 ]

    # Returns a coordinate string from its row and column components ex: [0,0] -> A1, [5,5] -> F6
    def join_coordinate(self, coordinate):
        return num_to_chr( coordinate[1]+1 ) + str( coordinate[0]+1 )

    # Returns the points to the left/above coordinate_1 and to the right/below coordinate_2
    # Checks the points for validity and removes invalid points
    # Returns False if they don't share a row or column
    def end_points(self, coordinate_1, coordinate_2):
        split_1 = self.split_coordinate( coordinate_1 )
        split_2 = self.split_coordinate( coordinate_2 )
        return_coordinates = []

        # If the coordinates share a row, return the points to the left and right
        if split_1[0] == split_2[0]:
            # Determine which is left and which is right
            if split_1[1] <= split_2[1]:
                one_left = split_1
                one_right = split_2
            else:
                one_left = split_2
                one_right = split_1

            # Move one to the left and append the point if it's valid
            one_left = self.join_coordinate( [ one_left[0] , one_left[1] - 1 ] )
            if self.is_valid_format( one_left ) and self.is_on_board( one_left ):
                return_coordinates.append( one_left )
            # Move one to the right and append the point if it's valid
            one_right = self.join_coordinate( [ one_right[0] , one_right[1] + 1 ] )
            if self.is_valid_format( one_right ) and self.is_on_board( one_right ):
                return_coordinates.append( one_right )
        # If the coordinates share a column, return the points above and below
        elif split_1[1] == split_2[1]:
            # Determine which is more towards the top of the board
            if split_1[0] <= split_2[0]:
                one_above = split_1
                one_below = split_2
            else:
                one_above = split_2
                one_below = split_1

            one_above = self.join_coordinate( [ one_above[0] - 1 , one_above[1] ] )
            if self.is_valid_format( one_above ) and self.is_on_board( one_above ):
                return_coordinates.append( one_above )
            one_below = self.join_coordinate( [ one_below[0] + 1 , one_below[1] ] )
            if self.is_valid_format( one_below ) and self.is_on_board( one_below ):
                return_coordinates.append( one_below )
        # Otherwise, they aren't on either a column or row
        else:
            return False

        return return_coordinates

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
        self.cpu = "n"

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
            print("Your last shot was a","miss" if self.shot_results["results"][-1] == "O" else "hit","at",self.shot_results["shots"][-1])

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

    # Updates the shot_results lists
    # Expects grid coordinate shot at and shot_result list returned from opponent's check_shot method
    def record_shot_result(self, shot, shot_result, board):
        self.shot_results["shots"].append(shot)
        self.shot_results["results"].append("O" if shot_result[0] == False else "X")

    # Attribute access methods
    def get_name(self, possessive = False):
        if not possessive:
            return self.name
        else:
            return self.name + "'s"
    # Returns a list with the coordinates of all of the player's ships
    def all_ship_coordinates(self):
        return [ coordinate for key in self.ships for coordinate in self.ships[key].get_coordinates() ]
    # Returns the Ship objects for the player
    def get_ships(self):
        return self.ships
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
    # Returns True if is CPU player or False if is human player
    def is_cpu(self):
        return True if self.cpu == "y" else False
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
        self.cpu = "y"

        # CPU Player extended attributes
        self.difficulty = difficulty
        self.kill_mode = {
            "status": "off",
            "target_ship": "",
            "first_hit": "",
            "ship_coordinates": [],
            "locked": "off",
            "lock_direction": "",
            "optimized": "n",
            "targets": [],
            "other_ships_hit": []
            }

    # Use auto-place to put down the CPU ships
    def place_ships(self, ships, board):
        print("Placing CPU ships...")
        self.auto_place( ships , board )
        time.sleep(1)

    # Updates the shot_results lists and activates/deactivates kill mode
    # Expects grid coordinate shot at and shot_result list returned from opponent's check_shot method
    def record_shot_result(self, shot, shot_result, board):
        self.shot_results["shots"].append( shot )
        self.shot_results["results"].append( "O" if shot_result[0] == False else "X" )

        # First hit - Record hit in first_hit and ship_coordinates, engage kill mode
        # Second hit - Lock direction, update ship_coordinates, update "targets" based on direction
        # Additional hits - Update ship_coordinates and targets
        # Sunk ship - Disengage kill mode

        # If the target ship was sunk...
        if shot_result[0] == True and shot_result[2] == False:
            self.kill_mode_disengage()

            # If any other ships were hit, reactivate kill mode to target the next ship
            if len( self.kill_mode["other_ships_hit"] ) > 0:
                next_ship = self.kill_mode["other_ships_hit"].pop(0)
                self.kill_mode_engage( board, next_ship[1] , next_ship[0] , "n" if self.difficulty == "e" else "y" )
        # If the shot was the first hit on a ship, engage kill mode
        elif shot_result[0] == True and not self.kill_mode_active():
            self.kill_mode_engage( board, shot , shot_result[1] , "n" if self.difficulty == "e" else "y" )
        # If the shot was the a hit on the same ship...
        elif shot_result[0] == True and self.kill_mode_active() and self.kill_mode["target_ship"] == shot_result[1]:
            # Append the successful shot to the known coordinates of the shot
            self.kill_mode["ship_coordinates"].append( shot )

            # If this is the 2nd shot on the ship, lock the direction of kill mode
            if not self.kill_mode_locked():
                self.direction_lock( shot , board )

            # Update the targets to be the points just beyond the known boundaries of the ship
            self.kill_mode["targets"] = []
            end_points = board.end_points( shot , self.kill_mode["first_hit"] )
            for point in end_points:
                if not self.is_duplicate_shot( point ):
                    self.kill_mode["targets"].append( point )

        # If the shot was the first hit on a different ship, record the result in other_ships_hit, but continue targeting the first ship
        elif shot_result[0] == True and self.kill_mode_active() and self.kill_mode["target_ship"] != shot_result[1]:
            self.kill_mode["other_ships_hit"].append( [ shot_result[1] , shot ] )
        print(self.kill_mode)

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
        # If kill mode isn't active, continue random firing
        if not self.kill_mode_active():
            duplicate_shot = True
            while duplicate_shot == True:
                shot_coordinate = board.random_coordinate()
                duplicate_shot = self.is_duplicate_shot( shot_coordinate )
        # If kill mode is active, fire at the targeted ship
        else:
            shot_coordinate = self.kill_mode["targets"].pop(0)

        return shot_coordinate

    # Returns the shot for Medium difficulty
    # Shoots only at every other square since the shortest ship is 2 squares long, uses Kill mode when a ship is hit
    # Like playing against someone with a basic strategy
    def shot_medium(self, board):
        pass

    # Returns the shot for Hard difficulty
    # Basic probability model
    # http://thephysicsvirtuosi.com/posts/the-linear-theory-of-battleship.html
    # Like playing against someone with a solid strategy based on knowledge of where ships are likely to be
    def shot_hard(self, board):
        pass

    # Returns the shot for Very Hard difficulty
    # Complex probability model
    def shot_very_hard(self, board):
        pass

    # Gets the squares adjacent to the first hit coordinate
    # Returns a list of valid coordinates that aren't duplicate shots, shuffled to a random order
    def get_adjacents(self, board):
        adjacents = []
        # Addends to move to the adjacent squares, ordered as left, right, up, down
        addends = [ [0,-1],[0,1],[-1,0],[1,0] ]
        split_hit = board.split_coordinate( self.kill_mode["first_hit"] )

        # Loop the addends, creating the 4 adjacent squares
        for addend in addends:
            adjacent_coordinate = [ split_hit[0] + addend[0] , split_hit[1] + addend[1] ]
            coordinate = board.join_coordinate( adjacent_coordinate )
            # If it's a valid coordinate and hasn't been shot at previously, add it to the return value list
            if board.is_valid_format( coordinate ) and board.is_on_board( coordinate ) and not self.is_duplicate_shot( coordinate ):
                adjacents.append( coordinate )
        return adjacents

    # Locks onto the direction of the target and updates the list of possible target squares
    def direction_lock(self, shot, board):
        # Determine if the shot was placed vertically or horizontally from the first square hit
        split_first_hit = board.split_coordinate( self.kill_mode["first_hit"] )
        split_shot = board.split_coordinate( shot )
        self.kill_mode["locked"] = "on"
        
        # If the row is identical, lock on horizontally
        if split_first_hit[0] == split_shot[0]:
            self.kill_mode["lock_direction"] = "h"
            # Remove any remaining targets that aren't in this row
            # self.kill_mode["targets"] = [coordinate for coordinate in self.kill_mode["targets"] if split_shot[0] == board.split_coordinate( coordinate )[0] ]
        # Otherwise, lock on vertically
        else:
            self.kill_mode["lock_direction"] = "v"
            # Remove any remaining targets that aren't in this column
            # self.kill_mode["targets"] = [coordinate for coordinate in self.kill_mode["targets"] if split_shot[1] == board.split_coordinate( coordinate )[1] ]

    # Turn kill mode on and off
    def kill_mode_engage(self, board, coordinate="", target_ship = "" , optimized="n"):
        # Ensure parameters are set to valid values
        if optimized not in ["n","y"]:
            optimized = "n"

        self.kill_mode["target_ship"] = target_ship
        self.kill_mode["first_hit"] = coordinate
        self.kill_mode["ship_coordinates"].append(coordinate)
        self.kill_mode["optimized"] = optimized
        self.kill_mode["targets"] = self.get_adjacents( board )
        self.kill_mode["other_ships_hit"]: []
            
        # If in optimized mode, determine which direction has highest probability of containing ship
        if self.kill_mode["optimized"] == "y":
            pass
        # If not optimized, shuffle the target coordinates
        else:
            shuffle( self.kill_mode["targets"] )

        self.kill_mode["status"] = "on"

    # Disengage kill mode, reset attribute
    def kill_mode_disengage(self):
        self.kill_mode["target_ship"] = ""
        self.kill_mode["first_hit"] = ""
        self.kill_mode["ship_coordinates"] = []
        self.kill_mode["locked"] = "off"
        self.kill_mode["lock_direction"] = ""
        self.kill_mode["optimized"] = "n"
        self.kill_mode["targets"] = []
        self.kill_mode["other_ships_hit"]: []
        self.kill_mode["status"] = "off"

    # Is kill mode active?
    def kill_mode_active(self):
        return True if self.kill_mode["status"] == "on" else False

    # Does kill mode have a direction lock?
    def kill_mode_locked(self):
        return True if self.kill_mode["locked"] == "on" else False

    # Prints the opponent's board with the opponent's ships overlaid on the proper coordinates with CPU's hits and misses
    def print_opponent_board(self, board, ships):
        print(self.shot_results["shots"])
        overlay = {}
        # Add the opponent's ships to the overlay
        for key in ships:
            ship_code = ships[key].get_code()
            for coordinate in ships[key].get_coordinates():
                overlay[coordinate] = ship_code

        # Add the Player's shots to the overlay, overwriting existing coordinates where opponent's ships are with shot results
        for index in range(0,len(self.shot_results["shots"])):
            overlay[self.shot_results["shots"][index]] = self.shot_results["results"][index]

        board.print_board( overlay )