'''
Created on Mar 20, 2013

@author: Devindra

Defines various layers/blocks that are used to compose the game view.
'''
from pyglet import graphics
from pyglet import text
from pyglet import gl
from regicide.controller.hotspot import Hotspot
from regicide.mvc import State

class View(object):
    FONT_NAME = "Courier New"
    FONT_SIZE = 10
    FONT_RATIO = 1.45
    
    def __init__(self, window):
        self.layers = []
        
    def update_all(self):
        for layer in self.layers:
            layer.update()
    
    def refresh(self, window):
        self.__init__(window)
    
    @property
    def hotspots(self):
        hotspots = []
        for layer in self.layers:
            if (isinstance(layer, Hotspot)):
                hotspots.append(layer)
        
        return hotspots

class Layer(object):
    def __init__(self, x, y, width, height, color):
        '''
        Constructor
        '''
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color # TODO: remove this test code
        self.batches = []
    
    def update(self, components = None):
        pass

    def draw(self):
        if type(self.batches) is list:
            for batch in self.batches:
                batch.draw();
        else:
            self.batches.draw()
            
class ListLayer(Layer):
    def __init__(self, x, y, width, height, font_name=View.FONT_NAME, font_size=View.FONT_SIZE, line_height=(View.FONT_SIZE*1.2), columns=1, column_width=None):
        Layer.__init__(self, x, y, width, height, [100.0, 100.0, 100.0])
        
        self.batches = graphics.Batch()
        self.items = []
        
        self.rows = int(self.height / line_height)
        self.columns = columns
        
        if (column_width is None):
            self.column_width = width / columns
        else:
            self.column_width = column_width
            
        self.line_height = line_height
        
        for col in range(columns):
            column = []
            for i in range(self.rows):
                column.append(text.Label(font_name=View.FONT_NAME, font_size=View.FONT_SIZE, x=x+col*self.column_width, y=y+i*line_height, width=column_width, batch=self.batches))
            
            self.items.append(column)
    
    def update(self, components = None):
        Layer.update(self, components)
    
    def clear(self):
        for column in self.items:
            for item in column:
                item.text = ""

class ActiveListLayer(ListLayer, Hotspot):
    def __init__(self, x, y, width, height, font_name=View.FONT_NAME, font_size=View.FONT_SIZE, line_height=(View.FONT_SIZE*1.2), columns=1, column_width=None):
        ListLayer.__init__(self, x, y, width, height, font_name, font_size, line_height, columns, column_width)
        Hotspot.__init__(self, x, y, self.column_width*self.columns, self.line_height*self.rows, rows=self.rows, columns=self.columns)
    
    def update(self, components = None):
        ListLayer.update(self, components)
        if (components is None or 'cursor' in components):
            self.update_cursor();
        
    def update_cursor(self):
        for column in self.items:
            for label in column:
                label.bold = False
        
        if self.has_focus:
            self.items[self.selection_x][self.selection_y].bold = True
    
    def draw(self):
        Layer.draw(self)
        
        '''
        index_x = 0
        index_y = 0
        line_height = self.height / self.rows
        for column in self.items:
            index_y = 0
            for cell in column:
                x = self.x + index_x*self.column_width
                y = self.y + index_y*line_height
                y2 = self.y + index_y*line_height + line_height
                
                gl.glColor3f(*self.color)
                graphics.draw(2, gl.GL_LINES, ('v2i', (x, y, x+self.column_width-5, y)))
                graphics.draw(2, gl.GL_LINES, ('v2i', (x, y2, x+self.column_width-5, y2)))
                index_y += 1
            index_x += 1
        '''
    
    # override
    def get_hover_type(self, x, y):
        if (self.items[x][y].text != ""):
            return Hotspot.HOVER_CLICK
        else:
            return Hotspot.HOVER_DEFAULT
