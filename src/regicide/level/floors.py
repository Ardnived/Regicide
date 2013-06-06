'''
Created on 2013-05-27

@author: Devindra
'''
from regicide.level.world import Direction
from regicide.level.gen.castle import CastleGenerator
from regicide.level.gen.single import SingleFloorGenerator

class Floor(object):
    
    def __init__(self, depth):
        self.depth = depth
        self.map = None
        self.known = False
        self.explored = False
        self._connections = {}
    
    def add_connection(self, direction, x, y):
        if not self._connections.has_key(direction):
            self._connections[direction] = []
        
        self._connections[direction].append((x, y))
    
    def has_connection(self, direction):
        return len(self.get_connections(direction)) > 0
    
    def get_connections(self, direction=None):
        if direction is None:
            return self._connections
        elif self._connections.has_key(direction):
            return self._connections[direction]
        else:
            return []

class CastleFloor(Floor, CastleGenerator):
    
    def __init__(self, depth):
        Floor.__init__(self, depth)
        CastleGenerator.__init__(self, 
            zone  = "castle", 
            floor = "commons",
        )
    
    def generate(self, **options):
        self.map = CastleGenerator.generate(self, options)
        
    def create_stairwell(self, location=None, up=False):
        location = CastleGenerator.create_stairwell(self, location=location, up=up)
        
        if up:
            self.add_connection(Direction.UP, *location)
        else:
            self.add_connection(Direction.DOWN, *location)
        
        return location
        
    def create_exit(self, direction=None, location=None):
        location = CastleGenerator.create_exit(self, direction=direction, location=location)
        
        self.add_connection(direction, *location)
        
        return location

class SingleFloor(Floor, SingleFloorGenerator):
    
    def __init__(self, depth):
        Floor.__init__(self, depth)
        SingleFloorGenerator.__init__(self, 
            zone  = "castle", 
            floor = "commons",
        )
    
    def generate(self, **options):
        self.map = SingleFloorGenerator.generate(self, options)
