'''
Created on Mar 4, 2013

@author: Devindra

In some ways this is the primary class.
It handles the core game logic and is the model in the pseudo model-view-controller pattern used by this game.
'''
import heapq
from collections import deque
from random import randint
from pyglet import event
from pyglet import clock
from regicide.entity import player
from regicide.entity import properties
from regicide.data import characters
from regicide.level import generator

class Game(event.EventDispatcher):
    
    def __init__(self):
        '''
        Constructor
        '''
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
        
        self.turn_queue = []
        self.current_turn = 0
        
        self.selection = None
        
        for row in self.map.grid:
            for tile in row:
                if (tile is not None and tile.entity is not None and type(tile.entity) is not player.Player):
                    self.schedule_turn(0, tile.entity.on_turn)
        
        self.schedule_turn(1, player.Player.TURN)
    
    def move_player_to(self, target_x, target_y):
        '''
        Moves the player to a new tile.
        '''
        success = self.move_entity_to(self.player, target_x, target_y)
        if (success and self.selection is not None):
            self.selection = (target_x + self.selection[0] - self.player.x, target_y + self.selection[1] - self.player.y, self.selection[2])
    
    def move_entity_to(self, user, target_x, target_y):
        '''
        Moves a given entity to a new tile.
        '''
        target_tile = self.map.get_tile(target_x, target_y);
        if (target_tile.entity is not None):
            self.log_message(user.name+" ["+str(user.get(properties.hp))+"] attacks "+target_tile.entity.name+" ["+str(target_tile.entity.get(properties.hp))+"]")
            self.do_update('log')
            return False
        else:
            self.map.get_tile(user.x, user.y).entity = None
            target_tile.entity = user
            user.x = target_x
            user.y = target_y
            
            self.do_update('cursor')
            self.do_update('entities')
            self.do_update('tiles')
            self.do_update('shadows')
            return True
    
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
        
    def end_player_turn(self, duration):
        '''
        Ends the current player's turn, and begins execution of the turn queue.
        :param duration: the time until this player can act again.
        '''
        self.schedule_turn(duration, player.Player.TURN) # TODO: test code
        self.execute_turn_queue()
        
    def schedule_turn(self, delay, action):
        '''
        Schedules an action to occur in the turn_queue
        '''
        delay += self.current_turn
        heapq.heappush(self.turn_queue, (delay, action))
        
    def execute_turn_queue(self):
        '''
        Cycles through the turn queue, executing each turn, 
        until it reaches another player turn.
        '''
        start = self.current_turn
        self.accept_input = False
        clock.schedule_once(self.cycle_turn_queue, 0.01)
        self.log_message("Executed turns from "+str(start)+" to "+str(self.current_turn))
        
    def cycle_turn_queue(self, dt):
        '''
        Recursively resolves every turn in the turn queue.
        '''
        turn = heapq.heappop(self.turn_queue)
        self.current_turn = turn[0]
        action = turn[1]
        if (hasattr(action, '__call__')):
            duration = action(self)
            self.schedule_turn(delay=duration, action=action)
            self.cycle_turn_queue(0)
            #clock.schedule_once(self.cycle_turn_queue, 0.001)
        else:
            self.accept_input = True
            self.log_message("Awaiting user input...")
            self.do_update('log')
            return; # Wait for user input.

Game.register_event_type('display')
Game.register_event_type('update')