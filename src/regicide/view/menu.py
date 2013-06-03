'''
Created on 2013-06-01

@author: Devindra
'''
from regicide.view.view import View, ActiveListLayer

class MenuView(View):
    FONT_NAME = View.FONT_NAME
    FONT_SIZE = View.FONT_SIZE
    FONT_RATIO = View.FONT_RATIO

    def __init__(self, window):
        '''
        Constructor
        '''
        View.__init__(self, window)
        

class MenuLayer(ActiveListLayer):
    def __init__(self, x, y, width, height, tile_width, tile_height, color):
        ActiveListLayer.__init__(self, x, y, width, height, color)
        
    def draw(self):
        ActiveListLayer.draw(self);