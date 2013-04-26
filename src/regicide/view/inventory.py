'''
Created on Apr 9, 2013

@author: Devindra
'''
from pyglet import text
from regicide.controller.hotspot import Hotspot
from regicide.view.view import View, ListLayer, ActiveListLayer
from regicide.mvc import State

class InventoryView(View):
    FONT_NAME = View.FONT_NAME
    FONT_SIZE = 13
    FONT_RATIO = View.FONT_RATIO
    
    DESCRIPTION_FONT_SIZE = 2
    STATS_FONT_SIZE = DESCRIPTION_FONT_SIZE
    
    LINE_HEIGHT = 18
    GUTTER = 10

    def __init__(self, window):
        View.__init__(self, window)
        
        x = InventoryView.GUTTER
        y = InventoryView.GUTTER
        width = window.width - InventoryView.GUTTER*2
        height = window.height - InventoryView.GUTTER*2
        layer = InventoryLayer(x, y, width, height)
        self.layers.append(layer)

class InventoryLayer(ActiveListLayer):
    DESC_FONT = '<font face="'+InventoryView.FONT_NAME+'" size="'+str(InventoryView.DESCRIPTION_FONT_SIZE)+'" color="white">'
    STAT_FONT = '<font face="'+InventoryView.FONT_NAME+'" size="'+str(InventoryView.STATS_FONT_SIZE)+'" color="white">'
    
    def __init__(self, x, y, width, height):
        ActiveListLayer.__init__(self, x, y, width, height, InventoryView.FONT_NAME, InventoryView.FONT_SIZE, InventoryView.LINE_HEIGHT, columns=3, column_width=250)
        self.title = text.Label(font_name=InventoryView.FONT_NAME, font_size=InventoryView.FONT_SIZE, x=800, y=height-50, batch=self.batches)
        self.description = text.HTMLLabel(x=820, y=height-70, width=300, multiline=True, batch=self.batches)
        self.actions = text.Label(font_name=InventoryView.FONT_NAME, font_size=InventoryView.FONT_SIZE, x=800, y=height-50, batch=self.batches)
        
    def update(self, components = None):
        ActiveListLayer.update(self, components)
        
        player = State.model().player
        
        slots = self.rows
        i = 0
        for equip_slot, items in player.equipment.iteritems():
            for item in items:
                if (i < slots):
                    x = i / self.rows
                    y = self.rows - (i - self.columns*x) - 1
                    
                    name = item.properties['name']
                    slot_name = equip_slot.name
                    spacing = " "*(10 - len(slot_name))
                    
                    self.items[x][y].text = slot_name + ": " + spacing + name
                    self.items[x][y].item = item
                    i += 1
                else:
                    break;
        
        slots = self.rows * (self.columns - 1)
        i = self.rows
        for item in player.inventory:
            if (i < slots):
                x = i / self.rows
                y = self.rows - (i - self.columns*x) - 1
                
                self.items[x][y].text = item.properties['name']
                self.items[x][y].item = item
                i += 1
            else:
                break;
        
    # override
    def update_cursor(self):
        ActiveListLayer.update_cursor(self)
        
        selection = State.model().selection
        if (selection is not None and selection[2] == self):
            x = selection[0]
            y = selection[1]
            self.update_description(self.items[x][y])
        
    def update_description(self, tile):
        title = ""
        text = ""
        if (tile.text != ""):
            item = tile.item
            title += item.properties['name']
            
            if (item.properties.has_key('description')):
                text += InventoryLayer.DESC_FONT+item.properties['description']+"</font>"
                text += "<br /><br />"
            
            '''
            text += InventoryLayer.STAT_FONT
            for prop, modifier in item.properties['modifiers'].iteritems():
                text += "  "+modifier[0]+str(modifier[1])+" "+prop.name+"<br />"
            text += "</font>"
            '''
        
        self.title.text = title
        self.description.text = text
            
    # override
    def get_hover_type(self, x, y):
        return Hotspot.HOVER_DEFAULT
        
        
        