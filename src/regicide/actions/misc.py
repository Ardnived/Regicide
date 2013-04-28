'''
Created on Apr 27, 2013

@author: Devindra
'''
from regicide.actions.action import Action
from regicide.entity import properties

class Attack(Action):
    def __init__(self):
        Action.__init__(self,
            name = "Attack",
            targets = [Action.TARGET_ENTITY],
            description = "",
        )
        
    def execute(self, game, source, power, target):
        Attack.execute_attack(game, source, power, target)
        
    @staticmethod
    def execute_attack(game, source, power, target):
        game.log_message(source.name+" ["+str(source.get(properties.hp))+"] attacks "+target.name+" ["+str(target.get(properties.hp))+"]")
        game.do_update('log')

class Move(Action):
    def __init__(self):
        Action.__init__(self,
            name = "Move",
            targets = [Action.TARGET_TILE],
            description = "",
        )
        
    def execute(self, game, source, power, target_x, target_y):
        target_tile = game.map.get_tile(target_x, target_y);
        if (target_tile.entity is not None):
            Attack.execute_attack(game, source, power, target_tile.entity)
        else:
            game.map.get_tile(source.x, source.y).entity = None
            target_tile.entity = source
            source.x = target_x
            source.y = target_y
            
            game.do_update('cursor')
            game.do_update('entities')
            game.do_update('tiles')
            game.do_update('shadows')
    