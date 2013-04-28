'''
Created on Apr 27, 2013

@author: Devindra
'''
import abc

EVENT_HANDLED = True
EVENT_CANCELED = False
EVENT_UNHANDLED = None

class Dispatcher(object):
    __metaclass__ = abc.ABCMeta
        
    @classmethod
    def register_dispatch_type(cls, dispatch_type):
        if not hasattr(cls, 'event_types'):
            cls.handlers = {}
        
        cls.handlers[dispatch_type] = []
        
    def add_handler(self, handler, priority=0):
        for dispatch_type in self.handlers.iterkeys():
            if hasattr(handler, dispatch_type):
                self.handlers[dispatch_type].append(handler)
    
    def remove_handler(self, handler):
        for dispatch_type in self.handlers.iterkeys():
            if hasattr(handler, dispatch_type):
                self.handlers.remove(handler)
    
class EventDispatcher(Dispatcher):
        
    def dispatch_event(self, event_type, *args):
        for handler in self.handlers[event_type]:
            func = getattr(handler, event_type)
            response = func(*args)
            
            if (response is not EVENT_UNHANDLED):
                return response
        
        return EVENT_UNHANDLED

class FilterDispatcher(Dispatcher):
        
    def filter(self, filter_type, value, *args):
        for handler in self.handlers[filter_type]:
            func = getattr(handler, filter_type)
            value = func(value, *args)
        
        return value
    