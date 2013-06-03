'''
Created on Mar 2, 2013

@author: Devindra
'''
import random
from pyglet import sprite
from regicide.mvc import State
from regicide.resources import visual

class Tile(object):
    '''
    A tile for use in a TileMap
    '''
    WIDTH = 20
    HEIGHT = WIDTH
    
    TARGET_SELF     = 'self'
    TARGET_ENTITY   = 'entity'
    TARGET_ITEM     = 'item'
    TARGET_PASSABLE = 'passable'
    TARGET_DOOR     = 'door'
    TARGET_FLOOR    = 'floor'
    TARGET_ROUGH    = 'rough'
    TARGET_WALL     = 'wall'
    TARGET_OPAQUE   = 'opaque'
    
    def __init__(self, template=None, room=None):
        '''
        Constructor
        '''
        self.template = template #TODO: remove this, it's for testing.
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
        
        self.init(**template['params'])
        
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
        return Tile.TARGET_PASSABLE in self.type
        
    def is_opaque(self):
        '''
        Returns whether this tile can be entered by an entity.
        '''
        return Tile.TARGET_OPAQUE in self.type
    
    def is_unoccupied(self):
        '''
        Returns whether this tile is passable and unoccupied
        '''
        return self.is_passable() and self.entity is None
    
    def get_target_types(self):
        target_types = set(self.type)
        
        if self.entity is not None:
            target_types.add(Tile.TARGET_ENTITY)
            
            if State.model() is not None and self.entity == State.model().current_entity:
                target_types.add(Tile.TARGET_SELF)
        
        if self.items != []:
            target_types.add(Tile.TARGET_ITEM)
        
        return target_types
    
    def init(self, **args):
        pass
    
    def on_enter(self, game):
        pass
        
class Stair(Tile):
    
    def init(self, up):
        self.up = up
        
    #event
    def on_enter(self, game):
        print(self.entity.name+" entered "+str(self))
        Tile.on_enter(self, game)
        
        if self.entity == game.player:
            x, y, z = game.current_floor_coords
            
            if self.up == True:
                game.current_floor = (x, y, z+1)
            else:
                game.current_floor = (x, y, z-1)
        
class Gate(Tile):
    
    def init(self, direction):
        self.direction = direction
        
    #event
    def on_enter(self, game):
        Tile.on_enter(self, game)
        
        if self.entity == game.player:
            x, y, z = game.current_floor_coords
            
            game.current_floor = (x + self.direction.x_offset, y + self.direction.y_offset, z + self.direction.z_offset)
            
            target_x = game.player.x
            target_y = game.player.y
            
            if self.direction.x > 0:
                target_x = game.current_floor.map.extended_width - 1
            elif self.direction.x < 0:
                target_x = 0
            
            if self.direction.y > 0:
                target_y = game.current_floor.map.extended_height - 1
            elif self.direction.y < 0:
                target_y = 0
                
            game.move_entity(game.player, (target_x, target_y), events=False)
    
        
        
        