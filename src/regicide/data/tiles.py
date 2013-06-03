'''
Created on 2013-05-30

@author: Devindra
'''
from regicide.resources import visual
from regicide.level.tile import Tile, Stair, Gate
from regicide.level.world import Direction

FLOOR = {
    'sprites' : [visual.Tile.BLOCK, visual.Tile.BLOCK, visual.Tile.BLOCK_CRACKED],
    'ascii'   : visual.ASCII.get_index(13, 13), #(11, 3), #(13, 13),
    'type'    : [Tile.TARGET_FLOOR, Tile.TARGET_PASSABLE],
    'class'   : Tile,
    'params'  : {},
}

LIGHT = {
    'sprites' : [visual.Tile.PLINTH_EYE],
    'ascii'   : visual.ASCII.get_index(8, 9),
    'type'    : [Tile.TARGET_FLOOR, Tile.TARGET_PASSABLE],
    'class'   : Tile,
    'params'  : {},
}

STAIRS_UP = {
    'sprites' : [visual.Tile.STAIRS_UP],
    'ascii'   : visual.ASCII.get_index(12, 12),
    'type'    : [Tile.TARGET_ROUGH, Tile.TARGET_PASSABLE],
    'class'   : Stair,
    'params'  : {
        'up' : True,
    },
}

STAIRS_DOWN = {
    'sprites' : [visual.Tile.STAIRS_DOWN],
    'ascii'   : visual.ASCII.get_index(14, 12),
    'type'    : [Tile.TARGET_ROUGH, Tile.TARGET_PASSABLE],
    'class'   : Stair,
    'params'  : {
        'up' : False,
    },
}

WALL = {
    'sprites' : [visual.Tile.PLINTH_LIGHT],
    'ascii'   : visual.ASCII.get_index(7, 0),
    'type'    : [Tile.TARGET_WALL, Tile.TARGET_OPAQUE],
    'class'   : Tile,
    'params'  : {},
}

GATE_NORTH = {
    'sprites' : [visual.Tile.COLUMNS_GATE],
    'ascii'   : visual.ASCII.get_index(9, 13),
    'type'    : [Tile.TARGET_DOOR, Tile.TARGET_PASSABLE],
    'class'   : Gate,
    'params'  : {
        'direction' : Direction.NORTH,
    },
}

GATE_SOUTH = {
    'sprites' : [visual.Tile.COLUMNS_GATE],
    'ascii'   : visual.ASCII.get_index(9, 13),
    'type'    : [Tile.TARGET_DOOR, Tile.TARGET_PASSABLE],
    'class'   : Gate,
    'params'  : {
        'direction' : Direction.SOUTH,
    },
}

GATE_WEST = {
    'sprites' : [visual.Tile.COLUMNS_GATE],
    'ascii'   : visual.ASCII.get_index(9, 13),
    'type'    : [Tile.TARGET_DOOR, Tile.TARGET_PASSABLE],
    'class'   : Gate,
    'params'  : {
        'direction' : Direction.WEST,
    },
}

GATE_EAST = {
    'sprites' : [visual.Tile.COLUMNS_GATE],
    'ascii'   : visual.ASCII.get_index(9, 13),
    'type'    : [Tile.TARGET_DOOR, Tile.TARGET_PASSABLE],
    'class'   : Gate,
    'params'  : {
        'direction' : Direction.EAST,
    },
}

DOOR = {
    'sprites' : [visual.Tile.GATE_1, visual.Tile.GATE_2, visual.Tile.GATE_3],
    'ascii'   : visual.ASCII.get_index(10, 13),
    'type'    : [Tile.TARGET_DOOR, Tile.TARGET_PASSABLE],
    'class'   : Tile,
    'params'  : {},
}

SECRET_DOOR = {
    'sprites' : [visual.Tile.COLUMNS_GATE],
    'ascii'   : visual.ASCII.get_index(2, 13),
    'type'    : [Tile.TARGET_DOOR, Tile.TARGET_PASSABLE],
    'class'   : Tile,
    'params'  : {},
}

DECORATION = {
    'sprites' : [visual.Tile.TILES],
    'ascii'   : visual.ASCII.get_index(11, 13),
    'type'    : [Tile.TARGET_PASSABLE],
    'class'   : Tile,
    'params'  : {},
}