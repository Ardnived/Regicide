'''
Created on 2013-05-23

@author: Devindra
'''
import random

class Direction:
    AXIS_X = 0
    AXIS_Y = 1
    AXIS_Z = 3
    UP = None
    DOWN = None
    NORTH = None
    SOUTH = None
    EAST = None
    WEST = None
    
    def __init__(self, x=0, y=0, z=0):
        self.x_offset = x
        self.y_offset = y
        self.z_offset = z
        self.opposite = None
        
        axis = []
        if x != 0:
            axis.append(Direction.AXIS_X)
        if y != 0:
            axis.append(Direction.AXIS_Y)
        if z != 0:
            axis.append(Direction.AXIS_Z)
        
        self.axis = axis
    
Direction.UP    = Direction(0, 0, +1)
Direction.DOWN  = Direction(0, 0, -1)
Direction.NORTH = Direction(0, +1, 0)
Direction.SOUTH = Direction(0, -1, 0)
Direction.EAST  = Direction(+1, 0, 0)
Direction.WEST  = Direction(-1, 0, 0)

Direction.UP.opposite = Direction.DOWN
Direction.DOWN.opposite = Direction.UP
Direction.NORTH.opposite = Direction.SOUTH
Direction.SOUTH.opposite = Direction.NORTH
Direction.EAST.opposite = Direction.WEST
Direction.WEST.opposite = Direction.EAST

from regicide.level import generator
from regicide.level.floors import CastleFloor

class World(object):
    '''
    Contains a three dimensional grid of all the floors in the game.
    '''
    DEFAULT_LENGTH_X = 10
    DEFAULT_LENGTH_Y = 10
    FLOORS = {
        -2: {
            'name': "Depths",
            'generator': generator.CastleGenerator(),
            'zone': 'depths',
            'types': [CastleFloor],
            'fill': True,
        },
        -1: {
            'name': "Dungeon",
            'generator': generator.CastleGenerator(),
            'zone': 'underground',
            'types': [CastleFloor],
            'fill': True,
        },
        0: {
            'name': "Ground Floor",
            'generator': generator.CastleGenerator(),
            'zone': 'castle',
            'types': [CastleFloor],
            'fill': True,
        },
        1: {
            'name': "Floor 1",
            'generator': generator.CastleGenerator(),
            'zone': 'castle',
            'types': [CastleFloor],
            'fill': True,
        },
        2: {
            'name': "Floor 2",
            'generator': generator.CastleGenerator(),
            'zone': 'tower',
            'types': [CastleFloor],
            'fill': False,
        },
        3: {
            'name': "Floor 3",
            'generator': generator.CastleGenerator(),
            'zone': 'tower',
            'types': [CastleFloor],
            'fill': False,
        },
        4: {
            'name': "Floor 4",
            'generator': generator.CastleGenerator(),
            'zone': 'tower',
            'types': [CastleFloor],
            'fill': False,
        },
    }

    def __init__(self, x_length=DEFAULT_LENGTH_X, y_length=DEFAULT_LENGTH_Y):
        '''
        Constructor
        '''
        self._grid = []
        self.columns = x_length
        self.rows = y_length
        
        for _ in xrange(x_length):
            row = []
            for _ in xrange(y_length):
                column = []
                for depth, floor in World.FLOORS.iteritems():
                    column.append(random.choice(floor['types'])(depth))
                row.append(column)
            self._grid.append(row)
    
    def get_floor(self, x, y, z):
        '''
        Gets the floor at the specified coordinates if there is one, 
        and the coordinates are valid. Otherwise, returns None
        '''
        try:
            floor = self._grid[x][y][z]    
        except (IndexError, KeyError):
            floor = None
        
        return floor
    
    def generate_floor(self, x, y, z):
        floor = self.get_floor(x, y, z)
        
        if floor is not None:
            floor.generate(connections = self.get_external_connections(x, y, z))
    
    def get_external_connections(self, x, y, z):
        '''
        Looks at all the floors adjacent to the floor at the specified location,
        and gets the connections they have to this specified floor.
        '''
        connections = {}
        
        for direction in [Direction.UP, Direction.DOWN, Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            floor_x = x + direction.x_offset
            floor_y = y + direction.y_offset
            floor_z = z + direction.z_offset
            
            if floor_x >= 0 and floor_x < self.columns and floor_y >= 0 and floor_y < self.rows:
                try:
                    floor = self._grid[floor_x][floor_y][floor_z]
                except IndexError:
                    floor = None
            else:
                floor = None
            
            if floor is not None:
                connections[direction] = floor.get_connections(direction.opposite)
            else:
                connections[direction] = False
        
        return connections
    
