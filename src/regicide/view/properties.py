'''
Created on Apr 9, 2013

@author: Devindra
'''
from pyglet import text
from regicide.controller.hotspot import Hotspot
from regicide.view.view import View, ListLayer, ActiveListLayer
from regicide.mvc import State
from regicide.entity import properties

class PropertiesView(View):
    FONT_NAME = View.FONT_NAME
    FONT_SIZE = 13
    FONT_RATIO = View.FONT_RATIO

    MODS_FONT_SIZE = FONT_SIZE - 2
    
    LINE_HEIGHT = 18
    GUTTER = 10

    def __init__(self, window):
        '''
        Constructor
        '''
        View.__init__(self, window)
        
        x = PropertiesView.GUTTER
        y = PropertiesView.GUTTER
        width = window.width - PropertiesView.GUTTER*2
        height = window.height - PropertiesView.GUTTER*2
        layer = PropertiesLayer(x, y, width, height)
        self.layers.append(layer)

class PropertiesLayer(ActiveListLayer):
    
    def __init__(self, x, y, width, height):
        ActiveListLayer.__init__(self, x, y, width, height, PropertiesView.FONT_NAME, PropertiesView.FONT_SIZE, PropertiesView.LINE_HEIGHT, columns=4, column_width=180)
        self.title = text.Label(font_name=PropertiesView.FONT_NAME, font_size=PropertiesView.FONT_SIZE, x=800, y=height-50, batch=self.batches)
        self.modifiers = text.Label(font_name=PropertiesView.FONT_NAME, font_size=PropertiesView.MODS_FONT_SIZE, x=800, y=height-70, width=250, multiline=True, batch=self.batches)
        
    def update(self, components = None):
        ActiveListLayer.update(self, components)
        
        player = State.model().player
        
        slots = self.rows * self.columns
        i = 0
        for prop in properties.Property.all:
            if (i < slots):
                x = i / self.rows
                y = self.rows - (i - self.rows*x) - 1
                
                name = prop.name
                value = str(player.get(prop))
                spacing = " "*(19 - len(prop.name) + 3 - len(value))
                
                self.items[x][y].text = name + spacing + value
                self.items[x][y].prop = prop
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
            prop = tile.prop
            player = State.model().player
            modifiers = player.get_property_modifiers(prop)
            title = prop.name+" "+str(player.get(prop))
            
            if (type(prop.base) == properties.Property):
                text += "   0\n"
                modifier = str(player.get(prop.base))
                spacing = " "*(2 - len(modifier))
                name = prop.base.name
                
                text += " +"+spacing+modifier+", "+name+"\n"
            else:
                modifier = str(player.get(prop, True))
                spacing = " "*(2 - len(modifier))
                text += "  "+spacing+modifier+"\n"
            
            for modifier in modifiers:
                value = modifier[0]
                if value < 0:
                    sign = "-"
                    value = str(abs(value))
                else:
                    sign = "+"
                    value = str(value)
                
                spacing = " "*(2 - len(value))
                source = modifier[1]
                
                text += " "+sign+spacing+value+", "+source+"\n"
        
        self.title.text = title
        self.modifiers.text = text
            
    # override
    def get_hover_type(self, x, y):
        return Hotspot.HOVER_DEFAULT
        
        