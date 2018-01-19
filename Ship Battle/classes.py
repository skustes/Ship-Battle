from random import randint
import os

# Game class
class Game(object):
    def __init__(self):
        self.turn = "p1"
        self.players = 1    # Set a default
        self.size = 10      # Set a default
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
        # Setup the game board and the players
        self.set_board_size()
        self.set_players()

        # Create the first player
        p1_board = Board( self.size )
        p1 = Player( p1_board , "Player 1" )

        # Create the second player
        p2_board = Board( self.size )
        if self.players == 2:
            p2 = Player( p2_board , "Player 2" )
        else:
            p2 = Player( p2_board , "CPU" , "y" )

        # Clear the screen
        self.wipe()

        # Place the ships on the game board
        p1.place_ships( self.ships )

    def set_board_size(self):
        valid_size = False
        while valid_size == False:
            try: 
                self.size = int( input("What size board? (5-15) ") )
                if self.size in range(5,16):
                    valid_size = True
            except ValueError:
                print("Please enter a valid number")

    def set_players(self):
        valid_number = False
        while valid_number == False:
            try: 
                self.players = int( input("1 or 2 players? ") )
                if self.players in [1,2]:
                    valid_number = True
            except ValueError:
                print("Please enter a valid number")

    # Uses os to clear the screen
    def wipe(self):
        os.system( 'cls' )

class Board(object):
    def __init__(self, size):
        self.size = size
        self.board = []
        row = []
        for i in range(self.size):
            row.append( "^" )
        for j in range(self.size):
            self.board.append( row )
    
    def random_coordinate(self):
        col = chr( randint(1,self.size) + 96 )
        row = randint(1,self.size)
        return col + str(row)

    """
    Attribute access methods
    """
    def print_board(self):
        for row in self.board:
            print( " ".join(row) )

# Player class
class Player(object):
    def __init__(self, board, default_name, is_cpu="n"):
        self.board = board
        self.is_cpu = is_cpu
        if self.is_cpu == "n":
            self.name = self.set_name( default_name )
        else:
            self.name = "CPU"

    def set_name(self, default_name):
        valid_name = False
        while valid_name == False:
            new_name = input( default_name + ", what's your name? " )
            if new_name.isalnum():
                valid_name = True
        return new_name
    
    def place_ships(self, ships):
        print( self.name + ", time to place your ships.\n\n" )
        for key in ships:
            pass #print(key + " " + str(ships[key]))

    """
    Attribute access methods
    """
    def get_name(self):
        return self.name
    def get_board(self):
        return self.board
    def print_board(self):
        self.board.print_board()