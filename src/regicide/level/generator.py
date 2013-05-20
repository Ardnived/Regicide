'''
Created on Mar 9, 2013

@author: Devindra

Contains code for generating the game's levels.
'''
import random
import math
from random import randint
from regicide.entity.npc import NPC
from regicide import data
from regicide.level.map import TileMap
from regicide.level.tile import Tile
from regicide.level.room import Room
from regicide.data.blueprints import Blueprint

class MapGenerator(object):
    '''
    Defines code for generating levels based on a few parameters.
    '''
    GUTTER = 5 # The number of tiles that a room can spill over the level's width and height.

    def __init__(self, width=0, height=0, zone="castle", floor="commons"):
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
        
        self.room_quantity = ((self.width + self.height)/2)/1
        self.guard_quantity = ((self.width + self.height)/2)/3
        
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
            x, y = self.random_location(Tile.WALL)
            
            if self.grid[x-1][y] is None and self.grid[x+1][y] == Tile.FLOOR:
                facing = "west"
                origin_room = self.room_grid[x+1][y]
            elif self.grid[x-1][y] == Tile.FLOOR and self.grid[x+1][y] is None:
                facing = "east"
                origin_room = self.room_grid[x-1][y]
            elif self.grid[x][y-1] is None and self.grid[x][y+1] == Tile.FLOOR:
                facing = "south"
                origin_room = self.room_grid[x][y+1]
            elif self.grid[x][y-1] == Tile.FLOOR and self.grid[x][y+1] is None:
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
                self.grid[x][y] = Tile.WALL
        
        for x in xrange(origin_x, origin_x + room.width):
            self.grid[x][origin_y-1] = Tile.WALL
            self.grid[x][origin_y + room.height] = Tile.WALL
            for y in xrange(origin_y, origin_y + room.height):
                self.grid[x][y] = Tile.FLOOR
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
                    tile = Tile(tile, self.room_grid[x][y])
                
                if tile is not None:
                    tile.room = self.room_grid[x][y]
                
                tile_map.grid[x].append(tile)
        
        return tile_map
    
    def decorate_rooms(self, tile_map):
        for room, location in self.rooms.iteritems():
            room.decorate(tile_map, *location)

    def generate(self):
        print("Creating "+str(self.room_quantity)+" rooms and "+str(self.guard_quantity)+" guards in a "+str(self.extended_width)+"x"+str(self.extended_height)+" area.")
        self.prepare()

class CastleGenerator(MapGenerator):

    def generate(self):
        MapGenerator.generate(self)
        
        print("Creating 3 stairwells.")
        self.create_stairwells(3)
        print("Creating "+str(self.room_quantity)+" rooms.")
        self.create_rooms(self.room_quantity)
        
        print("Decoding map.")
        tile_map = self.decode_map()
        print("Decorating rooms.")
        self.decorate_rooms(tile_map)
        print("Creating passages.")
        self.create_passages(tile_map, random.randint(3, 7))
        
        self.clean()
        return tile_map
    
    def create_stairwells(self, quantity):
        for _ in xrange(quantity):
            room = self.create_room(["stairwell"])
            location = self.random_location(None, room.width, room.height)
            x, y = location
            
            while not self.rect_is_empty(x, y, x + room.width, y + room.height):
                location = self.random_location(None, room.width, room.height)
                x, y = location
                
            self.place_room(room, x, y)
            self.grid[x][y] = Tile.STAIRS_UP # TODO: What about down stairs?
            
    def create_rooms(self, quantity):
        placed_count = 0
        
        while placed_count < quantity:
            room = None
            while room is None:
                pivot_x, pivot_y, facing, origin_room = self.pick_room_pivot()
                room = self.create_room(origin_room.connection_types)
            
            if facing == "north" or facing == "south":
                if facing == "north":
                    y = pivot_y + 1
                else:
                    y = pivot_y - room.height
                
                i = 0
                x = pivot_x - randint(0, room.width-1)
                while i < room.width:
                    x = pivot_x - randint(0, room.width-1)
                    if self.rect_is_empty(x, y, x + room.width, y + room.height):
                        break
                    else:
                        i += 1
                else:
                    continue # Can't fit this room here.
                
            elif facing == "east" or facing == "west":
                if facing == "east":
                    x = pivot_x + 1
                else:
                    x = pivot_x - room.width
                
                i = 0
                y = pivot_y - randint(0, room.height-1)
                while i < room.height:
                    y = pivot_y - randint(0, room.height-1)
                    if self.rect_is_empty(x, y, x + room.width, y + room.height):
                        break
                    else:
                        i += 1
                else:
                    continue # Can't fit this room here.
            
            self.place_room(room, x, y)
            origin_room.add_connection(x, y, room)
            room.add_connection(x, y, origin_room)
            self.grid[pivot_x][pivot_y] = Tile.DOOR
            placed_count += 1
        
    def create_passages(self, tile_map, quantity):
        placed_count = 0
        
        max_attempts = quantity * 2
        attempts = 0
        
        while placed_count < quantity and attempts < max_attempts:
            origin_room, location = random.choice(self.rooms.items())
            origin_x, origin_y = location
            
            if origin_room.allow_passages is False:
                continue
            
            target_room = random.choice(self.rooms.keys())
            while target_room == origin_room or target_room.allow_passages is False:
                target_room = random.choice(self.rooms.keys())
            
            target_x, target_y = self.rooms[target_room]
            distance = math.sqrt(abs((target_x - origin_x)**2 + (target_y - origin_y)**2))
                
            if distance > 7: # Don't choose rooms which are too close together.
                walls = origin_room.get_available_walls(tile_map, origin_x, origin_y, interior=False)
                if len(walls) < 1:
                    continue
                else:
                    origin_x, origin_y = random.choice(walls)
                    
                walls = target_room.get_available_walls(tile_map, target_x, target_y, interior=False)
                if len(walls) < 1:
                    continue
                else:
                    target_x, target_y = random.choice(walls)
                
                path = tile_map.find_path(tile_map.ALGORITHM_ASTAR_PASSAGE, origin_x, origin_y, target_x, target_y)
                if path is None:
                    continue
                else:
                    tile_map.grid[origin_x][origin_y] = Tile(Tile.SECRET_DOOR)
                    tile_map.grid[target_x][target_y] = Tile(Tile.SECRET_DOOR)
                    for x, y in path:
                        adjacent = [
                            (x+1, y),
                            (x-1, y),
                            (x, y+1),
                            (x, y-1),
                            (x+1, y+1),
                            (x-1, y+1),
                            (x+1, y-1),
                            (x-1, y-1),
                        ]
                        tile_map.grid[x][y] = Tile(Tile.FLOOR)
                        
                        for adj_x, adj_y in adjacent:
                            if tile_map.get_tile(adj_x, adj_y) is None:
                                tile_map.grid[adj_x][adj_y] = Tile(Tile.WALL)
                
                placed_count += 1
                
            attempts += 1
        
        print(str(placed_count)+" passages were created.")
                

class DungeonGenerator(MapGenerator):

    def generate(self):
        MapGenerator.generate(self)
        
        return self.decode_map()

class CaveGenerator(MapGenerator):

    def generate(self):
        MapGenerator.generate(self)
        
        return self.decode_map()
