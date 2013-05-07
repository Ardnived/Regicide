'''
Created on Apr 27, 2013

@author: Devindra
'''
import sys
from regicide.level import tile

class Action(object):
    
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
        
    def get_fatigue_cost(self):
        return self.fatigue
        
    def get_time_cost(self):
        return self.time
        
    def execute(self):
        pass
    
class ActionInstance(object):
    
    def __init__(self, source, action, target=None, **args):
        if target is None and action.targets == [tile.TARGET_SELF]:
            target = source
        
        self.source = source
        self.type = action
        self.power = 1
        self.fatigue = action.get_fatigue_cost()
        self.time = action.get_time_cost()
        self.target = target
        self.args = args
        
    def execute(self, game):
        self.source.dispatch_event('on_action', self)
        self.type.execute(game, self.source, self.power, self.target, **self.args)
        game.do_update('all')
        
    