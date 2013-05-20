'''
Created on Mar 2, 2013

@author: Devindra
'''
import random
from pyglet import sprite
from regicide.resources import visual
from regicide.mvc import State

TARGET_SELF     = 'self'
TARGET_ENTITY   = 'entity'
TARGET_ITEM     = 'item'
TARGET_PASSABLE = 'passable'
TARGET_DOOR     = 'door'
TARGET_FLOOR    = 'floor'
TARGET_ROUGH    = 'rough'
TARGET_WALL     = 'wall'
TARGET_OPAQUE   = 'opaque'

class Tile(object):
    
    '''
    A tile for use in a TileMap
    '''
    WIDTH = 20
    HEIGHT = WIDTH
    
    FLOOR = {
        'sprites' : [visual.Tile.BLOCK, visual.Tile.BLOCK, visual.Tile.BLOCK_CRACKED],
        'ascii'   : visual.ASCII.get_index(13, 13), #(11, 3), #(13, 13),
        'type'    : [TARGET_FLOOR, TARGET_PASSABLE]
    }
    
    LIGHT = {
        'sprites' : [visual.Tile.PLINTH_EYE],
        'ascii'   : visual.ASCII.get_index(8, 9),
        'type'    : [TARGET_FLOOR, TARGET_PASSABLE]
    }
    
    STAIRS_UP = {
        'sprites' : [visual.Tile.STAIRS_UP],
        'ascii'   : visual.ASCII.get_index(12, 12),
        'type'    : [TARGET_ROUGH, TARGET_PASSABLE]
    }
    
    STAIRS_DOWN = {
        'sprites' : [visual.Tile.STAIRS_DOWN],
        'ascii'   : visual.ASCII.get_index(14, 12),
        'type'    : [TARGET_ROUGH, TARGET_PASSABLE]
    }
    
    WALL = {
        'sprites' : [visual.Tile.PLINTH_LIGHT],
        'ascii'   : visual.ASCII.get_index(7, 0),
        'type'    : [TARGET_WALL, TARGET_OPAQUE]
    }
    
    DOOR = {
        'sprites' : [visual.Tile.GATE_1, visual.Tile.GATE_2, visual.Tile.GATE_3],
        'ascii'   : visual.ASCII.get_index(10, 13),
        'type'    : [TARGET_DOOR, TARGET_PASSABLE]
    }
    
    SECRET_DOOR = {
        'sprites' : [visual.Tile.COLUMNS_GATE],
        'ascii'   : visual.ASCII.get_index(2, 13),
        'type'    : [TARGET_DOOR, TARGET_PASSABLE]
    }
    
    DECORATION = {
        'sprites' : [visual.Tile.TILES],
        'ascii'   : visual.ASCII.get_index(11, 13),
        'type'    : [TARGET_PASSABLE]
    }
    
    def __init__(self, template=None, room=None):
        '''
        Constructor
        '''
        if template is not None:
            image = template['sprites'][random.randint(0, len(template['sprites'])-1)]
            
            self.type = template['type']
            self.sprite = sprite.Sprite(visual.Tile.get(image))
            self.ascii = sprite.Sprite(visual.ASCII.get(template['ascii']))
        
        self.decoration = None
        self.entity = None
        self.room = None
        self.items = []
        self.explored = True # TODO: This should be False, but I'm testing things atm.
        self._shadow = 8
        
    @property
    def shadow(self):
        return max(0, min(self._shadow, 8))
    
    @shadow.setter
    def shadow(self, value):
        self._shadow = value
        
    def is_passable(self):
        '''
        Returns whether this tile can be entered by an entity.
        '''
        return TARGET_PASSABLE in self.type
        
    def is_opaque(self):
        '''
        Returns whether this tile can be entered by an entity.
        '''
        return TARGET_OPAQUE in self.type
    
    def is_unoccupied(self):
        '''
        Returns whether this tile is passable and unoccupied
        '''
        return self.is_passable() and self.entity is None
    
    def get_target_types(self):
        target_types = set(self.type)
        
        if self.entity is not None:
            target_types.add(TARGET_ENTITY)
            
            if State.model() is not None and self.entity == State.model().current_entity:
                target_types.add(TARGET_SELF)
        
        if self.items != []:
            target_types.add(TARGET_ITEM)
        
        return target_types
        
        
        
        
        