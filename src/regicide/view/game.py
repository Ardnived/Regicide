'''
Created on Apr 6, 2013

@author: Devindra
'''
import math
from pyglet import graphics
from pyglet import text
from pyglet import sprite
from pyglet import image
from pyglet import gl
from pyglet.window import mouse
from regicide.view.view import View, Layer, ActiveListLayer
from regicide.resources import visual
from regicide.entity import properties
from regicide.controller.hotspot import Hotspot
from regicide.controller.game import GameHotspot
from regicide.controller import functions
from regicide.controller import commands
from regicide.entity.actions import action
from regicide.mvc import State

class GameView(View):
    FONT_NAME = View.FONT_NAME
    FONT_SIZE = View.FONT_SIZE
    FONT_RATIO = View.FONT_RATIO
    
    LOWER_BAR_HEIGHT = 200
    LOWER_BAR_GUTTER_X = 20
    LOWER_BAR_GUTTER_Y = 10
    
    COMMAND_BAR_GUTTER_X = 10
    COMMAND_BAR_FONT_SIZE = 3
    COMMAND_BAR_HEIGHT = 20
    
    INFO_GUTTER_X = 10
    INFO_GUTTER_Y = 10
    INFO_FONT_SIZE = 14
    INFO_WIDTH = 150
    INFO_HEIGHT = 390
    
    LOG_LINE_HEIGHT = 15
    LOG_FONT_SIZE = FONT_SIZE
    LOG_LINE_QUANTITY = (LOWER_BAR_HEIGHT - LOWER_BAR_GUTTER_Y*2) / LOG_LINE_HEIGHT
    LOG_HTML_FONT_SIZE = 2
    
    LOWER_BAR_LINE_HEIGHT = 15
    LOWER_BAR_FONT_SIZE = 11
    LOWER_BAR_LINE_QUANTITY = (LOWER_BAR_HEIGHT - LOWER_BAR_GUTTER_Y*2) / LOWER_BAR_LINE_HEIGHT
    
    EFFECTS_LINE_HEIGHT = 15
    EFFECTS_FONT_SIZE = 10
    
    MIN_LIGHT = 50
    
    def __init__(self, window, ascii=True):
        View.__init__(self, window)
        
        # Create the log window
        log_x = GameView.LOWER_BAR_GUTTER_X
        log_y = GameView.LOWER_BAR_GUTTER_Y
        log_width = (window.width / 3) - GameView.LOWER_BAR_GUTTER_X*3/2
        log_height = GameView.LOWER_BAR_HEIGHT - GameView.LOWER_BAR_GUTTER_Y*2
        log_layer = Log(log_x, log_y, log_width, log_height)
        self.layers.append(log_layer)
        
        # Create the inventory window
        inv_x = log_width + GameView.LOWER_BAR_GUTTER_X*2
        inv_width = ((window.width - log_width) / 3) - GameView.LOWER_BAR_GUTTER_X*3/2
        inv_layer = Inventory(inv_x, log_y, inv_width, log_height)
        self.layers.append(inv_layer)
        
        # Create the stances window
        stance_x = inv_x + inv_width + GameView.LOWER_BAR_GUTTER_X
        stance_layer = Actions(stance_x, log_y, inv_width, log_height)
        self.layers.append(stance_layer)
        
        # Create the actions window
        act_x = stance_x + inv_width + GameView.LOWER_BAR_GUTTER_X
        act_layer = Actions(act_x, log_y, inv_width, log_height)
        self.layers.append(act_layer)
        
        # Create the info window
        info_x = window.width - (GameView.INFO_WIDTH + GameView.INFO_GUTTER_X*2)
        info_y = window.height - (GameView.INFO_HEIGHT + GameView.INFO_GUTTER_Y)
        info_width = GameView.INFO_WIDTH
        info_height = GameView.INFO_HEIGHT
        info_layer = PlayerCard(info_x, info_y, info_width, info_height)
        self.layers.append(info_layer)
        
        # Create the effects list
        effects_x = window.width - (GameView.INFO_WIDTH + GameView.INFO_GUTTER_X*2)
        effects_y = GameView.LOWER_BAR_HEIGHT
        effects_width = GameView.INFO_WIDTH
        effects_height = window.height - GameView.LOWER_BAR_HEIGHT - GameView.INFO_GUTTER_Y*2 - info_height
        effects_layer = Effects(effects_x, effects_y, effects_width, effects_height)
        self.layers.append(effects_layer)
    
        # Create the command bar
        cmd_x = GameView.COMMAND_BAR_GUTTER_X
        cmd_y = GameView.LOWER_BAR_HEIGHT
        cmd_width = info_x - GameView.INFO_GUTTER_X - GameView.COMMAND_BAR_GUTTER_X*2
        cmd_height = GameView.COMMAND_BAR_HEIGHT + GameView.LOWER_BAR_GUTTER_Y
        cmd_layer = CommandBar(cmd_x, cmd_y, cmd_width, cmd_height)
        self.layers.append(cmd_layer)
        
        # Create the main game window
        game_x = 0
        game_y = GameView.LOWER_BAR_HEIGHT + cmd_height
        game_width = info_x - GameView.INFO_GUTTER_X
        game_height = window.height - log_height - cmd_height
        if ascii is True:
            game_layer = AsciiGame(game_x, game_y, game_width, game_height)
        else:
            game_layer = TileGame(game_x, game_y, game_width, game_height)
        self.layers.append(game_layer)

class GameLayer(Layer, GameHotspot):
    def __init__(self, x, y, width, height, tile_width, tile_height, color):
        Layer.__init__(self, x, y, width, height, color)
        self.cursor = sprite.Sprite(visual.Cursor.get(visual.Cursor.SELECT), x=-50)
        self.show_cursor = False
        
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.grid_width = self.width / self.tile_width
        self.grid_height = self.height / self.tile_height

        self.cursor.scale = float(self.tile_width / 32.0)
        
        GameHotspot.__init__(self, x, y, width, height, self.grid_height, self.grid_width, hover_type=Hotspot.HOVER_HIDDEN)
       
    def draw(self):
        Layer.draw(self);
        if self.show_cursor:
            self.cursor.draw()
    
    def update(self, components = None):
        if components is None or 'cursor' in components:
            self.update_cursor();
        
    def update_cursor(self):
        model = State.model()
        
        if self.has_focus:
            self.update_game_bounds()
            
            if model.state == model.STATE_EXPLORE:
                x = self.columns / 2
                y = self.rows / 2
            else:
                x = self.selection_x
                y = self.selection_y
                
            absolute_x = self.grid_x + x
            absolute_y = self.grid_y + y - 1
            
            valid = model.is_valid_target(absolute_x, absolute_y)
            if valid is None:
                self.cursor.image = visual.Cursor.get(visual.Cursor.TARGET)
            elif valid:
                self.cursor.image = visual.Cursor.get(visual.Cursor.YELLOW)
            else:
                self.cursor.image = visual.Cursor.get(visual.Cursor.SELECT)
            
            if valid is not None and (absolute_x != model.player.x or absolute_y != model.player.y):
                path = model.map.find_path(model.map.ALGORITHM_ASTAR, model.player.x, model.player.y, absolute_x, absolute_y)
                
                if path is not None:
                    for path_x, path_y in path:
                        self.highlight_tile(path_x, path_y)
                
                    self.highlight_tile(model.player.x, model.player.y)
                    self.highlight_tile(absolute_x, absolute_y)
            
            self.cursor.x = x * self.tile_width + self.x
            self.cursor.y = (self.rows - y - 1) * self.tile_height + self.y
            self.show_cursor = True
        else:
            self.show_cursor = False
            
    def update_game_bounds(self):
        center = State.model().get_center()
        self.grid_x = center[0] - self.grid_width/2
        self.grid_y = center[1] - self.grid_height/2
        
    def highlight_tile(self, x, y):
        pass
                    
    def is_game_layer(self):
        return True

class TileGame(GameLayer):
    def __init__(self, x, y, width, height):
        GameLayer.__init__(self, x, y, width, height, 32, 32, [0.0, 0.0, 255.0])
        self.tile_layer = None
        self.entity_layer = None
        
        if True: #TODO: Change this check to be opacity vs. pixel shading. via some kind of options class.
            self.shadow_layer = graphics.Batch()
            self.batches.append(self.shadow_layer)
            
            self.shadows = []
            for x in range(self.grid_width):
                self.shadows.append([])
                for y in range(self.grid_height):
                    self.shadows[x].append(sprite.Sprite(
                        img = image.Texture.create(self.tile_width, self.tile_height),
                        x = self.x + x*self.tile_width,
                        y = self.y + y*self.tile_height,
                    ))

    
    def update(self, components = None):
        if components is None or 'bounds' in components:
            self.update_game_bounds()
            
        if components is None or 'bounds' in components or 'tiles' in components:
            self.update_tiles();
            
        if components is None or 'bounds' in components or 'entities' in components:
            self.update_entities();

        if components is None or 'bounds' in components or 'shadows' in components:
            self.update_shadows();
            
        GameLayer.update(self, components)
        
    def update_tiles(self):
        if self.tile_layer is not None:
            self.batches.remove(self.tile_layer)
        
        self.tile_layer = graphics.Batch()
        self.batches.append(self.tile_layer)
        model = State.model()
        grid = model.map.grid
        
        for x in range(max(0, self.grid_x), min(self.grid_x + self.grid_width, len(grid))):
            for y in range(max(0, self.grid_y), min(self.grid_y + self.grid_height, len(grid[x]))):
                tile = grid[x][y]
                if tile is not None:
                    sprite = tile.sprite
                    sprite.batch = self.tile_layer
                    sprite.x = x*self.tile_width - self.grid_x*self.tile_width + self.x
                    sprite.y = y*self.tile_height - self.grid_y*self.tile_width + self.y
        
    def update_entities(self):
        if self.entity_layer is not None:
            self.batches.remove(self.entity_layer)
        
        self.entity_layer = graphics.Batch()
        self.batches.append(self.entity_layer)
        model = State.model()
        grid = model.map.grid
        
        for x in range(max(0, self.grid_x), min(self.grid_x + self.grid_width, len(grid))):
            for y in range(max(0, self.grid_y), min(self.grid_y + self.grid_height, len(grid[x]))):
                tile = grid[x][y]
                if tile is not None and tile.entity is not None:
                    sprite = tile.entity.sprite
                    sprite.color = [255, 100, 100]
                    sprite.batch = self.entity_layer
                    sprite.x = x*self.tile_width - self.grid_x*self.tile_width + self.x
                    sprite.y = y*self.tile_height - self.grid_y*self.tile_height + self.y
        
    def update_shadows(self):
        print('update shadows')
        model = State.model()
        
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                tile = model.map.get_tile(self.grid_x + x, self.grid_y + y)
                if tile is not None:
                    if True: #TODO: Change this check to be opacity vs. pixel shading. via some kind of options class.
                        sprite = self.shadows[x][y]
                        sprite.image = visual.Tile.get_shadow(7)
                        sprite.batch = self.shadow_layer
                    else:
                        if tile.shadow > 0:
                            sprite.opacity = (255 - GameView.MIN_LIGHT) / (tile.shadow + 1) + GameView.MIN_LIGHT
                        else:
                            sprite.opacity = 255
                        
                        if model.state == model.STATE_TARGET:
                            valid = model.is_valid_target(x, y)
                            if valid is None:
                                sprite.opacity *= 0.25
                            elif valid is False:
                                sprite.opacity *= 0.55
                elif True: #TODO: Change this check to be opacity vs. pixel shading. via some kind of options class.
                    self.shadows[x][y].batch = None


class AsciiGame(GameLayer):
    TILE_SIZE = 20
    
    def __init__(self, x, y, width, height):
        GameLayer.__init__(self, x, y, width, height, self.TILE_SIZE, self.TILE_SIZE, [0.0, 0.0, 255.0])
        
    def update(self, components = None):
        if components is None or 'bounds' in components:
            self.update_game_bounds()
        
        if components is None or 'bounds' in components or 'tiles' in components or 'entities' in components:
            self.update_grid()
        
        '''
        if components is None or 'bounds' in components or 'shadows' in components:
            self.update_shadows()
        '''
            
        GameLayer.update(self, components)
        
    def update_grid(self):
        self.batches = graphics.Batch()
        model = State.model()
        
        for x in range(max(0, self.grid_x), min(self.grid_x + self.grid_width, model.map.width)):
            for y in range(max(0, self.grid_y), min(self.grid_y + self.grid_height, model.map.height)):
                tile = model.map.get_tile(x, y)
                if tile is not None:
                    if tile.entity is None:
                        sprite = tile.ascii
                        
                        if tile.is_opaque():
                            sprite.color = [255, 100, 100]
                        else:
                            sprite.color = [255, 255, 255]
                    else:
                        sprite = tile.entity.ascii
                        sprite.color = [100, 100, 255]
                    
                    sprite.batch = self.batches
                    sprite.x = self.x + (x*self.tile_width - self.grid_x*self.tile_width)
                    sprite.y = self.y + (y*self.tile_height - self.grid_y*self.tile_height)
        
    def update_shadows(self):
        model = State.model()
        
        for x in range(max(0, self.grid_x), min(self.grid_x + self.grid_width, model.map.width)):
            for y in range(max(0, self.grid_y), min(self.grid_y + self.grid_height, model.map.height)):
                tile = model.map.get_tile(x, y)
                if tile is not None: 
                    if tile.entity is None:
                        sprite = tile.ascii
                    else:
                        sprite = tile.entity.ascii
                    
                    player = State.model().player
                    
                    if not tile.explored:
                        sprite.color = [0, 0, 0]
                    elif model.map.has_line_of_sight(player.x, player.y, x, y):
                        if tile.is_opaque():
                            light_x = x
                            light_y = y
                            
                            distance_x = x - player.x
                            distance_y = y - player.y
                            
                            if distance_x == 0:
                                light_y = light_y - int(math.copysign(1, distance_y))
                            elif distance_y == 0:
                                light_x = light_x - int(math.copysign(1, distance_x))
                            else:
                                angle = math.radians(distance_y / distance_y)
                                delta_x = math.cos(angle)
                                delta_y = math.sin(angle)
                                
                                if delta_x >= delta_y:
                                    light_x -= int(math.copysign(1, distance_x))                                
                                if delta_x <= delta_y:
                                    light_y -= int(math.copysign(1, distance_y))
                            
                            light_source = model.map.get_tile(light_x, light_y)
                            if light_source is not None:
                                shadow = light_source.shadow
                            else:
                                shadow = 100
                        else:
                            shadow = tile.shadow
                        
                        if shadow > 0:
                                sprite.opacity = (255 - GameView.MIN_LIGHT) / (shadow + 1) + GameView.MIN_LIGHT
                        else:
                            sprite.opacity = 255
                    else:
                        sprite.opacity = 128
                        sprite.color = [128, 128, 128]
                    
                    if model.state == model.STATE_TARGET:
                        valid = model.is_valid_target(x, y)
                        if valid is None:
                            sprite.opacity *= 0.25
                        elif valid is False:
                            sprite.opacity *= 0.55
        
    def highlight_tile(self, x, y):
        sprite = State.model().map.get_tile(x, y).ascii
        #sprite.color = [0, 255, 0]
        #TODO: uncomment the above line.

class Log(Layer):
    HTML_FONT = '<font face="'+GameView.FONT_NAME+'" size="'+str(GameView.LOG_HTML_FONT_SIZE)+'" color="white">'
    
    def __init__(self, x, y, width, height):
        Layer.__init__(self, x, y, width, height, [0.0, 255.0, 255.0])
        
        self.batches = graphics.Batch()
        self.log = []
        self.max_chars = int(width / GameView.LOG_FONT_SIZE * GameView.FONT_RATIO)
        
        for i in range(GameView.LOG_LINE_QUANTITY):
            self.log.append(text.Label(font_name=GameView.FONT_NAME, font_size=GameView.LOG_FONT_SIZE, x=x, y=y+i*GameView.LOG_LINE_HEIGHT, batch=self.batches))
        
        self.info = text.HTMLLabel(x=x, y=height, width=width, height=height, multiline=True, batch=self.batches)
        
    def update(self, components = None):
        model = State.model()
        
        if components is None or 'log' in components:
            if model.info:
                for i in range(min(len(model.log), len(self.log))):
                    self.log[i].text = ""
                    
                self.info.text = Log.HTML_FONT + model.info + "</font>"
            else:
                for i in range(min(len(model.log), len(self.log))):
                    self.log[i].text = model.log[i+model.log_offset]
                
                self.info.text = ""


class PlayerCard(Layer):
    def __init__(self, x, y, width, height):
        Layer.__init__(self, x, y, width, height, [0.0, 255.0, 0.0])
        
        self.batches = graphics.Batch()
        self.portrait = sprite.Sprite(visual.Character.HELENA, x+0, y+height-240, batch=self.batches)
        self.portrait.scale = 0.8
        
        self.name = self.create_label(5, 250, 4)
        self.hp = self.create_label(5, 270, 4)
        self.hp.color = (255, 215, 0, 255)
        self.mana = self.create_label(5, 285, 4)
        self.mana.color = (135, 206, 235, 255)
        self.attributes = self.create_label(5, 310, 2, multiline=True)
        
        self.effects = self.create_label(5, 415, multiline=True)
        
    def create_label(self, x, y, font_adjust=0, multiline=False):
        font_size = GameView.FONT_SIZE + font_adjust
        return text.Label("", GameView.FONT_NAME, font_size, x=self.x+x, y=self.y+self.height-y, multiline=multiline, width=self.width, batch=self.batches)
    
    def update(self, components = None):
        if components is None or 'playercard' in components:
            player = State.model().player
            self.portrait.image = player.portrait
            self.name.text = player.name
            self.hp.text = "HP: "+str(player.get(properties.hp))+" / "+str(player.get(properties.max_hp))
            self.mana.text = "MN: "+str(player.get(properties.mana))+" / "+str(player.get(properties.max_mana))
            
            self.attributes.text = ''
            self.attributes.text += "Dexterity   "+str(player.get(properties.dexterity))+"\n"
            self.attributes.text += "Agility     "+str(player.get(properties.agility))+"\n"
            self.attributes.text += "Mobility    "+str(player.get(properties.mobility))+"\n"
            self.attributes.text += "Wits        "+str(player.get(properties.wits))+"\n"
            self.attributes.text += "Perception  "+str(player.get(properties.perception))
            
            '''
            self.effects.text = ''
            for effect in player.effects:
                name = effect.name
                spacing = " " * (12 - len(name))
                duration = effect.duration
                self.effects.text += name + spacing + str(duration) + '\n'
            '''

class Effects(Layer, Hotspot):
    def __init__(self, x, y, width, height):
        Layer.__init__(self, x, y, width, height, [255.0, 0.0, 255.0])
        
        self.batches = graphics.Batch()
        self.items = []
        
        self.line_quantity = height / GameView.EFFECTS_LINE_HEIGHT
        for i in range(self.line_quantity):
            self.items.append(text.Label(font_name=GameView.FONT_NAME, font_size=GameView.EFFECTS_FONT_SIZE, x=x, y=y+i*GameView.EFFECTS_LINE_HEIGHT, batch=self.batches))
        
        Hotspot.__init__(self, x, y, width, height, rows=self.line_quantity)
    
    def draw(self):
        Layer.draw(self)
        
        '''
        i = 0
        height = self.height/len(self.items)
        for _ in self.items:
            y = self.y + i*height
            y2 = self.y + i*height + height
            gl.glColor3f(*self.color)
            graphics.draw(2, gl.GL_LINES, ('v2i', (self.x, y, self.x+self.width, y)))
            graphics.draw(2, gl.GL_LINES, ('v2i', (self.x, y2, self.x+self.width, y2)))
            i += 1
        '''
        
    def update(self, components = None):
        if components is None or 'effects' in components:
            player = State.model().player
            
            for i in range(min(len(player.effects), len(self.items))):
                effect = player.effects[i]
                index = self.line_quantity - i - 1
                
                name = effect.name
                spacing = " " * (12 - len(name))
                duration = effect.duration
                self.items[index].text = name + spacing + str(duration)
                self.items[index].effect = effect
        
        if components is None or 'cursor' in components:
            self.update_cursor();
        
    def update_cursor(self):
        for label in self.items:
                label.bold = False
        
        if self.has_focus:
            self.items[self.selection_y].bold = True
        
    def on_select(self, model, x, y):
        Hotspot.on_select(self, model, x, y)
        
        item = self.items[self.selection_y]
        if item.text != "":
            model.display_info(item.effect.name+"<br /><br />"+item.effect.description)
        else:
            model.display_info(None)
        
    def on_focus_lost(self, model):
        Hotspot.on_focus_lost(self, model)
        model.display_info(None)

class Inventory(ActiveListLayer):
    def __init__(self, x, y, width, height):
        ActiveListLayer.__init__(self, x, y, width, height)
        
    def update(self, components = None):
        ActiveListLayer.update(self, components)
        if components is None or 'inventory' in components:
            player = State.model().player
            
            for i in range(min(len(player.inventory), self.rows)):
                x = i / self.rows
                y = i
                item = player.inventory[i]
                
                text = ""
                if item in player.equipment[item.equip_slot]:
                    text += "e "
                else:
                    text += "  "
                
                text += item.name
                self.items[x][y].text = text
                self.items[x][y].item = item
        
    def on_select(self, model, selection_x, selection_y):
        ActiveListLayer.on_select(self, model, selection_x, selection_y)
        
        item = self.items[0][selection_y]
        if item.text != "":
            model.display_info(item.item.name+"<br /><br />"+item.item.description)
        else:
            model.display_info(None)
        
    def on_focus_lost(self, model):
        ActiveListLayer.on_focus_lost(self, model)
        model.display_info(None)
            
    def on_click(self, model, button, modifiers):
        if button == mouse.LEFT:
            functions.toggle_equip(model, self.items[0][self.selection_y].item)
            model.display_info(None)
        elif button == mouse.RIGHT:
            functions.set_state(model, 'inventory')
            #TODO: make it so that you are now selecting the appropriate tile.

class Actions(ActiveListLayer):
    def __init__(self, x, y, width, height):
        ActiveListLayer.__init__(self, x, y, width, height)
        
    def update(self, components = None):
        ActiveListLayer.update(self, components)
        if components is None or 'actions' in components:
            player = State.model().player
            
            for i in range(min(len(player.actions), self.rows)):
                action = player.actions[i]
                
                x = i / self.rows
                y = i
                self.items[x][y].text = action.name
                self.items[x][y].action = action
        
    def on_select(self, model, selection_x, selection_y):
        ActiveListLayer.on_select(self, model, selection_x, selection_y)
        
        item = self.items[0][selection_y]
        if item.text != "":
            model.display_info(item.action.name+"<br /><br />"+item.action.description)
        else:
            model.display_info(None)
        
    def on_focus_lost(self, model):
        ActiveListLayer.on_focus_lost(self, model)
        model.display_info(None)
            
    def on_click(self, model, button, modifiers):
        if button == mouse.LEFT:
            player = State.model().player
            index = self.rows - self.selection_y - 1
            model.execute_action(action.ActionInstance(
                action = player.actions[index],
                source = model.player,
            ))
        elif button == mouse.RIGHT:
            functions.set_state(model, 'actions')
            #TODO: make it so that you are now selecting the appropriate tile.

class Stances(ActiveListLayer):
    def __init__(self, x, y, width, height):
        ActiveListLayer.__init__(self, x, y, width, height)
        
    def update(self, components = None):
        ActiveListLayer.update(self, components)
        if components is None or 'stance' in components:
            player = State.model().player
            
            for i in range(min(len(player.actions), self.rows)):
                action = player.actions[i]
                
                x = i / self.rows
                y = i
                self.items[x][y].text = action.name
                self.items[x][y].action = action
        
    def on_select(self, model, selection_x, selection_y):
        ActiveListLayer.on_select(self, model, selection_x, selection_y)
        
        item = self.items[0][selection_y]
        if item.text != "":
            model.display_info(item.action.name+"<br /><br />"+item.action.description)
        else:
            model.display_info(None)
        
    def on_focus_lost(self, model):
        ActiveListLayer.on_focus_lost(self, model)
        model.display_info(None)
            
    def on_click(self, model, button, modifiers):
        if button == mouse.LEFT:
            player = State.model().player
            index = self.rows - self.selection_y - 1
            model.execute_action(action.ActionInstance(
                action = player.actions[index],
                source = model.player,
            ))
        elif button == mouse.RIGHT:
            functions.set_state(model, 'actions')
            #TODO: make it so that you are now selecting the appropriate tile.
           
class CommandBar(Layer, Hotspot):
    FONT = '<font face="'+GameView.FONT_NAME+'" size="'+str(GameView.COMMAND_BAR_FONT_SIZE)+'" color="white">'
    BUTTONS = ["<u>P</u>ROPERTIES", "S<u>K</u>ILLS", "<u>T</u>RAITS", "<u>L</u>OOK AROUND", "<u>W</u>AIT", "<u>R</u>EST"]
    ACTIONS = ['view_properties', 'view_actions', 'view_traits', 'look', 'wait', 'rest']
    
    def __init__(self, x, y, width, height):
        Layer.__init__(self, x, y, width, height, [255.0, 0.0, 0.0])
        Hotspot.__init__(self, x, y, width, height, columns=len(CommandBar.BUTTONS), hover_type=Hotspot.HOVER_CLICK)
        
        self.batches = graphics.Batch()
        self.commands = []
        for text in CommandBar.BUTTONS:
            self.create_label(text)
        
        self.redistribute_labels()
    
    def create_label(self, label, font=FONT):
        self.commands.append(text.HTMLLabel(text='<center>'+font+label+'</font></center>', x=self.x, y=self.y+(self.height-GameView.COMMAND_BAR_FONT_SIZE*3)/2, height=self.height, batch=self.batches))
        
    def redistribute_labels(self):
        i = 0
        button_width = self.width/len(self.commands)
        for label in self.commands:
            label_width = label.content_width
            label.x = self.x + i*button_width + (button_width - label_width)/2
            i += 1
    
    def update(self, components = None):
        if components is None or 'commandbar' in components:
            pass
        
        if components is None or 'cursor' in components:
            self.update_cursor();
        
    def update_cursor(self):
        for label in self.commands:
                label.bold = False
        
        if self.has_focus:
            self.commands[self.selection_x].bold = True

    def draw(self):
        Layer.draw(self)
        
        '''
        i = 0
        width = self.width/len(self.commands)
        for label in self.commands:
            x = self.x + i*width
            x2 = self.x + i*width + width
            gl.glColor3f(*self.color)
            graphics.draw(2, gl.GL_LINES, ('v2i', (x, self.y, x, self.y+self.height)))
            graphics.draw(2, gl.GL_LINES, ('v2i', (x2, self.y, x2, self.y+self.height)))
            i += 1
        '''
            
    def on_click(self, model, button, modifiers):
        action = State.commands().get(CommandBar.ACTIONS[self.selection_x]).action
        if action is not None:
            action(model)
