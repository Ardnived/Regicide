'''
Created on Mar 9, 2013

@author: Devindra

Contains code for generating the game's levels.
'''
import random
from random import randint
from regicide.data import tiles
from regicide.level.map import TileMap
from regicide.level.room import Room
from regicide.data.blueprints import Blueprint

class MapGenerator(object):
    '''
    Defines code for generating levels based on a few parameters.
    '''
    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 100
    GUTTER = 5 # The number of tiles that a room can spill over the level's width and height.

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, zone="castle", floor="commons"):
        '''
        :param zone: the area in which this level exists, restricts room types.
        :param floor: the specific type of level to generate, restricts room types.
        '''
        self.extended_width = width+(MapGenerator.GUTTER*2)
        self.extended_height = height+(MapGenerator.GUTTER*2)
        
        self.min_x = MapGenerator.GUTTER
        self.min_y = MapGenerator.GUTTER
        self.max_x = self.extended_width - MapGenerator.GUTTER
        self.max_y = self.extended_height - MapGenerator.GUTTER
        self.width = width
        self.height = height
        
        self.room_quantity = ((self.width + self.height)/2)*2
        
        self.zone = zone
        self.floor = floor
        
        self.clean()
        
    def clean(self):
        self.grid = []
        self.room_grid = []
        self.rooms = {}
    
    def prepare(self):
        for x in range(self.extended_width):
            self.grid.append([])
            self.room_grid.append([])
            for _ in range(self.extended_height):
                self.grid[x].append(None)
                self.room_grid[x].append(None)
    
    def random_location(self, tile_type = None, buffer_x = 0, buffer_y = 0):
        x = self.min_x + randint(0, self.width - buffer_x)
        y = self.min_y + randint(0, self.height - buffer_y)

        if tile_type is not None:
            while self.grid[x][y] != tile_type:
                x = self.min_x + randint(0, self.width - buffer_x)
                y = self.min_y + randint(0, self.height - buffer_y)
        
        return (x, y)
    
    def rect_is_empty(self, x1, y1, x2, y2):
        '''
        Returns whether a specific area of the map is empty.
        '''
        if x1 < 1 or y1 < 1 or x2 > self.extended_width-1 or y2 > self.extended_height-1:
            return False
        
        for x in xrange(x1, x2):
            for y in xrange(y1, y2):
                if self.grid[x][y] is not None:
                    return False
        
        return True
    
    def pick_room_pivot(self):
        '''
        Returns a random pivot chosen from across the map.
        '''
        while True:
            x, y = self.random_location(tiles.WALL)
            
            if self.grid[x-1][y] is None and self.grid[x+1][y] == tiles.FLOOR:
                facing = "west"
                origin_room = self.room_grid[x+1][y]
            elif self.grid[x-1][y] == tiles.FLOOR and self.grid[x+1][y] is None:
                facing = "east"
                origin_room = self.room_grid[x-1][y]
            elif self.grid[x][y-1] is None and self.grid[x][y+1] == tiles.FLOOR:
                facing = "south"
                origin_room = self.room_grid[x][y+1]
            elif self.grid[x][y-1] == tiles.FLOOR and self.grid[x][y+1] is None:
                facing = "north"
                origin_room = self.room_grid[x][y-1]
            else:
                continue
            
            if origin_room.count_connections() >= origin_room.max_connections:
                continue
            
            return [x, y, facing, origin_room]
    
    def place_room(self, room, origin_x, origin_y):
        '''
        Creates a room at the specified origin.
        This method should first be checked with the rect_is_empty function.
        '''
        
        for x in [origin_x - 1, origin_x + room.width]:
            for y in xrange(origin_y - 1, origin_y + room.height + 1):
                self.grid[x][y] = tiles.WALL
        
        for x in xrange(origin_x, origin_x + room.width):
            self.grid[x][origin_y-1] = tiles.WALL
            self.grid[x][origin_y + room.height] = tiles.WALL
            for y in xrange(origin_y, origin_y + room.height):
                self.grid[x][y] = tiles.FLOOR
                self.room_grid[x][y] = room
                
        x = origin_x + (room.width / 2)
        y = origin_y + (room.height / 2)
        
        self.rooms[room] = (origin_x, origin_y)
    
    def create_room(self, domains):
        '''
        Chooses a room with the given domains.
        '''
        rooms = []
        for domain in domains:
            rooms.extend(Blueprint.find_blueprints(type=domain, zone=self.zone, floor=self.floor))
        
        if len(rooms) != 0:
            return Room(random.choice(rooms).master())
        
    def decode_map(self):
        tile_map = TileMap(self.extended_width, self.extended_height)
        
        for x in xrange(self.extended_width):
            tile_map.grid.append([])
            for y in xrange(self.extended_height):
                tile = self.grid[x][y]
                if tile == None:
                    tile = None
                else:
                    cls = tile['class']
                    tile = cls(tile, self.room_grid[x][y])
                
                if tile is not None:
                    tile.room = self.room_grid[x][y]
                
                tile_map.grid[x].append(tile)
        
        return tile_map
    
    def decorate_rooms(self, tile_map):
        for room, location in self.rooms.iteritems():
            room.decorate(tile_map, *location)

    def generate(self, options):
        print(" === "+self.__class__.__name__+" === ")
        print("Creating "+str(self.room_quantity)+" rooms in a "+str(self.extended_width)+"x"+str(self.extended_height)+" area.")
        self.prepare()

