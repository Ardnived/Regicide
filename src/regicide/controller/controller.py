'''
Created on Mar 4, 2013

@author: Devindra

This class is the controller in the pseudo model-view-controller pattern used by this game.
'''
from pyglet import event
from pyglet.window import key
from regicide.controller.commands import KeyBinding
from regicide.mvc import State

class Controller(event.EventDispatcher):
    '''
    Handles all user input for the game.
    '''
    
    #event
    def on_key_press(self, symbol, modifiers):
        '''
        An event intended to be triggered by the window object.
        Triggers every time the user pressed a key.
        '''
        self.trigger_command(symbol, KeyBinding.TYPE_KEY)
        
        if symbol == key.ESCAPE:
            return event.EVENT_HANDLED
    
    def on_text_motion(self, motion):
        '''
        An event intended to be triggered by the window object.
        Triggers every time the user uses a text motion (such as the arrow keys).
        '''
        self.trigger_command(motion, KeyBinding.TYPE_MOTION)
    
    def on_text(self, text):
        '''
        An event intended to be triggered by the window object.
        Triggers every time the user types a letter.
        We use it to check for keys that are held, as they will trigger this function continuously.
        '''
        self.trigger_command(text, KeyBinding.TYPE_REPEAT)
    
    def trigger_command(self, key, key_type):
        '''
        A key has been pressed. Check if it is mapped to a command, 
        and send the command activation event if so.
        '''
        command = State.commands().get_action(key, key_type)
        
        if command is not None:
            self.dispatch_event('activate_command', command)
    
    def on_mouse_motion(self, x, y, dx, dy):
        '''
        An event intended to be triggered by the window object.
        Triggers every time the user moves the mouse.
        '''
        for hotspot in State.view().hotspots:
            if hotspot.contains(x, y):
                self.dispatch_event('on_mouse_hover', hotspot, x, y)
                return
        
        # If the mouse is not over any hotspot, send an event to clear the hotspots.
        self.dispatch_event('on_mouse_hover', None)
        
    def on_mouse_press(self, x, y, button, modifiers):
        '''
        An event intended to be triggered by the window object.
        Triggers every time the user moves the mouse.
        '''
        for hotspot in State.view().hotspots:
            if hotspot.contains(x, y):
                self.dispatch_event('on_hotspot_click', hotspot, button, modifiers)
         
    def on_mouse_release(self, x, y, button, modifiers):
        '''
        An event intended to be triggered by the window object.
        Triggers every time the user moves the mouse.
        '''
        pass

Controller.register_event_type('activate_command')
Controller.register_event_type('on_mouse_hover')
Controller.register_event_type('on_hotspot_click')