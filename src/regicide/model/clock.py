'''
Created on Apr 28, 2013

@author: Devindra

This class is badly designed, as it assumes that it is being extended by the game model.
Meaning it can't be reused, and is currently solely being used to organize the code.
'''
import abc
import heapq
from regicide.model import event

class TurnClock(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        self.turn_queue = []
        self.current_time = 0
        self.current_entity = None
    
    def end_turn(self, next_turn=False):
        '''
        Ends the current entity's turn, and executes the next turn.
        :param next_turn: the time until this entity can act again. Or False
        '''
        #TODO: remove this log_message, it shouldn't really be here.
        #self.log_message("Executed turn ["+str(self.current_time)+"] for "+self.current_entity.name)
        #self.do_update('log')
        
        if next_turn is not False:
            self.schedule_turn(next_turn, self.current_entity)
            self.current_entity = None
        
        self.next_turn()
        
    def schedule_turn(self, delay, entity):
        '''
        Schedules an action to occur in the turn_queue
        '''
        time_start = self.current_time + delay
        time_passed = delay
        heapq.heappush(self.turn_queue, (time_start, entity, time_passed))
        
    def next_turn(self):
        '''
        Resolve the next turn in the turn queue.
        '''
        self.accept_input = False
        self._turn()
        
    def _turn(self, dt=0):
        '''
        Resolve the next turn in the turn queue.
        '''
        self.accept_input = False
        
        turn = heapq.heappop(self.turn_queue)
        self.current_time = turn[0]
        self.current_entity = turn[1]
        time_passed = turn[2]
        
        #TODO: fix this, which hangs the game.
        #response = self.current_entity.on_turn_start(self, time_passed)
        response = self.current_entity.dispatch_event('on_turn_start', self, self.current_entity, time_passed)
        if response is not event.EVENT_CANCELED:
            self.current_entity.on_turn(self)
            self.current_entity.dispatch_event('on_turn_end', self, self.current_entity)
    
    
    