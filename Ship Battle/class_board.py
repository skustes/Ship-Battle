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