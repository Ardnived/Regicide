'''
Created on Mar 4, 2013

@author: Devindra

This class is the controller in the pseudo model-view-controller pattern used by this game.
'''
from pyglet import event
from regicide.controller.commands import KeyBinding
from regicide.mvc import State

class Controller(event.EventDispatcher):
    '''
    Handles all user input for the game.
    '''
    
    def __init__(self, model):
        '''
        Constructor
        '''
        self.model = model
    
    def on_key_press(self, symbol, modifiers):
        self.trigger_command(symbol, KeyBinding.TYPE_KEY)
    
    def on_text_motion(self, motion):
        self.trigger_command(motion, KeyBinding.TYPE_MOTION)
    
    def on_text(self, text):
        self.trigger_command(text, KeyBinding.TYPE_REPEAT)
    
    def trigger_command(self, key, key_type):
        command = State.commands().get_action(key, key_type)
        
        if (command is not None):
            self.dispatch_event('activate_command', command)
    
    def on_mouse_motion(self, x, y, dx, dy):
        for hotspot in State.view().hotspots:
            target = hotspot.get_tile(x, y)
            if (target is not None):
                self.dispatch_event('on_mouse_hover', hotspot, *target)
                return
        
        self.dispatch_event('on_mouse_hover', None)
        
    def on_mouse_press(self, x, y, button, modifiers):
        for hotspot in State.view().hotspots:
            target = hotspot.get_tile(x, y)
            if (target is not None):
                self.dispatch_event('on_hotspot_click', hotspot, target[0], target[1], button, modifiers)
         
    def on_mouse_release(self, x, y, button, modifiers):
        pass
    
Controller.register_event_type('activate_command')
Controller.register_event_type('on_mouse_hover')
Controller.register_event_type('on_hotspot_click')