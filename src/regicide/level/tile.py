'''
Created on Mar 2, 2013

@author: Devindra
'''
import random
from pyglet import sprite
from regicide.resources import visual

class Tile(object):
    '''
    A tile for use in a TileMap
    '''
    WIDTH = 20
    HEIGHT = WIDTH
    
    FLOOR = {
        'sprites' : [visual.Tile.BLOCK, visual.Tile.BLOCK, visual.Tile.BLOCK_CRACKED],
        'ascii'   : visual.ASCII.get_index(13, 13),
        'type'    : 'ground'
    }
    
    STAIRS_UP = {
        'sprites' : [visual.Tile.STAIRS_UP],
        'ascii'   : visual.ASCII.get_index(4, 13),
        'type'    : 'ground'
    }
    
    STAIRS_DOWN = {
        'sprites' : [visual.Tile.STAIRS_DOWN],
        'ascii'   : visual.ASCII.get_index(4, 13),
        'type'    : 'ground'
    }
    
    WALL = {
        'sprites' : [visual.Tile.PLINTH_LIGHT],
        'ascii'   : visual.ASCII.get_index(2, 13),
        'type'    : 'wall'
    }
    
    DOOR = {
        'sprites' : [visual.Tile.GATE_1, visual.Tile.GATE_2, visual.Tile.GATE_3],
        'ascii'   : visual.ASCII.get_index(15, 9),
        'type'    : 'ground'
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
        return self.type == 'ground' or self.type == 'liquid'
    
    def is_unoccupied(self):
        '''
        Returns whether this tile is passable and unoccupied
        '''
        return self.is_passable() and self.entity is None
        
        