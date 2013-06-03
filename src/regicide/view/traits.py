'''
Created on Apr 9, 2013

@author: Devindra
'''
from pyglet import text
from regicide.controller.hotspot import Hotspot
from regicide.view.view import View, ListLayer, ActiveListLayer
from regicide.mvc import State

class TraitsView(View):
    FONT_NAME = View.FONT_NAME
    FONT_SIZE = 13
    FONT_RATIO = View.FONT_RATIO
    
    DESCRIPTION_FONT_SIZE = 2
    MODIFIERS_FONT_SIZE = DESCRIPTION_FONT_SIZE
    
    LINE_HEIGHT = 18
    GUTTER = 10

    def __init__(self, window):
        View.__init__(self, window)
        
        x = TraitsView.GUTTER
        y = TraitsView.GUTTER
        width = window.width - TraitsView.GUTTER*2
        height = window.height - TraitsView.GUTTER*2
        layer = TraitsLayer(x, y, width, height)
        self.layers.append(layer)

class TraitsLayer(ActiveListLayer):
    DESC_FONT = '<font face="'+TraitsView.FONT_NAME+'" size="'+str(TraitsView.DESCRIPTION_FONT_SIZE)+'" color="white">'
    MOD_FONT = '<font face="'+TraitsView.FONT_NAME+'" size="'+str(TraitsView.MODIFIERS_FONT_SIZE)+'" color="white">'
    
    def __init__(self, x, y, width, height):
        ActiveListLayer.__init__(self, x, y, width, height, TraitsView.FONT_NAME, TraitsView.FONT_SIZE, TraitsView.LINE_HEIGHT, columns=3, column_width=250)
        self.title = text.Label(font_name=TraitsView.FONT_NAME, font_size=TraitsView.FONT_SIZE, x=800, y=height-50, batch=self.batches)
        self.description = text.HTMLLabel(x=820, y=height-70, width=300, multiline=True, batch=self.batches)
        
    def update(self, components = None):
        ActiveListLayer.update(self, components)
        
        player = State.model().player
        
        slots = self.rows * self.columns
        i = 0
        for trait in player.traits:
            if (i < slots):
                x = i / self.rows
                y = i - self.columns*x
                
                self.items[x][y].text = trait.name
                self.items[x][y].trait = trait
                i += 1
            else:
                break;
        
    # override
    def update_cursor(self):
        ActiveListLayer.update_cursor(self)
        
        if self.has_focus:
            self.update_description(self.items[self.selection_x][self.selection_y])
        
    def update_description(self, tile):
        title = ""
        text = ""
        if (tile.text != ""):
            trait = tile.trait
            title += trait.name
            text += TraitsLayer.DESC_FONT+trait.description+"</font>"
            text += "<br /><br />"
            
            text += TraitsLayer.MOD_FONT
            for prop, modifier in trait.modifiers.iteritems():
                text += "  "+modifier[0]+str(modifier[1])+" "+prop.name+"<br />"
            text += "</font>"
        
        self.title.text = title
        self.description.text = text
            
    # override
    def get_hover_type(self, x, y):
        return Hotspot.HOVER_DEFAULT

