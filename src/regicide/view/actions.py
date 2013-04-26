'''
Created on Apr 9, 2013

@author: Devindra
'''
from regicide.view.view import View, ListLayer, ActiveListLayer
from regicide.mvc import State

class ActionsView(View):
    FONT_NAME = View.FONT_NAME
    FONT_SIZE = 13
    FONT_RATIO = View.FONT_RATIO
    
    LINE_HEIGHT = 18
    GUTTER = 10

    def __init__(self, window):
        View.__init__(self, window)
        
        x = ActionsView.GUTTER
        y = ActionsView.GUTTER
        width = window.width - ActionsView.GUTTER*2
        height = window.height - ActionsView.GUTTER*2
        layer = ActionsLayer(x, y, width, height)
        self.layers.append(layer)

class ActionsLayer(ListLayer):
    
    def __init__(self, x, y, width, height):
        ListLayer.__init__(self, x, y, width, height, ActionsView.FONT_NAME, ActionsView.FONT_SIZE, ActionsView.LINE_HEIGHT, columns=3, column_width=250)
        
    def update(self, components = None):
        ListLayer.update(self, components)
        
        player = State.model().player
        
        slots = self.rows * self.columns
        i = 0
        for prop in player.properties:
            if (i < slots):
                x = i / self.rows
                y = self.rows - (i - self.columns*x) - 1
                
                name = prop.name
                value = str(player.get(prop))
                spacing = " "*(20 - len(prop.name) + 3 - len(value))
                
                self.items[x][y].text = "Action"
                i += 1
            else:
                break;
        
        