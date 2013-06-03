'''
Created on Mar 4, 2013

@author: Devindra

Handles all the visualization of the game.
This class is the MasterView in the pseudo model-MasterView-controller pattern that this game uses.
'''
from pyglet import graphics
from pyglet import text
from pyglet import gl
from pyglet import window
from regicide.controller.hotspot import Hotspot
from regicide.mvc import State

class MasterView(window.Window):

    def __init__(self):
        '''
        :param model: the model that this MasterView is visualizing.
        '''
        version_name = "Regicide Precursor"
        window.Window.__init__(self, 1240, 700, "Tyrannicide", resizable=False)
        #self.set_location(0, 0)
        
        self.update_components = set(['all'])
        self.version = text.Label(font_name='Courier', text=version_name, font_size=10, x=8, y=self.height-12, color=(100, 100, 100, 255))
    
    def on_draw(self):
        '''
        An event triggered when the window needs to redraw.
        '''
        if self.update_components:
            if 'cursor' in self.update_components:
                self.update_cursor()
            
            self.clear()
            
            if self.update_components != set(['cursor']):
                print(str(self.update_components))
            
            update_all = ('all' in self.update_components)
            for layer in State.view().layers:
                if update_all:
                    layer.update()
                else:
                    layer.update(self.update_components)
            self.update_components = set([])
            
            for layer in State.view().layers:
                layer.draw()
                
                '''
                x = int(layer.x)
                y = int(layer.y)
                x2 = int(x + layer.width)
                y2 = int(y + layer.height)
                gl.glColor3f(*layer.color)
                graphics.draw(2, gl.GL_LINES, ('v2i', (x, y, x2, y)))
                graphics.draw(2, gl.GL_LINES, ('v2i', (x, y, x, y2)))
                graphics.draw(2, gl.GL_LINES, ('v2i', (x2, y, x2, y2)))
                graphics.draw(2, gl.GL_LINES, ('v2i', (x, y2, x2, y2)))
                '''
            
            self.version.draw()
        
    def update(self, component):
        '''
        An update event received from the model when certain components need updating.
        '''
        # Schedule the update to be performed when we redraw.
        self.update_components.add(component)
        
    def update_cursor(self):
        hotspot = State.model().focus
        if hotspot is None:
            self.set_mouse_cursor(self.CURSOR_DEFAULT)
            self.set_mouse_visible(True)
        else:
            hover_type = hotspot.get_hover_type(hotspot.selection_x, hotspot.selection_y)
            
            if (hover_type == Hotspot.HOVER_HIDDEN):
                self.set_mouse_visible(False)
            else:
                if (hover_type == Hotspot.HOVER_CLICK):
                    cursor = self.get_system_mouse_cursor(self.CURSOR_HAND)
                else:
                    cursor = self.get_system_mouse_cursor(self.CURSOR_DEFAULT)
                
                self.set_mouse_cursor(cursor)
                self.set_mouse_visible(True)
    
    def add_layer(self, view, layer):
        '''
        Adds a layer to the specified view, and updates it.
        '''
        self.views[view].append(layer)
        layer.update(self)
    
    def add_view(self, slug):
        '''
        Adds a view to this MasterView.
        '''
        self.views[slug] = []

