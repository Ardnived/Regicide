'''
Created on Mar 4, 2013

@author: Devindra

In some ways this is the primary class.
It handles the core game logic and is the model in the pseudo model-view-controller pattern used by this game.
'''
from __future__ import division
import sys
from collections import deque
from random import randint
from pyglet import event
from regicide.model import clock
from regicide.entity import player
from regicide.data import characters
from regicide.level import generator, tile
from regicide.controller.game import GameHotspot

class Game(event.EventDispatcher, clock.TurnClock):
    STATE_NORMAL = 0
    STATE_TARGET = 1
    STATE_EXPLORE = 2
    
    def __init__(self):
        '''
        Constructor
        '''
        clock.TurnClock.__init__(self)
        self.map = generator.CastleGenerator(width=60, height=60).generate()
        
        self.player = player.Player(characters.ELLIOT.master())
        player_tile = None
        while player_tile is None or not player_tile.is_unoccupied():
            player_location = [randint(0, self.map.width), randint(0, self.map.height)]
            player_tile = self.map.get_tile(*player_location)
        
        player_tile.entity = self.player
        self.player.x = player_location[0]
        self.player.y = player_location[1]
        
        self._accept_input = True

        self.log = deque(maxlen=500)
        self.log_offset = 0
        self.info = ""
        
        self.state = None
        self.focus = None
        
        for row in self.map.grid:
            for tile in row:
                if (tile is not None and tile.entity is not None and type(tile.entity) is not player.Player):
                    self.schedule_turn(0, tile.entity)
        
        self.schedule_turn(1, self.player)
        self.set_state(Game.STATE_NORMAL)
    
    #event
    def on_mouse_hover(self, hotspot, mouse_x=0, mouse_y=0):
        '''
        An event triggered when the mouse moves in the game view region.
        This event indicates that the mouse is now hovering over the given location.
        '''
        if hotspot is not None:
            hotspot.on_hover(self, mouse_x, mouse_y)
        
        if self.focus != hotspot:
            if self.focus is not None:
                self.focus.on_focus_lost(self)
            
            self.focus = hotspot
            
            if hotspot is not None:
                self.focus.on_focus_gained(self)
    
    #event
    def on_hotspot_click(self, hotspot, button, modifiers):
        '''
        An event triggered when the mouse clicks on a tile.
        :param x: the x position in the grid of the clicked tile.
        :param y: the y position in the grid of the clicked tile.
        :param button: the mouse button that was clicked, could be LEFT, RIGHT, or MIDDLE, from the pyglet.window.mouse module.
        :param modifiers: a bitwise combination of the keyboard modifiers being held down.
        '''
        if self.accept_input:
            if self.state == Game.STATE_TARGET and hotspot.is_game_layer():
                x = hotspot.selection_x + hotspot.grid_x
                y = hotspot.selection_y + hotspot.grid_y
                
                if self.is_valid_target(x, y) is True:
                    self.target_action.target = self.map.get_tile(x, y)
                    self.target_action.execute(self)
                    self.end_turn(self.target_action.type.get_time_cost())
                    self.set_state(Game.STATE_NORMAL)
            else:
                hotspot.on_click(self, button, modifiers)
    
    def is_valid_target(self, x, y):
        target_tile = self.map.get_tile(x, y)
        
        if target_tile is None:
            return None
        
        tile_target_types = target_tile.get_target_types()
        
        if self.state == Game.STATE_TARGET:
            if (abs(x - self.current_entity.x) <= self.target_action.type.range
                and abs(y - self.current_entity.y) <= self.target_action.type.range):
                
                if len(set(self.target_action.type.targets) & tile_target_types) != 0:
                    return True
                elif tile.TARGET_WALL in tile_target_types:
                    return None
                else:
                    return False
            else:
                return None
        else:
            if tile.TARGET_WALL in tile_target_types:
                return None
            else:
                return tile.TARGET_ENTITY in tile_target_types
        
    #event
    def activate_command(self, command):
        '''
        An event triggered when the a key is pressed which has been mapped to a command.
        '''
        if self.accept_input is True:
            if command.action is not None:
                command.action(self)
    
    def log_message(self, message):
        '''
        Outputs a message to the game log.
        '''
        if len(self.log) == self.log.maxlen:
            self.log.pop()
            
        self.log.appendleft(message)
        
        if self.info:
            self.info = None
    
    def display_info(self, message):
        '''
        Display a message in the game log.
        '''
        if self.info != message:
            self.info = message
            self.do_update('log')
    
    def do_update(self, component):
        '''
        Sends an update event to the game's view.
        :param component: indicates which component to update.
        '''
        if self.state == Game.STATE_EXPLORE and component == 'cursor':
            self.dispatch_event('update', 'bounds')
        
        self.dispatch_event('update', component)
    
    def set_display(self, view):
        '''
        Sends a message the game's view to change the current display.
        :param component: indicates which component to update.
        '''
        self.dispatch_event('display', view)
    
    def execute_action(self, instance):
        if instance.target is not None:
            instance.execute(self)
        else:
            self.set_state(Game.STATE_TARGET, action=instance)
            self.log_message("Awaiting Action target...")
            self.do_update('log')
            
            if instance.type.range != sys.maxint:
                self.do_update('shadows')
        
    def set_state(self, state, **kargs):
        # Tear down the current state.
        if self.state == Game.STATE_NORMAL:
            pass
        elif self.state == Game.STATE_TARGET:
            self.target_action = None
        elif self.state == Game.STATE_EXPLORE:
            pass
        
        self.state = state
        
        # Set up new state.
        if self.state == Game.STATE_NORMAL:
            pass
        elif self.state == Game.STATE_TARGET:
            self.target_action = kargs['action']
        elif self.state == Game.STATE_EXPLORE:
            pass
        
        self.do_update('all')
    
    def get_center(self):
        if self.state == Game.STATE_EXPLORE and isinstance(self.focus, GameHotspot):
            hotspot = self.focus
            x = (hotspot.mouse_x - hotspot.x) * (self.map.width / hotspot.width)
            y = (hotspot.mouse_y - hotspot.y) * (self.map.height / hotspot.height)
            return (int(x), int(y))
        else:
            return (self.player.x, self.player.y)
        

Game.register_event_type('display')
Game.register_event_type('update')