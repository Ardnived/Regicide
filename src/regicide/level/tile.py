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

class Tile(object):
    
    '''
    A tile for use in a TileMap
    '''
    WIDTH = 20
    HEIGHT = WIDTH
    
    FLOOR = {
        'sprites' : [visual.Tile.BLOCK, visual.Tile.BLOCK, visual.Tile.BLOCK_CRACKED],
        'ascii'   : visual.ASCII.get_index(13, 13),
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
        'type'    : [TARGET_WALL]
    }
    
    DOOR = {
        'sprites' : [visual.Tile.GATE_1, visual.Tile.GATE_2, visual.Tile.GATE_3],
        'ascii'   : visual.ASCII.get_index(10, 13),
        'type'    : [TARGET_DOOR, TARGET_PASSABLE]
    }
    
    def __init__(self, template=None):
        '''
        Constructor
        '''
        if (template is not None):
            image = template['sprites'][random.randint(0, len(template['sprites'])-1)]
            
            self.type = template['type']
            self.sprite = sprite.Sprite(visual.Tile.get(image))
            self.ascii = sprite.Sprite(visual.ASCII.get(template['ascii']))
        
        self.no_shadow = True
        self.shadow = sprite.Sprite(visual.Tile.get(visual.Tile.SHADE_1))
        self.decoration = None
        self.entity = None
        self.items = []
        
    def is_passable(self):
        '''
        Returns whether this tile can be entered by an entity.
        '''
        return TARGET_PASSABLE in self.type
    
    def is_unoccupied(self):
        '''
        Returns whether this tile is passable and unoccupied
        '''
        return self.is_passable() and self.entity is None
    
    def get_target_types(self):
        target_types = set(self.type)
        
        if self.entity is not None:
            print('add entity')
            target_types.add(TARGET_ENTITY)
            
            if self.entity == State.model().current_entity:
                target_types.add(TARGET_SELF)
        
        if self.items != []:
            target_types.add(TARGET_ITEM)
        
        return target_types
        
        
        
        
        