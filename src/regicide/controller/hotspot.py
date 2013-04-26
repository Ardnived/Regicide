'''
Created on Apr 6, 2013

@author: Devindra
'''

class Hotspot(object):
    HOVER_HIDDEN = 0
    HOVER_CLICK = 1
    HOVER_DEFAULT = 2

    def __init__(self, x, y, width, height, rows=1, columns=1, hover_type=HOVER_DEFAULT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rows = rows
        self.columns = columns
        self.hover_type = hover_type
            
    def on_click(self, model, row, column, button, modifiers):
        pass
    
    def get_hover_type(self, x, y):
        return self.hover_type
    
    def get_tile(self, x, y):
        if (x < self.x or x >= self.x + self.width
            or y < self.y or y >= self.y + self.height):
            return None
        else:
            tile_width = self.width / self.columns
            tile_height = self.height / self.rows
            
            tile_x = (x - self.x) / tile_width
            tile_y = (y - self.y) / tile_height
            return [tile_x, tile_y]
    
