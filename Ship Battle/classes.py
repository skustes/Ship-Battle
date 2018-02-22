from random import randint, choice, shuffle
import time
import csv
from functions import *

# Session class
# Allows for multiple games with statistics
class Session(object):
    def __init__(self):
        self.game_mode = "p"
        self.simulations = [
            {
                "mode": "shoot",
                "p1_difficulty": 0,
                "p2_difficulty": 0,
                "games": 5000
                },
            {
                "mode": "shoot",
                "p1_difficulty": 1,
                "p2_difficulty": 1,
                "games": 5000
                },
            {
                "mode": "shoot",
                "p1_difficulty": 2,
                "p2_difficulty": 2,
                "games": 5000
                },
            {
                "mode": "shoot",
                "p1_difficulty": 3,
                "p2_difficulty": 3,
                "games": 5000
                },
            {
                "mode": "shoot",
                "p1_difficulty": 4,
                "p2_difficulty": 4,
                "games": 5000
                },
            {
                "mode": "vs",
                "p1_difficulty": 0,
                "p2_difficulty": 1,
                "games": 0
                },
            {
                "mode": "vs",
                "p1_difficulty": 0,
                "p2_difficulty": 2,
                "games": 0
                },
            {
                "mode": "vs",
                "p1_difficulty": 0,
                "p2_difficulty": 3,
                "games": 0
                },
            {
                "mode": "vs",
                "p1_difficulty": 0,
                "p2_difficulty": 4,
                "games": 0
                },
            {
                "mode": "vs",
                "p1_difficulty": 1,
                "p2_difficulty": 2,
                "games": 0
                },
            {
                "mode": "vs",
                "p1_difficulty": 1,
                "p2_difficulty": 3,
                "games": 0
                },
            {
                "mode": "vs",
                "p1_difficulty": 1,
                "p2_difficulty": 4,
                "games": 0
                },
            {
                "mode": "vs",
                "p1_difficulty": 2,
                "p2_difficulty": 3,
                "games": 0
                },
            {
                "mode": "vs",
                "p1_difficulty": 2,
                "p2_difficulty": 4,
                "games": 0
                },
            {
                "mode": "vs",
                "p1_difficulty": 3,
                "p2_difficulty": 4,
                "games": 0
                }
            ]
        # Comment out when not debugging
        """self.simulations = [
            {
                "mode": "shoot",
                "p1_difficulty": 3,
                "p2_difficulty": 3,
                "games": 5
                } 
            ]"""

    # Main control of session
    def start(self):
        self.set_game_mode()

        if self.game_mode == "p":
            self.play()
        else:
            self.simulate()

    # Determine if the user wants to run in normal gameplay or simulation mode
    def set_game_mode(self):
        valid_modes = ["p","s"]
        valid_mode = False
        while valid_mode == False:
            self.game_mode = input("Do you want to play or run a simulation? [p/s] ")
            if self.game_mode in valid_modes:
                valid_mode = True

    # Play normally
    def play(self):
        continue_playing = True
        while continue_playing is True:
            game = Game()
            game.play()

            continue_playing = self.play_again()

    # Simulate games for testing/statistical purposes
    def simulate(self):
        for simulation in self.simulations:
            for game_number in range( 0 , simulation["games"] ):
                print( "Game number:", game_number+1 )
                game = Game()
                statistics = game.simulation( simulation["p1_difficulty"] , simulation["p2_difficulty"] , simulation["mode"] )
                self.print_to_file( statistics , simulation["mode"] )

    # Does the player want to play again?
    # Returns True or False
    def play_again(self):
        valid_input = False
        while valid_input == False:
            play_again = input( "Do you want to play again? (y/n) " ).lower()
            if play_again in ["y","n"]:
                valid_input = True
        return True if play_again == "y" else False

    def print_to_file(self, statistics, mode):
        if mode == "shoot":
            data = [ statistics["p1_difficulty"] , statistics["shots"] , statistics["accuracy"] , statistics["first_hit"] , statistics["kill_mode_accuracy"] , statistics["first_shot_accuracy"] ]
        else:
            data = [ statistics["p1_difficulty"] , statistics["p1_shots"] , statistics["p2_difficulty"] , statistics["p2_shots"] , statistics["winner"] ]

        file_name = mode + "_statistics.csv"
        with open( file_name , 'a' , newline='' ) as stats_file:
            writer = csv.writer( stats_file , delimiter=',' )
            writer.writerow( data )
       
# Game class
# Sets up the game and handles game play
class Game(object):
    def __init__(self):
        self.turn = "p1"
        self.players = 1
        self.min_max_difficulty = [0,5]
        self.difficulty = 0                 # Set difficulty to easiest level by default
        self.status = 0                     # 0 if game in progress, 1 if p1 wins, 2 if p2 wins
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

    # Plays a game between 1 Player and CPU or 2 Players
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
        if p2.is_cpu():
            print("Placing CPU ships...")
            time.sleep(1)
        p2.place_ships( self.ships , board )
        
        # Repeat until someone wins
        while self.status == 0:
            self.turn = "p2"
            # wipe()

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
                print( p2.kill_mode_accuracy() )
                print( p2.first_hit() )
                print( p2.shot_results["shots"] )
                print( p2.shot_results["results"] )
                print( p2.shot_results["mode"] )
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
            # self.turn = "p2" if self.turn == "p1" else "p1"
            print(p2.kill_mode)
            print("")
            print("")
            print("")
            # input("Press enter to continue.")
    
    # Plays a simulated game between two CPU players
    # Has two modes:    "shoot" - test and record shooting algorithm
    #                   "vs"    - test two different CPU difficulties against each other
    def simulation(self, p1_diff, p2_diff, mode="shoot"):
        if mode not in ["shoot","vs"]:
            mode = "shoot"

        # Setup the board and the players
        board = Board( 10 )
        p1 = CPUPlayer( p1_diff )
        p2 = CPUPlayer( p2_diff )

        # Place the ships on the game board
        p1.place_ships( self.ships , board )
        p2.place_ships( self.ships , board )

        # Repeat until someone wins
        while self.status == 0:
            # Alternate turns
            if self.turn == "p1":
                shot = p1.bombs_away( board )
                shot_result = p2.check_shot( shot )
                p1.record_shot_result( shot , shot_result , board )
            else:
                shot = p2.bombs_away( board )
                shot_result = p1.check_shot( shot )
                p2.record_shot_result( shot , shot_result , board )

            if p1.get_ships_remaining() == 0:
                self.status = 2
            elif p2.get_ships_remaining() == 0:
                self.status = 1

            if mode == "vs":
                self.turn = "p2" if self.turn == "p1" else "p1"
            if self.status != 0:
                return self.statistics( p1 , p2 , mode , "p" + str( self.status ) )

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
        valid_entries = [ x for x in range(self.min_max_difficulty[0],self.min_max_difficulty[1]+1) ]
        valid_difficulty = False
        while valid_difficulty == False:
            self.difficulty = int( input( "Set difficulty level [" + str(self.min_max_difficulty[0]) + "-" + str(self.min_max_difficulty[1]) + "]: " ) )
            if self.difficulty in valid_entries:
                valid_difficulty = True

    # Returns the name of a ship given the board code for a ship
    def get_ship_by_code(self, code):
        for key in self.ships:
            if self.ships[key]["code"] == code:
                return self.ships[key]["name"]

    # Returns the statistics of a game
    def statistics(self, p1, p2, mode="shoot", winner=""):
        if mode not in ["shoot","vs"]:
            mode = "shoot"

        # Shoot mode - p1_difficulty, shots taken, accuracy, first hit accuracy
        # vs mode - p1_difficulty, p2_difficulty, winner
        if mode == "shoot":
            return {
                "p1_difficulty": p1.get_difficulty(),
                "shots": p1.shots_taken(),
                "accuracy": p1.accuracy(),
                "first_hit": p1.first_hit(),
                "kill_mode_accuracy": p1.kill_mode_accuracy(),
                "first_shot_accuracy": p1.first_shot_accuracy()
                }
        else:
            return {
                "p1_difficulty": p1.get_difficulty(),
                "p1_shots": p1.shots_taken(),
                "p2_difficulty": p2.get_difficulty(),
                "p2_shots": p2.shots_taken(),
                "winner": winner
                }

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

    # Returns the points to the left/above and to the right/below the ship coordinates
    # Checks the points for validity and removes invalid points
    # Returns False if they don't share a row or column
    def end_points(self, ship_coordinates):
        # Sort the coordinates into ascending order ex: a2,b2,c2 or f2,f3,f4
        split_coordinates = []
        for coordinate in ship_coordinates:
            split_coordinates.append( self.split_coordinate( coordinate ) )

        split_coordinates.sort()

        # Get the first and last coordinates from the sorted list 
        coordinate_1 = split_coordinates[0]
        coordinate_2 = split_coordinates[-1]
        return_coordinates = []

        # If the coordinates share a row, return the points to the left and right
        if coordinate_1[0] == coordinate_2[0]:
            # Determine which is left and which is right
            if coordinate_1[1] <= coordinate_2[1]:
                one_left = coordinate_1
                one_right = coordinate_2
            else:
                one_left = coordinate_2
                one_right = coordinate_1

            # Move one to the left and append the point if it's valid
            one_left = self.join_coordinate( [ one_left[0] , one_left[1] - 1 ] )
            if self.is_valid_format( one_left ) and self.is_on_board( one_left ):
                return_coordinates.append( one_left )
            # Move one to the right and append the point if it's valid
            one_right = self.join_coordinate( [ one_right[0] , one_right[1] + 1 ] )
            if self.is_valid_format( one_right ) and self.is_on_board( one_right ):
                return_coordinates.append( one_right )
        # If the coordinates share a column, return the points above and below
        elif coordinate_1[1] == coordinate_2[1]:
            # Determine which is more towards the top of the board
            if coordinate_1[0] <= coordinate_2[0]:
                one_above = coordinate_1
                one_below = coordinate_2
            else:
                one_above = coordinate_2
                one_below = coordinate_1

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

class Probability(Board):
    pass

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
        self.shot_results = { "shots": [] , "results": [] , "mode": [] , "km_first": [] }

        # CPU Player extended attributes
        self.cpu = "y"
        self.difficulty = difficulty
        self.kill_mode = {
            "status": "off",
            "target_ship": "",
            "first_hit": "",
            "ship_coordinates": [],
            "optimized": "",
            "targets": [],
            "other_ships_hit": []
            }
        self.record_first_hit = 0 # For statistical measurement of first hit accuracy

    # Use auto-place to put down the CPU ships
    def place_ships(self, ships, board):
        # Record the opponent's ships as alive
        self.record_opponent_ships( ships )

        # And place the ships for the CPU
        self.auto_place( ships , board )
    
    # Record the letter code of each ship for tracking which ships the opponent still has
    def record_opponent_ships(self, ships):
        self.opponent_ships = {}
        for ship in ships:
            current_ship = ships[ship]
            self.opponent_ships[ current_ship["code"] ] = 1

    # Updates the shot_results lists and activates/deactivates kill mode
    # Expects grid coordinate shot at and shot_result list returned from opponent's check_shot method
    def record_shot_result(self, shot, shot_result, board):
        self.shot_results["shots"].append( shot )
        self.shot_results["results"].append( "O" if shot_result[0] == False else "X" )
        self.shot_results["mode"].append( "K" if self.kill_mode_active() else "S" )

        if self.record_first_hit == 1: # If this is the first shot after a hit, record it for checking accuracy of first shots
            self.shot_results["km_first"].append( shot )
            self.record_first_hit = 0

        # If the target ship was sunk...
        if shot_result[0] == True and shot_result[2] == False:
            # If the ship being targeted was sunk
            if self.kill_mode["target_ship"] == shot_result[1]:
                # Record the ship as sunk and disengage Kill Mode
                self.opponent_ships[ shot_result[1] ] = 0
                self.kill_mode_disengage()

                # If any other ships were hit, reactivate kill mode to target the next ship
                if len( self.kill_mode["other_ships_hit"] ) > 0:
                    next_ship = self.kill_mode["other_ships_hit"].pop(0)
                    self.kill_mode_engage( board, next_ship[1] , next_ship[0] )

                    # If the ship was already hit more than once ( rare bug with A = A1-E1, B = C2-C6, S = D2-F2 or 
                    # similar configuration where a ship can be hit multiple times before active targeting )
                    if len( next_ship[2] ) > 1:
                        self.kill_mode["ship_coordinates"] = next_ship[2]
                        self.kill_mode["targets"] = self.target_ship( board , next_ship[2] )
            # If another ship that was hit previously was sunk, remove it from the other_ships_hit list
            else:
                self.kill_mode["other_ships_hit"] = [ ship for ship in self.kill_mode["other_ships_hit"] if ship[0] != shot_result[1] ]
                self.opponent_ships[ shot_result[1] ] = 0

                
        # If the shot was the first hit on a ship, engage kill mode
        elif shot_result[0] == True and not self.kill_mode_active():
            self.kill_mode_engage( board, shot , shot_result[1] )
        # If the shot was the a hit on the same ship...
        elif shot_result[0] == True and self.kill_mode_active() and self.kill_mode["target_ship"] == shot_result[1]:
            # Append the successful shot to the known coordinates of the shot
            self.kill_mode["ship_coordinates"].append( shot )

            # If this is the 2nd shot on the ship, lock the direction of kill mode
            #if not self.kill_mode_locked():
            #    self.direction_lock( shot , board )

            # Update the targets to be the points just beyond the known boundaries of the ship
            # self.kill_mode["targets"] = []
            self.kill_mode["targets"] = self.target_ship( board , self.kill_mode["ship_coordinates"] )

        # If the shot was the first hit on a different ship, record the result in other_ships_hit, but continue targeting the first ship
        elif shot_result[0] == True and self.kill_mode_active() and self.kill_mode["target_ship"] != shot_result[1]:
            # Determine if this ship has been hit before ( rare bug with A = A1-E1, B = C2-C6, S = D2-F2 or 
            # similar configuration where a ship can be hit multiple times before active targeting )
            ship_found = False
            for ship in self.kill_mode["other_ships_hit"]:
                # If the ship was already hit, append the shot to the known ship coordinates
                if ship[0] == shot_result[1]:
                    ship[2].append( shot )
                    ship_found = True
            
            # If the ship hasn't already been hit, append it
            if ship_found is False:
                self.kill_mode["other_ships_hit"].append( [ shot_result[1] , shot , [ shot ] ] )

    # Calls the shot generator for based on difficulty level
    def bombs_away(self, board):
        # http://thephysicsvirtuosi.com/posts/the-linear-theory-of-battleship.html
        if self.difficulty == 0:
            shot_coordinate = self.shot_level_0( board )
        elif self.difficulty == 1:
            shot_coordinate = self.shot_level_1( board )
        elif self.difficulty == 2:
            shot_coordinate = self.shot_level_2( board )
        elif self.difficulty == 3:
            shot_coordinate = self.shot_level_3( board )
        elif self.difficulty == 4:
            shot_coordinate = self.shot_level_4( board )
        elif self.difficulty == 5:
            shot_coordinate = self.shot_level_5( board )
        return shot_coordinate
        
    # Returns the shot for Difficulty Level 0
    # Random shots with no Kill mode when a ship is hit
    def shot_level_0(self, board):
        return self.random_shot( board )

    # Returns the shot for Difficulty Level 1
    # Random shots with Kill mode when a ship is hit
    def shot_level_1(self, board):
        # If kill mode isn't active, continue random firing
        if not self.kill_mode_active():
            shot_coordinate = self.random_shot( board )
        # If kill mode is active, fire at the targeted ship
        else:
            shot_coordinate = self.kill_mode["targets"].pop(0)

        return shot_coordinate

    # Returns the shot for Difficulty Level 2
    # Random shots with optimized Kill mode when a ship is hit to determine which direction is most likely to contain a ship
    def shot_level_2(self, board):
        # If kill mode isn't active, continue random firing
        if not self.kill_mode_active():
            shot_coordinate = self.random_shot( board )
        # If kill mode is active, fire at the targeted ship
        else:
            shot_coordinate = self.kill_mode["targets"].pop(0)

        return shot_coordinate

    # Returns the shot for Difficulty Level 3
    # Shoots only at every other square, regular kill mode
    def shot_level_3(self, board):
        # If kill mode isn't active, continue firing at every other square
        if not self.kill_mode_active():
            shot_coordinate = self.random_shot( board , "y" )
        # If kill mode is active, fire at the targeted ship
        else:
            shot_coordinate = self.kill_mode["targets"].pop(0)

        return shot_coordinate

    # Returns the shot for Difficulty Level 4
    # Shoots only at every other square, optimized kill mode
    def shot_level_4(self, board):
        # If kill mode isn't active, continue firing at every other square
        if not self.kill_mode_active():
            shot_coordinate = self.random_shot( board , "y" )
        # If kill mode is active, fire at the targeted ship
        else:
            shot_coordinate = self.kill_mode["targets"].pop(0)

        return shot_coordinate

    # Returns the shot for Difficulty Level 5
    # Uses a probability model to determine squares with highest chance of containing a ship, optimized kill mode
    def shot_level_5(self, board):
        # If kill mode isn't active, continue firing at every other square
        if not self.kill_mode_active():
            shot_coordinate = self.random_shot( board , "y" )
        # If kill mode is active, fire at the targeted ship
        else:
            shot_coordinate = self.kill_mode["targets"].pop(0)

        return shot_coordinate

    # Returns a random coordinate on the board that is a non-duplicate shot
    # If parity parameter is set, constrains shots to coordinates where row and column add up to an even number (A1, A3, E5, etc)
    def random_shot(self, board, parity="n"):
        if parity not in ["y","n"]:
            parity = "n"

        # While loop defaults to ensure it runs at least once
        duplicate_shot = True
        parity_check_passed = False if parity == "y" else True # If not using parity, no need for a check, so set it to True by default

        # Continue finding a random coordinate until one is found that passes the parity check and is not a duplicate
        while duplicate_shot is True or parity_check_passed is False:
            shot_coordinate = board.random_coordinate()
            split_shot = board.split_coordinate( shot_coordinate )

            # If using parity shooting, check to see if this is a correct square
            if parity == "y":
                if ( split_shot[0] + split_shot[1] ) % 2 == 0:
                    parity_check_passed = True
                else:
                    parity_check_passed = False

            duplicate_shot = self.is_duplicate_shot( shot_coordinate )

        return shot_coordinate

    # Turn kill mode on and off
    def kill_mode_engage(self, board, coordinate, target_ship):
        self.kill_mode["target_ship"] = target_ship
        self.kill_mode["first_hit"] = coordinate
        self.kill_mode["ship_coordinates"].append(coordinate)
        self.kill_mode["optimized"] = "y" if self.difficulty in [2,4,5] else "n"

        adjacent_targets = self.get_adjacents( board )
            
        # If in optimized mode, determine which direction has highest probability of containing ship
        if self.kill_mode["optimized"] == "y":
            self.kill_mode["targets"] = self.optimize_targets( board )
        # If not optimized, shuffle the targets for random firing
        else:
            self.kill_mode["targets"] = adjacent_targets
            shuffle( self.kill_mode["targets"] )

        self.kill_mode["status"] = "on"
        self.record_first_hit = 1
    
    # Gets the squares adjacent to the first hit coordinate
    # Returns a list of valid coordinates that aren't duplicate shots
    def get_adjacents(self, board):
        adjacents = []
        # Directional shifts to move to the adjacent squares, ordered as up, down, left, right
        direction_shifts = [ [0,-1],[0,1],[-1,0],[1,0] ]
        split_hit = board.split_coordinate( self.kill_mode["first_hit"] )

        # Loop the directional shifts, creating the 4 adjacent squares
        for shift in direction_shifts:
            adjacent_coordinate = [ split_hit[0] + shift[0] , split_hit[1] + shift[1] ]
            coordinate = board.join_coordinate( adjacent_coordinate )
            # If it's a valid coordinate and hasn't been shot at previously, add it to the return value list
            if board.is_valid_format( coordinate ) and board.is_on_board( coordinate ) and not self.is_duplicate_shot( coordinate ):
                adjacents.append( coordinate )
        return adjacents

    # Gets the end points of the ship, excluding duplicate shots
    def target_ship(self, board, coordinates):
        return [ point for point in board.end_points( coordinates ) if not self.is_duplicate_shot( point ) ]

    # Optimize the targets based on determining if firing vertically or horizontally has the highest chance of containing a ship
    # Returns a list of target coordinates
    def optimize_targets(self, board):
        # Loop 4 times, determining which direction has the highest probability of containing a ship, 
        # then set that direction to zero available squares to evaluate additional directions
        direction_shifts = []
        force_zeros = []
        first_hit = self.kill_mode["first_hit"]
        split_hit = board.split_coordinate( first_hit )
        row = split_hit[0]
        col = split_hit[1]

        # Coordinate shifts to move up, down, left, and right
        up = [-1,0]
        down = [1,0]
        left = [0,-1]
        right = [0,1]
        for x in range(0,4):
            ship_possibilities = self.ship_fit( first_hit , board , force_zeros )
            v_possibles = ship_possibilities["v_possibles"]
            h_possibles = ship_possibilities["h_possibles"]
            u_possibles = ship_possibilities["u"]
            d_possibles = ship_possibilities["d"]
            l_possibles = ship_possibilities["l"]
            r_possibles = ship_possibilities["r"]

            # If both directions are zero, break the loop
            if v_possibles == 0 and h_possibles == 0:
                break

            # Determine which axis and which direction on that axis has the most possible ships that can fit in it
            # Then add that direction to force_zeros to optimize remaining directions
            if v_possibles > h_possibles:
                if u_possibles > d_possibles:
                    direction_shifts.append( up )
                    force_zeros.append( "u" )
                elif d_possibles > u_possibles:
                    direction_shifts.append( down )
                    force_zeros.append( "d" )
                else:
                    random_direction = randint(0,1)
                    if random_direction == 0:
                        direction_shifts.append( up )
                        force_zeros.append( "u" )
                    else:
                        direction_shifts.append( down )
                        force_zeros.append( "d" )
            elif h_possibles > v_possibles:
                if l_possibles > r_possibles:
                    direction_shifts.append( left )
                    force_zeros.append( "l" )
                elif r_possibles > l_possibles:
                    direction_shifts.append( right )
                    force_zeros.append( "r" )
                else:
                    random_direction = randint(0,1)
                    if random_direction == 0:
                        direction_shifts.append( left )
                        force_zeros.append( "l" )
                    else:
                        direction_shifts.append( right )
                        force_zeros.append( "r" )
            # Otherwise, equal possibility, randomly pick an axis and direction
            else:
                random_axis = randint(0,1)
                # Horizontal axis
                if random_axis == 0:
                    if l_possibles > r_possibles:
                        direction_shifts.append( left )
                        force_zeros.append( "l" )
                    elif r_possibles > l_possibles:
                        direction_shifts.append( right )
                        force_zeros.append( "r" )
                    else:
                        random_direction = randint(0,1)
                        if random_direction == 0:
                            direction_shifts.append( left )
                            force_zeros.append( "l" )
                        else:
                            direction_shifts.append( right )
                            force_zeros.append( "r" )
                # Vertical axis
                else:
                    if u_possibles > d_possibles:
                        direction_shifts.append( up )
                        force_zeros.append( "u" )
                    elif d_possibles > u_possibles:
                        direction_shifts.append( down )
                        force_zeros.append( "d" )
                    else:
                        random_direction = randint(0,1)
                        if random_direction == 0:
                            direction_shifts.append( up )
                            force_zeros.append( "u" )
                        else:
                            direction_shifts.append( down )
                            force_zeros.append( "d" )

        # Loop the directional shift addends, creating the 4 adjacent squares
        adjacents = []
        for shift in direction_shifts:
            adjacent_coordinate = [ row + shift[0] , col + shift[1] ]
            coordinate = board.join_coordinate( adjacent_coordinate )
            # If it's a valid coordinate and hasn't been shot at previously, add it to the return value list
            if board.is_valid_format( coordinate ) and board.is_on_board( coordinate ) and not self.is_duplicate_shot( coordinate ):
                adjacents.append( coordinate )

        return adjacents

    # Determines how many ships can fit in the spaces above, below, left, and right from this coordinate, 
    # along with the total vertical and horizontal possibilities
    # Returns dictionary with six keys: vertical, horizontal, u, d, l, r
    def ship_fit(self, coordinate, board, force_zeros=[]):
        print(coordinate)
        print("")
        split_hit = board.split_coordinate( coordinate )
        row = split_hit[0]
        col = split_hit[1]
   
        directions = {
            "u": {
                "axis": 1,          # 0 = row, 1 = column
                "multiplier": -1,   # -1 for moving up/left, 1 for moving down/right
                "count": 0          # Number of available squares in this direction
                },
            "d": {
                "axis": 1,
                "multiplier": 1,
                "count": 0
                },
            "l": {
                "axis": 0,
                "multiplier": -1,
                "count": 0
                },
            "r": {
                "axis": 0,
                "multiplier": 1,
                "count": 0
                }
            }
        ways_to_fit = {
            "A": [[0,0,0,0,1],
                  [0,0,0,1,2],
                  [0,0,1,2,3],
                  [0,1,2,3,4],
                  [1,2,3,4,5]
                ],
            "B": [[0,0,0,1,1],
                  [0,0,1,2,2],
                  [0,1,2,3,3],
                  [1,2,3,4,4],
                  [1,2,3,4,4]
                ],
            "C": [[0,0,1,1,1],
                  [0,1,2,2,2],
                  [1,2,3,3,3],
                  [1,2,3,3,3],
                  [1,2,3,3,3]
                ],
            "S": [[0,0,1,1,1],
                  [0,1,2,2,2],
                  [1,2,3,3,3],
                  [1,2,3,3,3],
                  [1,2,3,3,3]
                ],
            "D": [[0,1,1,1,1],
                  [1,2,2,2,2],
                  [1,2,2,2,2],
                  [1,2,2,2,2],
                  [1,2,2,2,2]
                ]
            }

        # Count how many valid and non-duplicate shot coordinates there are in each direction
        for direction in directions:
            if direction not in force_zeros:
                current_direction = directions[direction]
                for i in range(1,5):
                    i_signed = current_direction["multiplier"] * i
                    if current_direction["axis"] == 1:      # If checking a column
                        next_coordinate = board.join_coordinate( [ row + i_signed , col ] )
                        print(next_coordinate)
                        if board.is_valid_format( next_coordinate ) and board.is_on_board( next_coordinate ) and not self.is_duplicate_shot( next_coordinate ):
                            directions[direction]["count"] += 1
                        else:
                            break
                    else:                                   # Else, checking a row
                        next_coordinate = board.join_coordinate( [ row , col + i_signed ] )
                        print(next_coordinate)
                        if board.is_valid_format( next_coordinate ) and board.is_on_board( next_coordinate ) and not self.is_duplicate_shot( next_coordinate ):
                            directions[direction]["count"] += 1
                        else:
                            break

        print(directions)
        # Variables to hold total number of ships that could fit in the vertical and horizontal axes
        ships_possible = {
            "v_possibles": 0,
            "h_possibles": 0,
            "u": 0,
            "d": 0,
            "l": 0,
            "r": 0
            }

        for ship in ways_to_fit:
            # Add the number of ways this ship could fit into the space if the ship is still alive
            if self.opponent_ships[ship] == 1:
                ships_possible["v_possibles"] += ways_to_fit[ship][ directions["u"]["count"] ][ directions["d"]["count"] ]
                ships_possible["h_possibles"] += ways_to_fit[ship][ directions["l"]["count"] ][ directions["r"]["count"] ]
                ships_possible["u"] += ways_to_fit[ship][ directions["u"]["count"] ][0]
                ships_possible["d"] += ways_to_fit[ship][ directions["d"]["count"] ][0]
                ships_possible["l"] += ways_to_fit[ship][ directions["l"]["count"] ][0]
                ships_possible["r"] += ways_to_fit[ship][ directions["r"]["count"] ][0]
                
        return ships_possible

    # Disengage kill mode, reset attribute
    def kill_mode_disengage(self):
        self.kill_mode["target_ship"] = ""
        self.kill_mode["first_hit"] = ""
        self.kill_mode["ship_coordinates"] = []
        self.kill_mode["optimized"] = ""
        self.kill_mode["targets"] = []
        self.kill_mode["status"] = "off"

    # Is kill mode active?
    def kill_mode_active(self):
        return True if self.kill_mode["status"] == "on" else False

    # Prints the opponent's board with the opponent's ships overlaid on the proper coordinates with CPU's hits and misses
    def print_opponent_board(self, board, ships):
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

    # Returns the difficulty level of the CPU player
    def get_difficulty(self):
        return self.difficulty

    # Returns the number of shots taken
    def shots_taken(self):
        return len( self.shot_results["shots"] )

    # Returns the number of hits divided by the number of shots
    def accuracy(self):
        return round( self.shot_results["results"].count("X") / self.shots_taken() , 2 )

    # Returns the shot number of the first hit on any ship
    # Helps understand seek mode accuracy
    def first_hit(self):
        return self.shot_results["results"].index("X") + 1

    # Returns the accuracy of Kill mode
    def kill_mode_accuracy(self):
        kill_mode_hits = 0
        kill_mode_misses = 0
        # Determine how many hits and shots were made in Kill Mode
        for index in range( 0 , len( self.shot_results["results"] ) ):
            if self.shot_results["results"][index] == "X" and self.shot_results["mode"][index] == "K":
                kill_mode_hits += 1
            elif self.shot_results["results"][index] == "O" and self.shot_results["mode"][index] == "K":
                kill_mode_misses += 1
        
        return round( kill_mode_hits / ( kill_mode_hits + kill_mode_misses) , 2 )

    # Determines the accuracy of the first shot in Kill mode
    # Returns hits/total first shots
    def first_shot_accuracy(self):
        hits = 0
        misses = 0

        for hit in self.shot_results["km_first"]:
            index_of_hit = self.shot_results["shots"].index(hit)
            
            if self.shot_results["results"][index_of_hit] == "X":
                hits += 1
            else:
                misses += 1

        return hits/(hits+misses)
