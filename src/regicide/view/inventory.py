'''
Created on Apr 9, 2013

@author: Devindra
'''
from pyglet import text
from pyglet.window import mouse
from regicide.controller import functions
from regicide.controller.hotspot import Hotspot
from regicide.view.view import View, ActiveListLayer
from regicide.mvc import State

class InventoryView(View):
    FONT_NAME = View.FONT_NAME
    FONT_SIZE = 13
    FONT_RATIO = View.FONT_RATIO

    HEADER_FONT_SIZE = FONT_SIZE - 2
    
    DESCRIPTION_FONT_SIZE = 2
    STATS_FONT_SIZE = DESCRIPTION_FONT_SIZE
    
    LINE_HEIGHT = 18
    GUTTER = 10

    DESC_FONT = '<font face="'+FONT_NAME+'" size="'+str(DESCRIPTION_FONT_SIZE)+'" color="white">'
    STAT_FONT = '<font face="'+FONT_NAME+'" size="'+str(STATS_FONT_SIZE)+'" color="white">'

    def __init__(self, window):
        View.__init__(self, window)
        
        x = InventoryView.GUTTER
        y = InventoryView.GUTTER
        width = 380
        height = window.height - InventoryView.GUTTER*2
        layer = EquipmentLayer(x, y, width, height)
        self.layers.append(layer)
        
        x = width + InventoryView.GUTTER*2 + 15
        width = 400
        layer = InventoryLayer(x, y, width, height)
        self.layers.append(layer)

class ItemListLayer(ActiveListLayer):
    
    def __init__(self, title, x, y, width, height, header, description_y, columns=1):
        height -= 50
        
        ActiveListLayer.__init__(self, x, y, width, height, InventoryView.FONT_NAME, InventoryView.FONT_SIZE, InventoryView.LINE_HEIGHT, columns=columns, column_width=width/columns)
        
        text.Label(text=title, color=(255, 127, 80, 255), font_name=InventoryView.FONT_NAME, font_size=InventoryView.FONT_SIZE, x=x, y=height+34, batch=self.batches)
        text.Label(text=header, color=(150, 150, 150, 255), font_name=InventoryView.FONT_NAME, font_size=InventoryView.HEADER_FONT_SIZE, x=x, y=height+15, batch=self.batches)
        
        self.title = text.Label(font_name=InventoryView.FONT_NAME, font_size=InventoryView.FONT_SIZE, x=850, y=height-description_y, batch=self.batches)
        self.description = text.HTMLLabel(x=870, y=height-description_y-20, width=300, multiline=True, batch=self.batches)
        
    def update(self, components = None):
        ActiveListLayer.update(self, components)
        self.update_list()
        
    # override
    def update_cursor(self):
        # We're specifically not calling the base function that we are overriding.
        if self.has_focus:
            tile = self.items[self.selection_x][self.selection_y]
            if tile.text != "":
                for column in self.items:
                    for label in column:
                        label.bold = False
                        
                tile.bold = True
                self.update_description(tile)
            
    def update_list(self):
        self.clear()
        
    def update_description(self, tile):
        item = tile.item
        title = item.name
        text = InventoryView.DESC_FONT+item.description+"</font><br /><br />"
        
        '''
        text += InventoryView.STAT_FONT
        for prop, modifier in item.properties['modifiers'].iteritems():
            text += "  "+modifier[0]+str(modifier[1])+" "+prop.name+"<br />"
        text += "</font>"
        '''
    
        self.title.text = title
        self.description.text = text
            
    def on_click(self, model, button, modifiers):
        tile = self.items[self.selection_x][self.selection_y]
        if button == mouse.LEFT and modifiers == 0 and tile.text != "":
            functions.toggle_equip(model, tile.item)
            
    # override
    def get_hover_type(self, x, y):
        if self.items[x][y].text != "":
            return Hotspot.HOVER_CLICK
        else:
            return Hotspot.HOVER_DEFAULT

class InventoryLayer(ItemListLayer):
    NAME_COLUMN = 0
    TYPE_COLUMN = 20
    SLOT_COLUMN = 30
    SIZE_COLUMN = 38
    WEIGHT_COLUMN = 45
    
    def __init__(self, x, y, width, height):
        header = ""
        header += " " * (InventoryLayer.NAME_COLUMN - len(header))
        header += "Name"
        header += " " * (InventoryLayer.TYPE_COLUMN - len(header))
        header += "Type"
        header += " " * (InventoryLayer.SLOT_COLUMN - len(header))
        header += "Slot"
        header += " " * (InventoryLayer.SIZE_COLUMN - len(header))
        header += "Size"
        header += " " * (InventoryLayer.WEIGHT_COLUMN - len(header))
        header += "Weight"
        
        ItemListLayer.__init__(self, "Inventory", x, y, width, height, header, columns=1, description_y=0)
        
    def update_list(self):
        ItemListLayer.update_list(self)
        
        player = State.model().player

        i = 0
        for item in player.inventory:
            if item not in player.equipment[item.equip_slot]:
                x = i / self.rows
                y = self.rows - (i - self.rows*x) - 1
                
                text = ""
                text += " " * (InventoryLayer.NAME_COLUMN - len(text))
                text += item.name
                text += " " * (InventoryLayer.TYPE_COLUMN - len(text))
                text += item.type
                text += " " * (InventoryLayer.SLOT_COLUMN - len(text))
                text += item.equip_slot.name
                text += " " * (InventoryLayer.SIZE_COLUMN - len(text))
                text += str(item.equip_size)
                text += " " * (InventoryLayer.WEIGHT_COLUMN - len(text))
                text += str(item.weight)
                
                self.items[x][y].text = text
                self.items[x][y].item = item
                
                if player.could_equip(item):
                    self.items[x][y].disabled = False
                    self.items[x][y].color = (255, 255, 255, 255)
                else:
                    self.items[x][y].disabled = True
                    self.items[x][y].color = (188, 143, 143, 255)
                
                i += 1
    
    #override
    def update_description(self, tile):
        ItemListLayer.update_description(self, tile)
        
        #TODO: the following isn't working atm
        if State.model().player.could_equip(tile.item) is False:
            text = self.description.text
            text += "You cannot equip this item, because your "+tile.item.equip_slot.name+" slot does not have "+str(tile.item.equip_size)+" space."
            self.description.text = text
                
    # override
    def get_hover_type(self, x, y):
        item = self.items[x][y]
        if hasattr(item, 'disabled') and item.disabled is True:
            return Hotspot.HOVER_DEFAULT
        else:
            return ItemListLayer.get_hover_type(self, x, y)

class EquipmentLayer(ItemListLayer):
    NAME_COLUMN = 0
    TYPE_COLUMN = 20
    SLOT_COLUMN = 30
    WEIGHT_COLUMN = 42
    
    def __init__(self, x, y, width, height):
        header = ""
        header += " " * (EquipmentLayer.NAME_COLUMN - len(header))
        header += "Name"
        header += " " * (EquipmentLayer.TYPE_COLUMN - len(header))
        header += "Type"
        header += " " * (EquipmentLayer.SLOT_COLUMN - len(header))
        header += "Slot"
        header += " " * (EquipmentLayer.WEIGHT_COLUMN - len(header))
        header += "Weight"
        
        ItemListLayer.__init__(self, "Equipment", x, y, width, height, header, description_y=300)
        
    def update_list(self):
        ItemListLayer.update_list(self)
        
        player = State.model().player
        
        i = 0
        for equip_slot, items in player.equipment.iteritems():
            n = 0
            for item in items:
                x = i / self.rows
                y = self.rows - (i - self.columns*x) - 1
                
                text = ""
                text += " " * (EquipmentLayer.NAME_COLUMN - len(text))
                text += item.name
                text += " " * (EquipmentLayer.TYPE_COLUMN - len(text))
                text += item.type
                text += " " * (EquipmentLayer.SLOT_COLUMN - len(text))
                text += str(item.equip_slot.get_slot_description(n))
                text += " " * (EquipmentLayer.WEIGHT_COLUMN - len(text))
                text += str(item.weight)
                
                self.items[x][y].text = text
                self.items[x][y].item = item
                i += 1
                n += 1
        
        
        