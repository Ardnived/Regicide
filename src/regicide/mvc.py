'''
Created on Apr 13, 2013

@author: Devindra
'''

class State(object):
    _current = None
    _all = {}
    _links = {}
    
    @staticmethod
    def exists():
        return State._current is not None
    
    @staticmethod
    def model():
        if (State.exists()):
            return State._current.model
        else:
            return None
    
    @staticmethod
    def view():
        if (State.exists()):
            return State._current.view
        else:
            return None
    
    @staticmethod
    def controller():
        if (State.exists()):
            return State._current.controller
        else:
            return None
    
    @staticmethod
    def commands():
        if (State.exists()):
            return State._current.commands
        else:
            return None
    
    @staticmethod
    def window():
        if (State.exists()):
            return State._current.window
        else:
            return None
    
    @staticmethod
    def set_current(slug):
        state = State._all[slug]
        State._current = state
        state.model.do_update('all')

    def __init__(self, slug, window, model, view, controller, commands):
        print("Initializing State: "+slug)
        self.window = window
        self.model = model
        self.view = view
        self.controller = controller
        self.commands = commands
        
        self.set_handler(window, controller)
        self.set_handler(controller, model)
        self.set_handler(model, window)
        
        State._all[slug] = self
        
    def set_handler(self, source, handler):
        if (State._links.has_key(source) is False):
            source.push_handlers(handler)
            State._links[source] = handler
        elif (State._links[source] != handler):
            print("Linking Collision: "+str(handler)+" was not assigned to handle "+str(source)+" (mvc.py)")
            

