'''
Created on Apr 9, 2013

@author: Devindra
'''
from pyglet import text
from regicide.entity.actions import action
from regicide.controller.hotspot import Hotspot
from regicide.view.view import View, ActiveListLayer
from regicide.mvc import State
from regicide.controller import functions

class ActionsView(View):
    FONT_NAME = View.FONT_NAME
    FONT_SIZE = 13
    FONT_RATIO = View.FONT_RATIO
    
    DESCRIPTION_FONT_SIZE = FONT_SIZE - 2

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

class ActionsLayer(ActiveListLayer):
    
    def __init__(self, x, y, width, height):
        ActiveListLayer.__init__(self, x, y, width, height, ActionsView.FONT_NAME, ActionsView.FONT_SIZE, ActionsView.LINE_HEIGHT, columns=3, column_width=250)
        self.title = text.Label(font_name=ActionsView.FONT_NAME, font_size=ActionsView.FONT_SIZE, x=800, y=height-50, batch=self.batches)
        self.description = text.Label(font_name=ActionsView.FONT_NAME, font_size=ActionsView.DESCRIPTION_FONT_SIZE, x=820, y=height-70, width=300, multiline=True, batch=self.batches)
        
    def update(self, components = None):
        ActiveListLayer.update(self, components)
        
        player = State.model().player
        
        slots = self.rows * self.columns
        i = 0
        for action in player.actions:
            if i < slots:
                x = i / self.rows
                y = i - self.columns*x
                
                self.items[x][y].text = action.name
                self.items[x][y].action = action
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
            action = tile.action
            title = action.name
            text = action.description
        
        self.title.text = title
        self.description.text = text
        
    def on_click(self, model, button, modifiers):
        player = State.model().player
        index = self.selection_y
        functions.set_state(model, 'game')
        State.model().execute_action(action.ActionInstance(
            action = player.actions[index],
            source = model.player,
        ))
        
    # override
    def get_hover_type(self, x, y):
        return Hotspot.HOVER_DEFAULT
        
        