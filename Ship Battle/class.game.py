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