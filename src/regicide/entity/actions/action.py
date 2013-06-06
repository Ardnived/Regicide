'''
Created on Apr 27, 2013

@author: Devindra

Defines structure for actions that can be taken by entities in the game.
'''
import sys
from regicide.level.tile import Tile

class Action(object):
    '''
    The definition of an action.
    '''
    
    def __init__(self, name, description, targets, tags=[], fatigue=1, time=100, target_range=sys.maxint):
        '''
        Constructor
        '''
        self.name = name
        self.description = description
        self.targets = targets
        self.tags = tags
        self.fatigue = fatigue
        self.time = time
        self.range = target_range
    
    @property
    def fatigue_cost(self):
        return self.fatigue
    
    #property
    def time_cost(self):
        return self.time
        
    def execute(self):
        pass
    
class ActionInstance(object):
    '''
    Whenever an action is to be executed, it creates an instance of this class,
    where the properties of the action can be temporarily modified for this execution.
    '''
    
    def __init__(self, source, action, target=None, **args):
        if target is None and action.targets == [Tile.TARGET_SELF]:
            target = source
        
        self.source = source
        self.type = action
        self.power = 1
        self.fatigue = action.fatigue_cost
        self.time = action.time_cost
        self.target = target
        self.args = args
        
    def execute(self, game):
        '''
        Execute the action.
        '''
        self.source.dispatch_event('on_action', self)
        self.type.execute(game, self.source, self.power, self.target, **self.args)
        game.do_update('all')
        
    