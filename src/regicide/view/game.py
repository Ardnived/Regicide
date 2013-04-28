'''
Created on Apr 6, 2013

@author: Devindra
'''
from regicide.view.view import View, Layer
from pyglet import graphics
from pyglet import text
from pyglet import sprite
from pyglet import gl
from regicide.resources import visual
from regicide.entity import properties
from regicide.controller.hotspot import Hotspot
from regicide.controller.game import GameHotspot
from regicide.controller import commands
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
    
    LOG_LINE_HEIGHT = 15
    LOG_FONT_SIZE = FONT_SIZE
    LOG_LINE_QUANTITY = (LOWER_BAR_HEIGHT - LOWER_BAR_GUTTER_Y*2) / LOG_LINE_HEIGHT
    
    LOWER_BAR_LINE_HEIGHT = 15
    LOWER_BAR_FONT_SIZE = 11
    LOWER_BAR_LINE_QUANTITY = (LOWER_BAR_HEIGHT - LOWER_BAR_GUTTER_Y*2) / LOWER_BAR_LINE_HEIGHT
    
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
        inv_layer = Inventory(inv_x, log_y, log_width, log_height)
        self.layers.append(inv_layer)
        
        # Create the inventory window
        act_x = inv_x + log_width + GameView.LOWER_BAR_GUTTER_X
        act_layer = Actions(act_x, log_y, log_width, log_height)
        self.layers.append(act_layer)
        
        # Create the info window
        info_x = window.width - (GameView.INFO_WIDTH + GameView.INFO_GUTTER_X*2)
        info_y = GameView.LOWER_BAR_HEIGHT
        info_width = GameView.INFO_WIDTH
        info_height = window.height - GameView.LOWER_BAR_HEIGHT - GameView.INFO_GUTTER_Y
        info_layer = PlayerCard(info_x, info_y, info_width, info_height)
        self.layers.append(info_layer)
    
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
        if (ascii is True):
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
        
        GameHotspot.__init__(self, x, y, width, height, self.grid_height, self.grid_width, hover_type=Hotspot.HOVER_HIDDEN)
       
    def draw(self):
        Layer.draw(self);
        if (self.show_cursor):
            self.cursor.draw();
    
    def update(self, components = None):
        if (components is None or 'cursor' in components):
            self.update_cursor();
        
    def update_cursor(self):
        model = State.model()
        selection = model.selection
        
        if (selection is not None and selection[2] == self):
            grid_width = self.width / self.tile_width
            grid_height = self.height / self.tile_height
            grid_x = model.player.x - grid_width/2
            grid_y = model.player.y - grid_height/2
            x = selection[0]
            y = selection[1]
            tile = model.map.get_tile(x + grid_x, y + grid_y)
            
            if (tile is not None):
                if (tile.entity is not None):
                    self.cursor.image = visual.Cursor.get(visual.Cursor.YELLOW)
                else:
                    if (tile.is_passable()):
                        self.cursor.image = visual.Cursor.get(visual.Cursor.SELECT)
                    else:
                        self.cursor.image = visual.Cursor.get(visual.Cursor.TARGET)
            else:
                self.cursor.image = visual.Cursor.get(visual.Cursor.TARGET)
            
            self.cursor.x = x * self.tile_width + self.x
            self.cursor.y = y * self.tile_height + self.y
            self.show_cursor = True
        else:
            self.show_cursor = False
            
    def update_game_bounds(self):
        self.grid_x = State.model().player.x - self.grid_width/2
        self.grid_y = State.model().player.y - self.grid_height/2

class TileGame(GameLayer):
    def __init__(self, x, y, width, height):
        GameLayer.__init__(self, x, y, width, height, 32, 32, [0.0, 0.0, 255.0])
    
    def update(self, components = None):
        GameLayer.update(self, components)
        
        if (components is None or 'tiles' in components):
            self.update_game_bounds()
            self.update_tiles();
            
        if (components is None or 'entities' in components):
            self.update_entities();

        if (components is None or 'shadows' in components):
            self.update_shadows();
        
    def update_tiles(self):
        if (hasattr(self, 'tile_layer')):
            self.batches.remove(self.tile_layer)
        self.tile_layer = graphics.Batch()
        self.batches.append(self.tile_layer)
        model = State.model()
        grid = model.map.grid
        
        for x in range(max(0, self.grid_x), min(self.grid_x + self.grid_width, len(grid))):
            for y in range(max(0, self.grid_y), min(self.grid_y + self.grid_height, len(grid[x]))):
                tile = grid[x][y]
                if (tile is not None):
                    sprite = tile.sprite
                    sprite.batch = self.tile_layer
                    sprite.x = x*self.tile_width - self.grid_x*self.tile_width + self.x
                    sprite.y = y*self.tile_height - self.grid_y*self.tile_width + self.y
        
    def update_entities(self):
        if (hasattr(self, 'entity_layer')):
            self.batches.remove(self.entity_layer)
        self.entity_layer = graphics.Batch()
        self.batches.append(self.entity_layer)
        model = State.model()
        grid = model.map.grid
        
        for x in range(max(0, self.grid_x), min(self.grid_x + self.grid_width, len(grid))):
            for y in range(max(0, self.grid_y), min(self.grid_y + self.grid_height, len(grid[x]))):
                tile = grid[x][y]
                if (tile is not None and tile.entity is not None):
                    sprite = tile.entity.sprite
                    sprite.color = [255, 100, 100]
                    sprite.batch = self.entity_layer
                    sprite.x = x*self.tile_width - self.grid_x*self.tile_width + self.x
                    sprite.y = y*self.tile_height - self.grid_y*self.tile_height + self.y
        
    def update_shadows(self):
        if (hasattr(self, 'shadow_layer')):
            self.batches.remove(self.shadow_layer)
        self.shadow_layer = graphics.Batch()
        self.batches.append(self.shadow_layer)
        model = State.model()
        grid = model.map.grid
        
        for x in range(max(0, self.grid_x), min(self.grid_x + self.grid_width, len(grid))):
            for y in range(max(0, self.grid_y), min(self.grid_y + self.grid_height, len(grid[x]))):
                tile = grid[x][y]
                if (tile is not None and tile.no_shadow is False):
                    sprite = grid[x][y].shadow
                    sprite.batch = self.shadow_layer
                    sprite.x = x*self.tile_width - self.grid_x*self.tile_width + self.x
                    sprite.y = y*self.tile_height - self.grid_y*self.tile_height + self.y


class AsciiGame(GameLayer):
    TILE_SIZE = 20
    
    def __init__(self, x, y, width, height):
        GameLayer.__init__(self, x, y, width, height, self.TILE_SIZE, self.TILE_SIZE, [0.0, 0.0, 255.0])
        self.cursor.scale = float(self.TILE_SIZE / 32.0)
        
    def update(self, components = None):
        GameLayer.update(self, components)
        
        if (components is None or 'tiles' in components or 'entities' in components or 'shadows' in components):
            self.update_game_bounds()
            self.update_grid()
        
    def update_grid(self):
        self.batches = graphics.Batch()
        model = State.model()
        grid = model.map.grid
        
        for x in range(max(0, self.grid_x), min(self.grid_x + self.grid_width, len(grid))):
            for y in range(max(0, self.grid_y), min(self.grid_y + self.grid_height, len(grid[x]))):
                tile = grid[x][y]
                if (tile is not None):
                    if (tile.entity is None):
                        sprite = tile.ascii
                    else:
                        sprite = tile.entity.ascii
                        sprite.color = [100, 100, 255]
                    
                    sprite.batch = self.batches
                    sprite.x = self.x + (x*self.tile_width - self.grid_x*self.tile_width)
                    sprite.y = self.y + (y*self.tile_height - self.grid_y*self.tile_height)


class Log(Layer):
    def __init__(self, x, y, width, height):
        Layer.__init__(self, x, y, width, height, [0.0, 255.0, 255.0])
        
        self.batches = graphics.Batch()
        self.log = []
        self.max_chars = int(width / GameView.LOG_FONT_SIZE * GameView.FONT_RATIO)
        
        for i in range(GameView.LOG_LINE_QUANTITY):
            self.log.append(text.Label(font_name=GameView.FONT_NAME, font_size=GameView.LOG_FONT_SIZE, x=x, y=y+i*GameView.LOG_LINE_HEIGHT, batch=self.batches))
        
    def update(self, components = None):
        model = State.model()
        
        if (components is None or 'log' in components):
            for i in range(min(len(model.log), len(self.log))):
                self.log[i].text = model.log[i+model.log_offset]


class PlayerCard(Layer):
    def __init__(self, x, y, width, height):
        Layer.__init__(self, x, y, width, height, [0.0, 255.0, 0.0])
        
        self.batches = graphics.Batch()
        self.portrait = sprite.Sprite(visual.Character.HELENA, x+5, y+height-250, batch=self.batches)
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
        if (components is None or 'playercard' in components):
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
            
            self.effects.text = ''
            for effect in player.effects:
                name = effect.name
                spacing = " " * (14 - len(name))
                duration = effect.duration
                self.effects.text += name + spacing + str(duration) + '\n'

class Inventory(Layer, Hotspot):
    def __init__(self, x, y, width, height):
        Layer.__init__(self, x, y, width, height, [0.0, 255.0, 255.0])
        
        self.batches = graphics.Batch()
        self.items = []
        
        for i in range(GameView.LOWER_BAR_LINE_QUANTITY):
            self.items.append(text.Label(font_name=GameView.FONT_NAME, font_size=GameView.LOWER_BAR_FONT_SIZE, x=x, y=y+i*GameView.LOWER_BAR_LINE_HEIGHT, batch=self.batches))
            
        Hotspot.__init__(self, x, y, width, height, rows=GameView.LOWER_BAR_LINE_QUANTITY)
        
    def update(self, components = None):
        if (components is None or 'inventory' in components):
            player = State.model().player
            
            for i in range(min(len(player._inventory), len(self.items))):
                index = GameView.LOWER_BAR_LINE_QUANTITY - i - 1
                self.items[index].text = player._inventory[i].properties['name']
        
        if (components is None or 'cursor' in components):
            self.update_cursor();
        
    def update_cursor(self):
        for label in self.items:
                label.bold = False
        
        selection = State.model().selection
        if (selection is not None and selection[2] == self):
            y = selection[1]
            self.items[y].bold = True
    
    def draw(self):
        Layer.draw(self)
        
        i = 0
        height = self.height/len(self.items)
        for label in self.items:
            y = self.y + i*height
            y2 = self.y + i*height + height
            gl.glColor3f(*self.color)
            graphics.draw(2, gl.GL_LINES, ('v2i', (self.x, y, self.x+self.width, y)))
            graphics.draw(2, gl.GL_LINES, ('v2i', (self.x, y2, self.x+self.width, y2)))
            i += 1
    
    # override
    def get_hover_type(self, x, y):
        if (self.items[y].text != ""):
            return Hotspot.HOVER_CLICK
        else:
            return Hotspot.HOVER_DEFAULT

class Actions(Layer, Hotspot):
    def __init__(self, x, y, width, height):
        Layer.__init__(self, x, y, width, height, [255.0, 255.0, 0.0])
        
        self.batches = graphics.Batch()
        self.items = []
        
        for i in range(GameView.LOWER_BAR_LINE_QUANTITY):
            self.items.append(text.Label(font_name=GameView.FONT_NAME, font_size=GameView.LOWER_BAR_FONT_SIZE, x=x, y=y+i*GameView.LOWER_BAR_LINE_HEIGHT, batch=self.batches))
        
        Hotspot.__init__(self, x, y, width, height, rows=GameView.LOWER_BAR_LINE_QUANTITY)
        
    def update(self, components = None):
        if (components is None or 'actions' in components):
            player = State.model().player
            
            for i in range(min(len(player.actions), len(self.items))):
                index = GameView.LOWER_BAR_LINE_QUANTITY - i - 1
                self.items[index].text = player.actions[i].name
        
        if (components is None or 'cursor' in components):
            self.update_cursor();
        
    def update_cursor(self):
        for label in self.items:
                label.bold = False
        
        selection = State.model().selection
        if (selection is not None and selection[2] == self):
            y = selection[1]
            self.items[y].bold = True
    
    def draw(self):
        Layer.draw(self)
        
        i = 0
        height = self.height/len(self.items)
        for label in self.items:
            y = self.y + i*height
            y2 = self.y + i*height + height
            gl.glColor3f(*self.color)
            graphics.draw(2, gl.GL_LINES, ('v2i', (self.x, y, self.x+self.width, y)))
            graphics.draw(2, gl.GL_LINES, ('v2i', (self.x, y2, self.x+self.width, y2)))
            i += 1
            
    def on_click(self, model, x, y, button, modifiers):
        player = State.model().player
        index = GameView.LOWER_BAR_LINE_QUANTITY - y - 1
        model.log_message("Execute "+player.actions[index].name)
        model.do_update('log')
    
    # override
    def get_hover_type(self, x, y):
        if (self.items[y].text != ""):
            return Hotspot.HOVER_CLICK
        else:
            return Hotspot.HOVER_DEFAULT
           
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
        if (components is None or 'commandbar' in components):
            pass
        
        if (components is None or 'cursor' in components):
            self.update_cursor();
        
    def update_cursor(self):
        for label in self.commands:
                label.bold = False
        
        selection = State.model().selection
        if (selection is not None and selection[2] == self):
            x = selection[0]
            self.commands[x].bold = True

    def draw(self):
        Layer.draw(self)
        
        i = 0
        width = self.width/len(self.commands)
        for label in self.commands:
            x = self.x + i*width
            x2 = self.x + i*width + width
            gl.glColor3f(*self.color)
            graphics.draw(2, gl.GL_LINES, ('v2i', (x, self.y, x, self.y+self.height)))
            graphics.draw(2, gl.GL_LINES, ('v2i', (x2, self.y, x2, self.y+self.height)))
            i += 1
            
    def on_click(self, model, x, y, button, modifiers):
        action = State.commands().get(CommandBar.ACTIONS[x]).action
        if (action is not None):
            action(model)
