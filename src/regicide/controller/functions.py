'''
Created on Apr 6, 2013

@author: Devindra
'''
from regicide.mvc import State

def move(game, x=0, y=0):
    target_x = game.player.x + x
    target_y = game.player.y + y
    
    tile = game.map.get_tile(target_x, target_y)
    if (tile is not None and tile.is_passable()):
        game.move_player_to(target_x, target_y)
        game.end_player_turn(100)
        
def wait(game):
    game.end_player_turn(100)
    
def set_state(game, state):
    State.set_current(state)