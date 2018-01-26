# Player class
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
            "first_shot": "a1"
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