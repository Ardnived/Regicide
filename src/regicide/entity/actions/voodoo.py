'''
Created on Apr 27, 2013

@author: Devindra
'''
import abc
from regicide.level import tile
from regicide.entity import properties
from regicide.entity.entity import Entity
from regicide.entity.actions.action import Action
from regicide.level.tile import Tile

class Possess(Action):
    def __init__(self):
        Action.__init__(self,
            name = "Possess",
            targets = [Tile.TARGET_ENTITY],
            description = "Take control of an enemy.",
            tags = ['spell', 'voodoo'],
            target_range = 3,
        )
        
    def execute(self, game, source, power, target):
        target = target.entity
        
        resistance = target.get(properties.spirit)
        strength = source.get(properties.voodoo)
        game.log_message(source.name+" casts "+self.name+".") 
               
        if (strength > resistance):
            #spirit = source.primary_spirit
            #source.remove_spirit(spirit)
            #target.add_spirit(spirit)
            game.log_message("Your perspective shifts.")
        else:
            game.log_message(target.name+" resists.")

class Exorcism(Action):
    def __init__(self):
        Action.__init__(self,
            name = "Exorcism",
            targets = [Tile.TARGET_ENTITY],
            description = "Attempts to remove a chosen spirit from the target.",
            tags = ['spell', 'voodoo']
        )
        
    def execute(self, game, source, power, target):
        target = target.entity
        
        resistance = target.get(properties.spirit)
        strength = source.get(properties.voodoo)
        game.log_message(source.name+" casts "+self.name+".") 
               
        if (strength > resistance):
            pass
            #spirit = source.primary_spirit
            #source.remove_spirit(spirit)
        else:
            game.log_message(target.name+" resists.")

class Purge(Action):
    def __init__(self):
        Action.__init__(self,
            name = "Purge",
            targets = [Tile.TARGET_ENTITY],
            description = "Attempts to remove a chosen spirit from the target.",
            tags = ['spell', 'voodoo']
        )
        
    def execute(self, game, source, power, target):
        target = target.entity
        
        resistance = target.get(properties.spirit)
        strength = source.get(properties.voodoo)
        game.log_message(source.name+" casts "+self.name+".") 
               
        if strength > resistance:
            source.remove_spirit(source.primary_spirit)
        else:
            game.log_message(target.name+" resists.")
            
class SummonSpirit(Action):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, name, description, blueprint):
        Action.__init__(self, name, description, 
            targets = [Tile.TARGET_ENTITY, Tile.TARGET_ITEM], 
            tags = ['spell', 'voodoo', 'spirit']
        )
        self.blueprint = blueprint
        
    def execute(self, game, source, power, target):
        target = target.entity
        
        if ( isinstance(target, Entity) ):
            resistance = target.get(properties.spirit)
        else:
            resistance = 0
            
        strength = source.get(properties.voodoo)
        game.log_message(source.name+" casts "+self.name+".") 
               
        if (strength > resistance):
            spirit = self.blueprint.master()
            target.add_spirit(spirit)
            
            if (source == target):
                game.log_message("You hear a new voice in the back of your head. (not really)")
        else:
            game.log_message(target.name+" resists.")
        
class BullStrength(SummonSpirit):
    def __init__(self):
        SummonSpirit.__init__(self,
            name = "Bull's Strength",
            description = "Summon a random spirit of strength into the target.",
            blueprint = None
        )
        
class AvianWisdom(SummonSpirit):
    name = "Avian's Wisdom",
    description = "Summon a random spirit of soul into the target."
    
    def __init__(self):
        SummonSpirit.__init__(self,
            name = "Avian's Wisdom",
            description = "Summon a random spirit of soul into the target.",
            blueprint = None
        )
        
class CatEye(SummonSpirit):
    def __init__(self):
        SummonSpirit.__init__(self,
            name = "Cat's Eye",
            description = "Summon a random spirit of awareness into the target.",
            blueprint = None
        )
        
class RavenWrath(SummonSpirit):
    def __init__(self):
        SummonSpirit.__init__(self,
            name = "Raven's Wrath",
            description = "Summon a random spirit of war into the target.",
            blueprint = None
        )
        
class CowApathy(SummonSpirit):
    def __init__(self):
        SummonSpirit.__init__(self,
            name = "Cow's Apathy",
            description = "Summon a random spirit of sloth into the target.",
            blueprint = None
        )
        
class DemonRage(SummonSpirit):
    def __init__(self):
        SummonSpirit.__init__(self,
            name = "Demon's Rage",
            description = "Summon a random spirit of anger into the target.",
            blueprint = None
        )
        
class DogSimplicity(SummonSpirit):
    def __init__(self):
        SummonSpirit.__init__(self,
            name = "Dog's Simplicity",
            description = "Summon a random spirit of simplicity into the target.",
            blueprint = None
        )
        