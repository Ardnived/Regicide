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
            KeyBinding(key.MOTION_UP, KeyBinding.TYPE_KEY),
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
                       
    'cancel': KeyBinder(
        bindings = [KeyBinding(key.ESCAPE)],
        action = functions.cancel,
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
        action = functions.look,
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
        
    def on_click(self, model, button, modifiers):
        if self.selection_x != model.player.x or self.selection_y != model.player.y:
            player_x = model.player.x
            player_y = model.player.y
            grid_x = player_x - self.grid_width/2
            grid_y = player_y - self.grid_height/2
            click_x = self.selection_x + grid_x
            click_y = self.selection_y + grid_y
            
            if player_x == click_x:
                if player_y > click_y:
                    model.activate_command(commands.get('south'))
                else:
                    model.activate_command(commands.get('north'))
            elif player_x > click_x:
                if player_y > click_y:
                    model.activate_command(commands.get('southwest'))
                elif player_y < click_y:
                    model.activate_command(commands.get('northwest'))
                else:
                    model.activate_command(commands.get('west'))
            elif player_x < click_x:
                if player_y > click_y:
                    model.activate_command(commands.get('southeast'))
                elif player_y < click_y:
                    model.activate_command(commands.get('northeast'))
                else:
                    model.activate_command(commands.get('east'))
    
    def on_select(self, model, x, y):
        Hotspot.on_select(self, model, x, y)
        
        tile = model.map.get_tile(self.grid_x + x, self.grid_y + y)
        text = None
        
        if tile is not None:
            if tile.entity is not None:
                text = tile.entity.name
            elif tile.room is not None:
                text = tile.room.name + " " + str(tile.room.count_connections())
        
        model.display_info(text)
        model.do_update('log')
