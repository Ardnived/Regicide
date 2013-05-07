'''
Created on Apr 27, 2013

@author: Devindra
'''
import abc
import heapq

EVENT_HANDLED = True
EVENT_CANCELED = False
EVENT_UNHANDLED = None

FILTER_ADD = 0
FILTER_SUBTRACT = 1
FILTER_DIVIDE = 2
FILTER_MULTIPLY = 3
FILTER_SET = 4

class Dispatcher(object):
    __metaclass__ = abc.ABCMeta
        
    @classmethod
    def register_dispatch_type(cls, dispatch_type):
        if not hasattr(cls, 'handlers'):
            cls.handlers = {}
        
        cls.handlers[dispatch_type] = []
        
    def add_handler(self, handler, priority=0):
        for dispatch_type in self.handlers.iterkeys():
            if hasattr(handler, dispatch_type):
                heapq.heappush(self.handlers[dispatch_type], (priority, handler))
    
    def remove_handler(self, handler):
        for dispatch_type, handlers in self.handlers.iteritems():
            if hasattr(handler, dispatch_type):
                for item in handlers:
                    if item[1] == handler:
                        handlers.remove(item)
    
class EventDispatcher(Dispatcher):
        
    def dispatch_event(self, event_type, *args):
        if hasattr(self, event_type):
            func = getattr(self, event_type)
            response = func(*args)
            
            if response is not EVENT_UNHANDLED:
                return response
        
        for item in self.handlers[event_type]:
            handler = item[1]
            func = getattr(handler, event_type)
            response = func(*args)
            
            if response is not EVENT_UNHANDLED:
                return response
        
        return EVENT_UNHANDLED

class FilterDispatcher(Dispatcher):
        
    def filter(self, filter_type, value, *args):
        print("Filtering "+args[0].name+", "+str(value))
        for item in self.handlers[filter_type]:
            handler = item[1]
            func = getattr(handler, filter_type)
            response = func(value, *args)
            
            if response is not None:
                value = response
                print(args[0].name+" = "+str(value)+" ("+handler.name+")")
        
        return value
    