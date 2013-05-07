'''
Created on Apr 27, 2013

@author: Devindra
'''
from random import randint
from regicide.level import tile
from regicide.entity import properties
from regicide.entity.actions.action import Action

class Attack(Action):
    def __init__(self):
        Action.__init__(self,
            name = "Attack",
            targets = [tile.TARGET_ENTITY],
            description = "",
        )
        
    def execute(self, game, source, power, target):
        Attack.execute_attack(game, source, power, target)
        
    @staticmethod
    def execute_attack(game, source, power, target):
        damage = source.get(properties.damage)
        damage_dice = source.get(properties.damage_dice)
        damage_sides = source.get(properties.damage_sides)
        
        for _ in xrange(damage_dice):
            damage += randint(1, damage_sides)
        
        game.log_message(source.name+" attacks "+target.name+" ["+str(target.get(properties.hp))+"] for "+str(damage)+" damage.")
        game.do_update('log')
        
        target.set(properties.hp, target.get(properties.hp) - damage) 

class Move(Action):
    def __init__(self):
        Action.__init__(self,
            name = "Move",
            targets = [tile.TARGET_PASSABLE],
            description = "",
        )
        
    def execute(self, game, source, power, target):
        target_tile = game.map.get_tile(*target);
        if target_tile.entity is not None:
            Attack.execute_attack(game, source, power, target_tile.entity)
        else:
            game.map.get_tile(source.x, source.y).entity = None
            target_tile.entity = source
            source.x = target[0]
            source.y = target[1]
            
            game.do_update('cursor')
            game.do_update('entities')
            game.do_update('tiles')
            game.do_update('shadows')
    