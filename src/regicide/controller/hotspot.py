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
        self.has_focus = False
        self.mouse_x = 0
        self.mouse_y = 0
        
    def on_focus_gained(self, model):
        self.has_focus = True
    
    def on_focus_lost(self, model):
        self.has_focus = False
        model.do_update('cursor')
        
    def on_hover(self, model, mouse_x, mouse_y):
        prev_select_x = self.selection_x
        prev_select_y = self.selection_y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        
        if prev_select_x != self.selection_x or prev_select_y != self.selection_y or not self.has_focus:
            self.on_select(model, self.selection_x, self.selection_y)
        
    def on_select(self, model, selection_x, selection_y):
        model.do_update('cursor')
        
    @property
    def selection_x(self):
        return (self.mouse_x - self.x) / (self.width / self.columns)
    
    @property
    def selection_y(self):
        return (self.mouse_y - self.y) / (self.height / self.rows)
            
    def on_click(self, model, button, modifiers):
        pass
    
    def get_hover_type(self, x, y):
        return self.hover_type
    
    def contains(self, x, y):
        return x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height
    
    def is_game_layer(self):
        return False
    
