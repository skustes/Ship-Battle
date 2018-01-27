import os

# Uses os to clear the screen
def wipe():
    os.system( 'cls' )

# Returns the character corresponding to a number (1 = a, 2 = b, etc)
def num_to_chr(number):
    return chr( number + 96 ).lower()

# Returns the number corresponding to a character (1 = A, 2 = B, etc)
def chr_to_num(character):
    return ord( character.lower() ) - 96

# For purposes of stopping execution without closing window during debugging
import sys
def stop_game():
    input("Press enter when ready to close")
    sys.exit()