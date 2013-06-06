'''
Created on Apr 6, 2013

@author: Devindra

This file defines various actions that can be taken by the player,
when the player presses the appropriate keys, these functions should be triggered.
'''
from __future__ import division
from regicide.mvc import State
from regicide.entity import actions

def cancel(game):
    '''
    Return the game to it's normal state, if it is a different one,
    such as Targeting or Looking around
    '''
    if game.state != game.STATE_NORMAL:
        game.set_state(game.STATE_NORMAL)

def move(game, x=0, y=0):
    if game.state == game.STATE_NORMAL:
        '''
        Move the player towards the target location.
        '''
        target_x = game.player.x + x
        target_y = game.player.y + y
        
        tile = game.map.get_tile(target_x, target_y)
        if tile is not None and tile.is_passable():
            game.execute_action(actions.action.ActionInstance(
                source = game.current_entity,
                action = actions.misc.Move(), 
                target = (target_x, target_y),
            ))
            game.end_turn(100)
    elif game.state == game.STATE_TARGET:
        '''
        Choose the given location as the target for the current targeting state.
        '''
        game.selection = (game.selection[0] + x, game.selection[1] + y, game.selection[2])
        game.do_update('cursor')
    elif game.state == game.STATE_EXPLORE:
        '''
        Move the user's view towards the given location.
        '''
        hotspot = game.focus
        if hotspot.is_game_layer():
            x = hotspot.mouse_x + x*(hotspot.width / game.map.width)
            y = hotspot.mouse_y + y*(hotspot.height / game.map.height)
            State.window().set_mouse_position(x, y)
            hotspot.on_hover(game, x, y)
            game.do_update('bounds')
        
def wait(game):
    '''
    Causes the current entity (player character) to wait for 1 standard turn,
    which is 100 units of time.
    '''
    if game.state != game.STATE_TARGET:
        game.end_turn(100)
        
def look(game):
    '''
    Switch to the Explore state, in which the player can pan around the level.
    '''
    if game.state == game.STATE_NORMAL:
        game.set_state(game.STATE_EXPLORE)
        
def toggle_equip(game, item):
    '''
    Toggle whether the player has a given item equipped.
    
    TODO: change how the action variable in this is implemented so that it can vary for different item types.
    '''
    if item.equip_slot is None:
        # This item doesn't have any equip slots, so it can't be equipped.
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
    '''
    Change the program's current state.
    Specifically, this means switching to a different view,
    so that the player can view a menu, or return to the game view.
    '''
    State.set_current(state)