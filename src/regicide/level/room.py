'''
Created on 2013-05-16

@author: Devindra
'''
import random
from regicide import data
from regicide.level.tile import Tile
from regicide.entity.npc import NPC
from regicide.data import tiles
from regicide.data.blueprints import Blueprint

class Room(object):

    def __init__(self, template):
        '''
        Constructor
        '''
        self.name = template.properties['name']
        self.max_connections = template.properties['max_connections']
        
        self.connection_types = template.properties['connections']
        if type(self.connection_types) != list:
            self.connection_types = [self.connection_types]
        
        if template.properties.has_key('add_doors'):
            self.additional_door_types = template.properties['add_doors']
        else:
            self.additional_door_types = []
        
        if template.properties.has_key('guards'):
            self.guards = template.properties['guards']
        else:
            self.guards = []
        
        self.allow_passages = template.properties['allow_passages']
        
        self.width = template.properties['width']
        self.height = template.properties['height']
        
        self._connection_count = 0
        self.connections = {}
    
    def add_connection(self, x, y, room):
        if not self.connections.has_key(room):
            self.connections[room] = []
        
        self.connections[room].append((x, y))
        self._connection_count += 1
        
    def count_connections(self, room=None):
        if room is None:
            return self._connection_count
        elif self.connections.has_key(room):
            return len(self.connections[room])
        else:
            return 0
    
    def decorate(self, tile_map, origin_x, origin_y):
        wall_list = self.get_available_walls(tile_map, origin_x, origin_y, interior=True)
        
        max_tries = len(wall_list)
        n = 0
        while self.count_connections() < self.max_connections and n < max_tries and len(wall_list) > 0:
            location, room = random.choice(wall_list.items())
            x, y = location
            
            if room.count_connections() < room.max_connections:
                tile_map.grid[x][y] = Tile(tiles.DOOR)
                self.add_connection(x, y, room)
                room.add_connection(x, y, self)
                wall_list.pop(location)
            
            n += 1
        
        if self.guards != []:
            guard_quantity = random.randint(0, max(1, (self.width + self.height)/2/2))
            #blueprints = Blueprint.find_blueprints(*self.guards)
            for _ in xrange(guard_quantity):
                blueprint = data.units.GOBLIN #random.choice(blueprints)
                x = random.randint(origin_x, origin_x + self.width - 2)
                y = random.randint(origin_y, origin_y + self.height - 2)
                tile = tile_map.get_tile(x, y)
                
                while not tile.is_unoccupied:
                    x = random.randint(origin_x, origin_x + self.width - 2)
                    y = random.randint(origin_y, origin_y + self.height - 2)
                    tile = tile_map.get_tile(x, y)
                
                tile_map.get_tile(x, y).entity = NPC(blueprint.master(), x, y)
    
    def get_available_walls(self, tile_map, origin_x, origin_y, interior = True):
        if interior:
            wall_list = {}
        else:
            wall_list = []
        
        if interior:
            offset = 1
        else:
            offset = 0
        
        for y in xrange(self.height - 1 - offset):
            y += origin_y - 1 + offset
            for x in range(origin_x - 1, origin_x + self.width - 1 - offset):
                result = self._is_valid_door_location(tile_map, x, y, interior)
                if not interior and result is True:
                    wall_list.append((x, y))
                elif result is not None:
                    wall_list[(x, y)] = result
            
        for x in xrange(self.width - 1 - offset):
            x += origin_x - 1 + offset
            for y in range(origin_y - 1, origin_y + self.height - 1 - offset):
                result = self._is_valid_door_location(tile_map, x, y, interior)
                if not interior and result is True:
                    wall_list.append((x, y))
                elif result is not None:
                    wall_list[(x, y)] = result
        
        return wall_list
        
    def _is_valid_door_location(self, tile_map, x, y, interior):
        tile = tile_map.get_tile(x, y)
        if Tile.TARGET_WALL in tile.get_target_types():
            north = tile_map.get_tile(x, y+1)
            south = tile_map.get_tile(x, y-1)
            west = tile_map.get_tile(x-1, y)
            east = tile_map.get_tile(x+1, y)
            
            empty_tiles = [north, south, east, west].count(None)
            
            if interior:
                if empty_tiles > 0:
                    return None
                
                if (south is not None and Tile.TARGET_WALL in south.get_target_types() and 
                    north is not None and Tile.TARGET_WALL in north.get_target_types() and 
                    west is not None and Tile.TARGET_FLOOR in west.get_target_types() and 
                    east is not None and Tile.TARGET_FLOOR in east.get_target_types()):
                    
                    if west.room is not self:
                        return west.room
                    else:
                        return east.room
                if (west is not None and Tile.TARGET_WALL in west.get_target_types() and 
                    east is not None and Tile.TARGET_WALL in east.get_target_types() and 
                    south is not None and Tile.TARGET_FLOOR in south.get_target_types() and 
                    north is not None and Tile.TARGET_FLOOR in north.get_target_types()):
                    
                    if south.room is not self:
                        return south.room
                    else:
                        return north.room
                else:
                    return None
            else:
                if empty_tiles > 2 or empty_tiles < 1:
                    return None
                
                return True
                
    