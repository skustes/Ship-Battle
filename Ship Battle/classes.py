# Game class
class Game(object):
    def __init__(self):
        self.turn = "p1"
        self.board = []

    def set_board_size(self):
        valid_size = False
        while valid_size == False:
            try: 
                self.size = int( input("What size board? (5-15) ") )
                if self.size in range(5,16):
                    valid_size = True
                    row = []
                    for i in range(self.size):
                        row.append( "^" )
                    for j in range(self.size):
                        self.board.append( row )
            except ValueError:
                print("Please enter a valid number")
    
    def play(self, p1, p2):
        print("Time to play: " + p1.get_name() + " vs " + p2.get_name() )

    """
    Variable accesss methods
    """
    def get_size(self):
        return self.size
    def get_board(self):
        return self.board
    def print_board(self):
        for row in self.board:
            print( " ".join(row) )


# Player class
class Player(object):
    def __init__(self):
        self.name = "cpu"

    def set_name(self):
        valid_name = False
        while valid_name == False:
            self.name = input("What's your name? ")
            if self.name.isalnum():
                valid_name = True

    """
    Variable access methods
    """
    def get_name(self):
        return self.name