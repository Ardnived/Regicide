'''
Created on 2013-06-02

@author: Devindra
'''
import random
from regicide.data import tiles
from regicide.level.world import Direction
from regicide.level.gen.generator import MapGenerator
from regicide.level.gen.castle import CastleGenerator

class SingleFloorGenerator(CastleGenerator):

    def generate(self, options):
        MapGenerator.generate(self, options)
        
        print("Creating Throne Room")
        self.create_throne_room()
        
        print("Creating "+str(self.room_quantity)+" rooms.")
        self.create_rooms(self.room_quantity)
        
        print("Creating dividers.")
        for direction in [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]:
            for _ in xrange(2):
                self.create_divider(direction)
        
        print("Decoding map.")
        tile_map = self.decode_map()
        print("Decorating rooms.")
        self.decorate_rooms(tile_map)
        
        print("Creating passages.")
        self.create_passages(tile_map, random.randint(3, 7))
        
        self.clean()
        return tile_map
    
    def create_throne_room(self):
        room = self.create_room(["throne"])
        
        x, y = self.random_location(None, room.width, room.height)
        while not self.rect_is_empty(x, y, x + room.width, y + room.height):
            x, y = self.random_location(None, room.width, room.height)
        
        self.place_room(room, x, y)
            
        return (x, y)
    
    def create_divider(self, direction=None):
        increment_x = 1
        increment_y = 1
        gutter = MapGenerator.GUTTER*3
        
        if Direction.AXIS_X in direction.axis:
            y = random.randint(gutter, self.extended_height - gutter)
            
            if direction.x_offset > 0:
                x = -1
                increment_x = -1
            else:
                x = 0
                increment_x = +1
            
            origin_x = x
            origin_y = y
            
            try:
                while self.grid[x][y] == None:
                    x += increment_x
            except IndexError:
                self.create_divider(direction) #retry
                return
            
        elif Direction.AXIS_Y in direction.axis:
            x = random.randint(gutter, self.extended_width - gutter)
            
            if direction.y_offset > 0:
                y = -1
                increment_y = -1
            else:
                y = 0
                increment_y = +1
            
            origin_x = x
            origin_y = y
            
            try:
                while self.grid[x][y] == None:
                    y += increment_y
            except IndexError:
                self.create_divider(direction) #retry
                return
        
        for x in xrange(origin_x, x+increment_x, increment_x):
            for y in xrange(origin_y, y+increment_y, increment_y):
                self.grid[x][y] = tiles.WALL
        