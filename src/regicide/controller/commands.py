'''
Created on Apr 6, 2013

@author: Devindra

This file defines the structure for how controls are defined,
using CommandSets which are a collection of KeyBinders
where as KeyBinders are a collection fo KeyBindings
'''
from pyglet.window import key

class CommandSet(object):
    '''
    A command set is a collection of commands defined as KeyBinders
    '''
    
    def __init__(self, binders={}):
        '''
        Constructor, takes a set of bindings to be included in this command set.
        
        :param binders: the initial commands in this set.
        '''
        self._bindings = {
            KeyBinding.TYPE_KEY: {},
            KeyBinding.TYPE_MOTION: {},
            KeyBinding.TYPE_REPEAT: {},
        }
        
        self.binders = {}
        
        for key, binder in binders.iteritems():
            self.add(key, binder)
        
    def get_action(self, command_key, key_type):
        '''
        Get's the action for a given key press.
        
        :param command_key: the key that was pressed
        :param key_type: the type of key that was pressed. Can be one of KeyBinding.TYPE_KEY, TYPE_MOTION, or TYPE_REPEAT
        '''
        if self._bindings[key_type].has_key(command_key):
            return self._bindings[key_type][command_key]
        else:
            return None
    
    def get(self, key):
        '''
        Get a command as a KeyBinder object.
        '''
        return self.binders[key]
    
    def add(self, key, binder):
        '''
        Adds a set of bindings
        
        :param key: the string that represents this command
        :param binder: a KeyBinder that includes all the KeyBindings and the action for this command.
        '''
        for binding in binder.bindings:
            self._bindings[binding.type][binding.key] = binder
        
        self.binders[key] = binder
        
    def remove(self, key):
        '''
        Remove a command and all it's bindings from the set.
        
        :param key: the string that identifies the command to be removed
        '''
        for binding in self.binders[key].bindings:
            self._bindings[binding.type][binding.key] = None
        
        self.binders[key] = None

class KeyBinder(object):
    '''
    A set of key bindings and the action that they map to.
    '''
    
    def __init__(self, bindings=[], action=None):
        '''
        Constructor
        
        :param bindings: the key bindings for this command
        :param action: the function that executes when this action is triggered
        '''
        self.bindings = bindings
        self.action = action
    
class KeyBinding(object):
    '''
    A pair of a key index, and the type of key press to trigger it on.
    '''
    TYPE_KEY = 0 # This is used for standard single key presses.
    TYPE_MOTION = 1 # This is used for text editor motions. Specifically the arrow keys.
    TYPE_REPEAT = 2 # Used for bindings that should trigger repeatedly when the key is held.
    
    def __init__(self, key, command_type=TYPE_KEY):
        '''
        Constructor
        
        :param key: the index value of the key, as defined by the pyglet library.
        :param command_type: can be TYPE_KEY, TYPE_MOTION, or TYPE_REPEAT
        '''
        self.key = key
        self.type = command_type
