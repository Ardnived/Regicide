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
            
            if source == game.player:
                self.update_exploration(game)
                
                game.do_update('cursor')
                game.do_update('bounds')
    
    def update_exploration(self, game):
        strength = game.player.get(properties.perception)
        
        for x in xrange(-strength, strength+1):
            range_y = strength - abs(x)
            for y in xrange(-range_y, range_y+1):
                target_x = game.player.x + x
                target_y = game.player.y + y
                tile = game.map.get_tile(target_x, target_y)
                
                if tile is not None and game.map.has_line_of_sight(game.player.x, game.player.y, target_x, target_y):
                    tile.explored = True
        
    