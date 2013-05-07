'''
Created on Mar 9, 2013

@author: Devindra

Contains code for generating the game's levels.
'''
from random import randint
from regicide.entity.npc import NPC
from regicide import data
from regicide.level.map import TileMap
from regicide.level.tile import Tile
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
        
        self.room_quantity = ((self.width + self.height)/2)/2
        self.guard_quantity = ((self.width + self.height)/2)/3
        
        self.zone = zone
        self.floor = floor
        self.room_grid = []
        self.grid = []
        
        for x in range(self.extended_width):
            self.grid.append([])
            self.room_grid.append([])
            for y in range(self.extended_height):
                self.grid[x].append(" ")
                self.room_grid[x].append(None)
         
    def generate(self):
        '''
        Generate a level based on this generator's parameters.
        '''
        tile_map = TileMap(self.extended_width, self.extended_height)
        
        print("Creating "+str(self.room_quantity)+" rooms and "+str(self.guard_quantity)+" guards in a "+str(self.extended_width)+"x"+str(self.extended_height)+" area.")
        
        rooms = Blueprint.find_blueprints(type="stairwell", zone=self.zone, floor=self.floor)
        room = rooms[randint(0, len(rooms)-1)].master()
        
        x = self.min_x + randint((self.width*1/4), (self.width*3/4) - room.properties['width'])
        y = self.min_y + randint((self.height*1/4), (self.height*3/4) - room.properties['height'])
        
        self.place_room(room, x, y)
        self.grid[x][y] = "%"
        for i in range(0, int(self.room_quantity)):
            while not self.generate_room():
                pass
        
        for i in range(0, int(self.room_quantity / 6)):
            while not self.generate_door():
                pass
        
        for x in range(self.extended_width):
            tile_map.grid.append([])
            for y in range(self.extended_height):
                tile = self.grid[x][y]
                if (tile == "#"):
                    tile = Tile(Tile.WALL)
                elif (tile == " "):
                    tile = None
                elif (tile == "%"):
                    tile = Tile(Tile.STAIRS_UP)
                elif (tile == "^"):
                    tile = Tile(Tile.DOOR)
                else:
                    tile = Tile(Tile.FLOOR)
                
                tile_map.grid[x].append(tile)
        
        for i in range(0, int(self.guard_quantity)):
            tile = None
            while (tile is None or not tile.is_passable()):
                location = [randint(0, self.extended_width), randint(0, self.extended_height)]
                tile = tile_map.get_tile(*location)
            
            tile.entity = NPC(data.units.GOBLIN.master(), *location)
        
        tile_map.room_grid = self.room_grid
        
        return tile_map
    
    def generate_room(self):
        '''
        Find a location for and create a new room.
        Returns success or failure.
        '''
        pivot = None
        while pivot is None:
            pivot = self.pick_room_pivot()
            
        return self.try_room(*pivot)
        
    def try_room(self, pivot_x, pivot_y, facing, origin_room):
        '''
        Tries to branch a room off of a given pivot.
        '''
        connections = origin_room.properties['connections']
        if (type(connections) != list):
            connections = [connections]
        
        room = self.choose_room(connections)
        
        if (room is None):
            self.generate_room()
            return;
        
        room_width = room.properties['width']
        room_height = room.properties['height']
        
        if (facing == "north" or facing == "south"):
            if (facing == "north"):
                y = pivot_y + 1
            else:
                y = pivot_y - room_height
            
            i = 0
            x = pivot_x - randint(0, room_width-1)
            while not self.rect_is_empty(x, y, x + room_width, y + room_height):
                if (i > room_width):
                    return False
                else:
                    x = pivot_x - randint(0, room_width-1)
                    i += 1
            
        elif (facing == "east" or facing == "west"):
            if (facing == "east"):
                x = pivot_x + 1
            else:
                x = pivot_x - room_width
            
            i = 0
            y = pivot_y - randint(0, room_height-1)
            while not self.rect_is_empty(x, y, x + room_width, y + room_height):
                if (i > room_height):
                    return False
                else:
                    y = pivot_y - randint(0, room_height-1)
                    i += 1
        
        self.place_room(room, x, y)
        self.grid[pivot_x][pivot_y] = "^"
        return True
    
    def pick_room_pivot(self):
        '''
        Returns a random pivot chosen from across the map.
        '''
        x = randint(self.min_x, self.max_x)
        y = randint(self.min_y, self.max_y)
        
        if (self.grid[x][y] == "#"):
            if (self.grid[x-1][y] == " " and self.grid[x+1][y] == "."):
                facing = "west"
                origin_room = self.room_grid[x+1][y]
            elif (self.grid[x-1][y] == "." and self.grid[x+1][y] == " "):
                facing = "east"
                origin_room = self.room_grid[x-1][y]
            elif (self.grid[x][y-1] == " " and self.grid[x][y+1] == "."):
                facing = "south"
                origin_room = self.room_grid[x][y+1]
            elif (self.grid[x][y-1] == "." and self.grid[x][y+1] == " "):
                facing = "north"
                origin_room = self.room_grid[x][y-1]
            else:
                return None;
            
            return [x, y, facing, origin_room]
    
    def choose_room(self, domains):
        '''
        Chooses a room with the given domains.
        '''
        rooms = []
        for domain in domains:
            rooms.extend(Blueprint.find_blueprints(type=domain, zone=self.zone, floor=self.floor))
        
        if len(rooms) != 0:
            return rooms[randint(0, len(rooms)-1)].master()
    
    def rect_is_empty(self, x1, y1, x2, y2):
        '''
        Returns whether a specific area of the map is empty.
        '''
        if (x1 < 1 or y1 < 1 or x2 > len(self.grid)-1 or y2 > len(self.grid[0])-1):
            return False
        
        for x in range(x1, x2):
            for y in range(y1, y2):
                if (self.grid[x][y] != " "):
                    #self.grid[x][y] = "/"
                    return False
                else:
                    pass
                    #self.grid[x][y] = "_"
        
        return True
    
    def place_room(self, master, origin_x, origin_y):
        '''
        Creates a room at the specified origin.
        This method should first be checked with the rect_is_empty function.
        '''
        room_width = master.properties['width']
        room_height = master.properties['height']
        
        for x in [origin_x - 1, origin_x + room_width]:
            for y in range(origin_y - 1, origin_y + room_height + 1):
                self.grid[x][y] = "#"
        
        for x in range(origin_x, origin_x + room_width):
            self.grid[x][origin_y-1] = "#"
            self.grid[x][origin_y+room_height] = "#"
            for y in range(origin_y, origin_y + room_height):
                self.grid[x][y] = "."
                self.room_grid[x][y] = master
                
        x = origin_x + (room_width/2)
        y = origin_y + (room_height/2)
        
        self.grid[x][y] = master.properties['name'][0]
        
    def generate_door(self):
        pivot = None
        while pivot is None:
            pivot = self.pick_door_pivot()
            
        return self.try_door(*pivot)
        
    def pick_door_pivot(self):
        '''
        Returns a random pivot chosen from across the map.
        '''
        x = randint(self.min_x, self.max_x)
        y = randint(self.min_y, self.max_y)
        
        if (self.grid[x][y] == "#"):
            if (self.grid[x-1][y] == "." and self.grid[x+1][y] == "."):
                room_1 = self.room_grid[x-1][y]
                room_2 = self.room_grid[x+1][y]
            elif (self.grid[x][y-1] == "." and self.grid[x][y+1] == "."):
                room_1 = self.room_grid[x][y-1]
                room_2 = self.room_grid[x][y+1]
            else:
                return None;
            
            return [x, y, room_1, room_2]
        
    def try_door(self, x, y, room_1, room_2):
        '''
        Places a door at the given x/y coords, if a connection between room_1 and room_2 is valid.
        Returns success or failure.
        '''
        if (self.is_connection_valid(room_1, room_2)):
            self.grid[x][y] = "^"
            return True
        else:
            return False
        
    def is_connection_valid(self, room_1, room_2):
        '''
        Checks to see if a connection between the two given rooms would be valid.
        '''
        for type in room_1.blueprint.domains['type']:
            if (type in room_2.properties['connections']):
                return True

#gen = MapGenerator(width=20, height=20)
#map = gen.generate()
#
#for column in gen.grid:
#    print("".join(column))