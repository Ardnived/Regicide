'''
Created on Apr 9, 2013

@author: Devindra
'''
from functools import partial
from pyglet.window import key
from regicide.controller.hotspot import Hotspot
from regicide.controller.commands import CommandSet, KeyBinder, KeyBinding
from regicide.controller import functions

commands = CommandSet({
    'north': KeyBinder(
        bindings = [
            KeyBinding(key.MOTION_UP, KeyBinding.TYPE_MOTION),
            KeyBinding(key.NUM_8, KeyBinding.TYPE_REPEAT),
        ],
        action = partial(functions.move, y=1),
    ),
    'northwest': KeyBinder(
        bindings = [
                    KeyBinding(key.NUM_7, KeyBinding.TYPE_REPEAT),
        ],
        action = partial(functions.move, x=-1, y=1),
    ),
    'northeast': KeyBinder(
        bindings = [
            KeyBinding(key.NUM_9, KeyBinding.TYPE_REPEAT),
        ],
        action = partial(functions.move, x=1, y=1),
    ),
    'south': KeyBinder(
        bindings = [
            KeyBinding(key.MOTION_DOWN, KeyBinding.TYPE_MOTION),
            KeyBinding(key.NUM_2, KeyBinding.TYPE_REPEAT),
        ],
        action = partial(functions.move, y=-1),
    ),
    'southwest': KeyBinder(
        bindings = [
            KeyBinding(key.NUM_1, KeyBinding.TYPE_REPEAT),
        ],
        action = partial(functions.move, x=-1, y=-1),
    ),
    'southeast': KeyBinder(
        bindings = [
            KeyBinding(key.NUM_3, KeyBinding.TYPE_REPEAT),
        ],
        action = partial(functions.move, x=1, y=-1),
    ),
    'west': KeyBinder(
        bindings = [
            KeyBinding(key.MOTION_LEFT, KeyBinding.TYPE_MOTION),
            KeyBinding(key.NUM_4, KeyBinding.TYPE_REPEAT),
        ],
        action = partial(functions.move, x=-1),
    ),
    'east': KeyBinder(
        bindings = [
            KeyBinding(key.MOTION_RIGHT, KeyBinding.TYPE_MOTION),
            KeyBinding(key.NUM_6, KeyBinding.TYPE_REPEAT),
        ],
        action = partial(functions.move, x=1),
    ),
    
    'rest': KeyBinder(
        bindings = [KeyBinding(key.R)],
        action = None,
    ),
    'wait': KeyBinder(
        bindings = [KeyBinding(key.W)],
        action = functions.wait,
    ),
    'look': KeyBinder(
        bindings = [KeyBinding(key.L)],
        action = None,
    ),
    'view_properties': KeyBinder(
        bindings = [KeyBinding(key.P)],
        action = partial(functions.set_state, state='properties'),
    ),
    'view_traits': KeyBinder(
        bindings = [KeyBinding(key.T)],
        action = partial(functions.set_state, state='traits'),
    ),
    'view_actions': KeyBinder(
        bindings = [KeyBinding(key.K)],
        action = partial(functions.set_state, state='actions'),
    ),
    'view_inventory': KeyBinder(
        bindings = [KeyBinding(key.I)],
        action = partial(functions.set_state, state='inventory'),
    ),
})

class GameHotspot(Hotspot):
    
    def __init__(self, x, y, width, height, rows=1, columns=1, hover_type=Hotspot.HOVER_HIDDEN):
        Hotspot.__init__(self, x, y, width, height, rows, columns, hover_type)
            
    def on_click(self, model, row, column, button, modifiers):
        if (model.selection[0] != model.player.x or model.selection[1] != model.player.y):
            
            player_x = model.player.x
            player_y = model.player.y
            grid_x = player_x - self.grid_width/2
            grid_y = player_y - self.grid_height/2
            click_x = model.selection[0] + grid_x
            click_y = model.selection[1] + grid_y
            
            room = model.map.room_grid[click_x][click_y]
            if (room is not None):
                model.log_message("Selected "+room.properties['name'])
                model.do_update('log')
            
            if (player_x == click_x):
                if (player_y > click_y):
                    model.activate_command(commands.get('south'))
                else:
                    model.activate_command(commands.get('north'))
            elif (player_x > click_x):
                if (player_y > click_y):
                    model.activate_command(commands.get('southwest'))
                elif (player_y < click_y):
                    model.activate_command(commands.get('northwest'))
                else:
                    model.activate_command(commands.get('west'))
            elif (player_x < click_x):
                if (player_y > click_y):
                    model.activate_command(commands.get('southeast'))
                elif (player_y < click_y):
                    model.activate_command(commands.get('northeast'))
                else:
                    model.activate_command(commands.get('east'))

