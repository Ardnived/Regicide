'''
Created on Apr 6, 2013

@author: Devindra
'''
from __future__ import division
from regicide.mvc import State
from regicide.entity import actions

def cancel(game):
    if game.state != game.STATE_NORMAL:
        game.set_state(game.STATE_NORMAL)

def move(game, x=0, y=0):
    if game.state == game.STATE_NORMAL:
        target_x = game.player.x + x
        target_y = game.player.y + y
        
        tile = game.map.get_tile(target_x, target_y)
        if (tile is not None and tile.is_passable()):
            game.execute_action(actions.action.ActionInstance(
                source = game.current_entity,
                action = actions.misc.Move(), 
                target = (target_x, target_y),
            ))
            game.end_turn(100)
    elif game.state == game.STATE_TARGET:
        game.selection = (game.selection[0] + x, game.selection[1] + y, game.selection[2])
        game.do_update('cursor')
    elif game.state == game.STATE_EXPLORE:
        hotspot = game.focus
        if hotspot.is_game_layer():
            x = hotspot.mouse_x + x*(hotspot.width / game.map.width)
            y = hotspot.mouse_y + y*(hotspot.height / game.map.height)
            State.window().set_mouse_position(x, y)
            hotspot.on_hover(game, x, y)
            game.do_update('bounds')
        
def wait(game):
    if game.state != game.STATE_TARGET:
        game.end_turn(100)
        
def look(game):
    if game.state == game.STATE_NORMAL:
        game.set_state(game.STATE_EXPLORE)
        
def toggle_equip(game, item):
    if item.equip_slot is None:
        game.log_message("You can't equip that.")
    else:
        if item in game.current_entity.equipment[item.equip_slot]:
            action = "unequip"
            success = game.player.unequip_item(item)
        else:
            action = "equip"
            success = game.player.equip_item(item)
            
        if success:
            game.do_update('inventory')
            game.log_message("You "+action+" your "+item.name+".")
        else:
            game.log_message("Your "+item.equip_slot.name+" is already full.")
    
    game.do_update('log')
    
def set_state(game, state):
    State.set_current(state)