'''
Created on Mar 4, 2013

@author: Devindra

In some ways this is the primary class.
It handles the core game logic and is the model in the pseudo model-view-controller pattern used by this game.
'''
from collections import deque
from random import randint
from pyglet import event
from regicide import actions
from regicide.model import clock
from regicide.entity import player
from regicide.data import characters
from regicide.level import generator

class Game(event.EventDispatcher, clock.TurnClock):
    
    def __init__(self):
        '''
        Constructor
        '''
        clock.TurnClock.__init__(self)
        self.map = generator.MapGenerator(width=60, height=60).generate()
        
        self.player = player.Player(characters.LANCEL.master())
        player_tile = None
        while (player_tile is None or not player_tile.is_unoccupied()):
            player_location = [randint(0, self.map.width), randint(0, self.map.height)]
            player_tile = self.map.get_tile(*player_location)
        player_tile.entity = self.player
        self.player.x = player_location[0]
        self.player.y = player_location[1]
        
        self.accept_input = True

        self.log = deque(maxlen=500)
        self.log_offset = 0
        
        self.selection = None
        
        for row in self.map.grid:
            for tile in row:
                if (tile is not None and tile.entity is not None and type(tile.entity) is not player.Player):
                    self.schedule_turn(0, tile.entity)
        
        self.schedule_turn(1, self.player)
    
    def execute(self, action, *args):
        instance = actions.action.ActionInstance(self.current_entity, action) #TODO: should be self.current_entity
        instance.execute(self, *args)
    
    #event
    def on_mouse_hover(self, hotspot, x=0, y=0):
        '''
        An event triggered when the mouse moves in the game view region.
        This event indicates that the mouse is now hovering over the given location.
        :param tile: a list [x, y], indicating the location of the tile.
        '''
        if (hotspot is None):
            new_selection = None
        else:
            new_selection = (x, y, hotspot)
         
        if (self.selection != new_selection):
            self.selection = new_selection
            self.do_update('cursor')
    
    #event
    def on_hotspot_click(self, hotspot, x, y, button, modifiers):
        '''
        An event triggered when the mouse clicks on a tile.
        :param x: the x position in the grid of the clicked tile.
        :param y: the y position in the grid of the clicked tile.
        :param button: the mouse button that was clicked, could be LEFT, RIGHT, or MIDDLE, from the pyglet.window.mouse module.
        :param modifiers: a bitwise combination of the keyboard modifiers being held down.
        '''
        hotspot.on_click(self, x, y, button, modifiers)
    
    #event
    def activate_command(self, command):
        '''
        An event triggered when the a key is pressed which has been mapped to a command.
        '''
        if (self.accept_input is True):
            if (command.action is not None):
                command.action(self)
    
    def log_message(self, message):
        '''
        Outputs a message to the player log.
        '''
        if (len(self.log) == self.log.maxlen):
            self.log.pop()
            
        self.log.appendleft(message)
    
    def do_update(self, component):
        '''
        Sends an update event to the game's view.
        :param component: indicates which component to update.
        '''
        self.dispatch_event('update', component)
    
    def set_display(self, view):
        '''
        Sends a message the game's view to change the current display.
        :param component: indicates which component to update.
        '''
        self.dispatch_event('display', view)
        

Game.register_event_type('display')
Game.register_event_type('update')