'''
Created on Apr 6, 2013

@author: Devindra
'''

class Hotspot(object):
    '''
    A hotspot is an on screan area that reacts to the player 
    moving their mouse or clicking within it's bounds.
    '''
    HOVER_HIDDEN = 0 # Hide the mouse when hovering.
    HOVER_CLICK = 1 # Use the pointer mouse when hovering.
    HOVER_DEFAULT = 2 # Use the default mouse.

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
        '''
        Triggered when the mouse enter's this hotspot's area.
        '''
        self.has_focus = True
    
    def on_focus_lost(self, model):
        '''
        Triggered when the mouse leave's this hotspot's area.
        '''
        self.has_focus = False
        model.do_update('cursor') # Trigger a cursor update so that elements of the hotspot can be deselected as needed.
        
    def on_hover(self, model, mouse_x, mouse_y):
        '''
        Triggered when the mouse moves within the bounds of this hotspot.
        '''
        prev_select_x = self.selection_x
        prev_select_y = self.selection_y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        
        if prev_select_x != self.selection_x or prev_select_y != self.selection_y or not self.has_focus:
            self.on_select(model, self.selection_x, self.selection_y)
        
    def on_select(self, model, selection_x, selection_y):
        '''
        Triggered when the mouse's selection changes.
        ie. when the mouse is hovering over a different segment of the hotspot
        from what it was hovering over last update.
        '''
        model.do_update('cursor')
        
    @property
    def selection_x(self):
        '''
        Get the x coordinate of the hotspot tile (segment) that is currently selected.
        '''
        return int((self.mouse_x - self.x) / (self.width / self.columns))
    
    @property
    def selection_y(self):
        '''
        Get the y coordinate of the hotspot tile (segment) that is currently selected.
        '''
        return int((self.height - (self.mouse_y - self.y)) / (self.height / self.rows))
            
    def on_click(self, model, button, modifiers):
        '''
        Triggered when the user clicks their mouse, even if this hotspot does not have focus.
        Make sure you check if hotspot.has_focus, before performing any actions!
        '''
        pass
    
    def get_hover_type(self, x, y):
        '''
        :return: the type of mouse to display when hovering over the given location in this hotspot.
        '''
        return self.hover_type
    
    def contains(self, x, y):
        '''
        :return: whether or not this hotspot contains the given coordinates.
        '''
        return x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height
    
    def is_game_layer(self):
        '''
        This method should always return false, except when it is overridden by the GameHotspot class.
        This code structure is being used primarily to avoid import loops.
        '''
        return False
    
