'''
Created on Mar 24, 2013

@author: Devindra
'''
import abc
from random import randint
from regicide.entity.entity import Entity
from regicide.entity import actions

class NPC(Entity):
    '''
    A computer controlled entity.
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self, template, x=0, y=0):
        '''
        :param template: the blueprints.Master object to base this entity on.
        :param x: the initial x location on the map of this entity.
        :param x: the initial y location on the map of this entity.
        '''
        Entity.__init__(self, template=template, x=x, y=y)
    
    def on_turn(self, game):
        '''
        Executes this NPC's turn AI, and then returns the amount of time till it can act again.
        '''
        possible_moves = [
            (self.x+1, self.y),
            (self.x-1, self.y),
            (self.x, self.y+1),
            (self.x, self.y-1),
            (self.x+1, self.y+1),
            (self.x+1, self.y-1),
            (self.x-1, self.y+1),
            (self.x-1, self.y-1),
        ]
        target = possible_moves[randint(0, len(possible_moves)-1)]
        
        tile = game.map.get_tile(*target)
        if tile is not None and tile.is_passable():
            game.execute_action(actions.action.ActionInstance(
                source = self, 
                action = actions.misc.Move(), 
                target = target,
            ))
        
        game.end_turn(randint(60, 120))
    
