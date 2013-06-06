'''
Created on 2013-06-01

@author: Devindra
'''
import random
from pyglet import gl
from regicide.mvc import State
from regicide.level.world import World
from regicide.view.view import View, Layer, ActiveListLayer
from regicide.controller.hotspot import Hotspot

class WorldView(View):
    FONT_NAME = View.FONT_NAME
    FONT_SIZE = View.FONT_SIZE
    FONT_RATIO = View.FONT_RATIO
    
    LINE_HEIGHT = 16
    GUTTER = 10
    
    def __init__(self, window):
        '''
        Constructor
        '''
        View.__init__(self, window)
        
        select_x = WorldView.GUTTER
        select_y = WorldView.GUTTER
        select_width = 180
        select_height = (window.height - WorldView.GUTTER*3 / 2)
        layer = FloorSelectLayer(select_x, select_y, select_width, select_height)
        self.layers.append(layer)
        
        info_y = WorldView.GUTTER
        layer = FloorInfoLayer(select_x, info_y, select_width, select_height)
        self.layers.append(layer)
        
        display_x = select_x + select_width + WorldView.GUTTER
        display_width = window.width - select_width - WorldView.GUTTER*2
        display_height = window.height - WorldView.GUTTER*2
        layer = FloorDisplayLayer(display_x, select_y, display_width, display_height)
        self.layers.append(layer)

class FloorDisplayLayer(Layer, Hotspot):
    
    def __init__(self, x, y, width, height):
        Layer.__init__(self, x, y, width, height)
        
    def update(self, components = None):
        world = State.model().game
        Layer.update(self, components)
        
        Hotspot.__init__(self, self.x, self.y, self.width, self.height, world.rows, world.columns)
        
        if components is None or 'cursor' in components:
            self.update_cursor();
        elif components == None:
            y = 0
            for depth in xrange(-world.depth, world.height):
                floor = World.FLOORS[depth]
                self.items[0][y].text = floor['name']
                self.items[0][y].depth = depth
                y += 1
        
    def update_cursor(self):
        '''
        for column in self.items:
            for label in column:
                label.bold = False
        
        if self.has_focus:
            self.items[self.selection_x][self.selection_y].bold = True
        '''
        pass
    
    def draw(self):
        Layer.draw(self)
        game = State.model()
        world = game.world
        
        cell_width = self.width / world.columns
        cell_height = self.height / world.rows
        
        depth = 0
        
        x = self.x
        for col in xrange(world.columns):
            y = self.y
            for row in xrange(world.rows):
                floor = world.get_floor(col, row, depth)
                
                color = (1.0, 1.0, 1.0)
                
                if game.current_floor_coords == (col, row, depth):
                    color = (0.7, 0.7, 1.0)
                
                if floor is None:
                    opacity = 0
                elif floor.known:
                    opacity = 0.5
                elif floor.explored:
                    opacity = 1.0
                else:
                    opacity = 0
                
                if opacity > 0:
                    self.set_color(*color, opacity=opacity)
                    
                    gl.glRectf(x, y, x + cell_width, y + cell_height)
                
                y += cell_height
            x += cell_width
    
    def set_color(self, r, g, b, opacity=1.0):
        r *= opacity
        g *= opacity
        b *= opacity
        gl.glColor3f(r, g, b)
        

class FloorSelectLayer(ActiveListLayer):
    
    def __init__(self, x, y, width, height):
        ActiveListLayer.__init__(self, x, y, width, height, font_name=WorldView.FONT_NAME, font_size=WorldView.FONT_SIZE, line_height=WorldView.LINE_HEIGHT)
        
        y = 0
        for depth, floor in World.FLOORS.iteritems():
            self.items[0][y].text = floor['name']
            self.items[0][y].depth = depth
            y += 1
    
    # override
    def update_cursor(self):
        # We're specifically not calling the base function that we are overriding.
        if self.has_focus:
            tile = self.items[self.selection_x][self.selection_y]
            if tile.text != "":
                for column in self.items:
                    for label in column:
                        label.bold = False
                        
                tile.bold = True

class FloorInfoLayer(Layer):
    
    def __init__(self, x, y, width, height):
        Layer.__init__(self, x, y, width, height)

