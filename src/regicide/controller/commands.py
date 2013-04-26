'''
Created on Apr 6, 2013

@author: Devindra
'''
from pyglet.window import key

class CommandSet(object):
    def __init__(self, binders={}):
        self._bindings = {
            KeyBinding.TYPE_KEY: {},
            KeyBinding.TYPE_MOTION: {},
            KeyBinding.TYPE_REPEAT: {},
        }
        
        self.binders = {}
        
        for key, binder in binders.iteritems():
            self.add(key, binder)
        
    def get_action(self, command_key, key_type):
        if (self._bindings[key_type].has_key(command_key)):
            return self._bindings[key_type][command_key]
        else:
            return None
    
    def get(self, key):
        return self.binders[key]
    
    def add(self, key, binder):
        for binding in binder.bindings:
            self._bindings[binding.type][binding.key] = binder
        
        self.binders[key] = binder
        
    def remove(self, key):
        for binding in self.binders[key].bindings:
            self._bindings[binding.type][binding.key] = None
        
        self.binders[key] = None

class KeyBinder(object):
    def __init__(self, bindings=[], action=None):
        self.bindings = bindings
        self.action = action
    
class KeyBinding(object):
    TYPE_KEY = 0
    TYPE_MOTION = 1
    TYPE_REPEAT = 2
    
    def __init__(self, key, command_type=TYPE_KEY):
        self.key = key
        self.type = command_type
