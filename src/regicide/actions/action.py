'''
Created on Apr 27, 2013

@author: Devindra
'''

class Action(object):
    TARGET_SELF = 0
    TARGET_ENTITY = 1
    TARGET_ITEM = 2
    TARGET_TILE = 4

    def __init__(self, name, description, targets, tags=[], fatigue=1, time=100):
        '''
        Constructor
        '''
        self.name = name
        self.description = description
        self.targets = targets
        self.tags = tags
        self.fatigue = fatigue
        self.time = time
        
    def get_fatigue_cost(self):
        return self.fatigue
        
    def get_time_cost(self):
        return self.time
        
    def execute(self):
        pass
    
class ActionInstance(object):
    
    def __init__(self, source, action):
        self.source = source
        self.type = action
        self.power = 1
        self.fatigue = action.get_fatigue_cost()
        self.time = action.get_time_cost()
        
    def execute(self, game, *args):
        self.source.dispatch_event('on_action', self)
        self.type.execute(game, self.source, self.power, *args)
        
    