
import os
from classes import Game
from classes import Player

game = Game()
game.set_board_size()
p1 = Player()
p1.set_name()
p2 = Player()
os.system( 'cls' )

game.print_board()
game.play( p1 , p2 )
