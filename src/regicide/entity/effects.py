'''
Created on Apr 27, 2013

@author: Devindra

Various effects that can be added to an entity. These effects can affect any of the entity's properties or actions.
'''
import math
from random import randint
from regicide.entity import properties

class Effect(object):
    STACK_NONE = 0
    STACK_INTENSITY = 1
    STACK_DURATION = 2
    STACK_REFRESH = 3
    
    def __init__(self, name, description, duration=100, intensity=1, stack_type=STACK_NONE):
        '''
        Constructor
        '''
        self.name = name
        self.description = description
        self.duration = duration
        self.intensity = 1
        self.stack_type = stack_type
        
    def stack(self, duration, intensity):
        if self.stack_type == Effect.STACK_INTENSITY:
            self.intensity += intensity
        elif self.stack_type == Effect.STACK_DURATION:
            self.duration += duration
        elif self.stack_type == Effect.STACK_REFRESH:
            self.duration = max(self.duration, duration)
    
class Bleeding(Effect):
    DMG_PER_AUT = 0.02
    
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Bleeding",
            description = "Take damage over time.", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_INTENSITY,
        )
    
    def on_turn_start(self, game, entity, time_passed):
        current_hp = entity.get(properties.hp)
        damage = self.DMG_PER_AUT * self.intensity * time_passed
        entity.set(properties.hp, current_hp - damage)
        
class Poisoned(Effect):
    DMG_PER_AUT = 0.01
    
    def __init__(self, duration=200, intensity=1):
        Effect.__init__(self, 
            name = "Poisoned",
            description = "Take damage over time.", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_DURATION,
        )
    
    def on_turn_start(self, game, entity, time_passed):
        current_hp = entity.get(properties.hp)
        damage = self.DMG_PER_AUT * self.intensity * time_passed
        entity.set(properties.hp, current_hp - damage)
        
class Burning(Effect):
    DMG_PER_AUT = 0.02
    
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Burning",
            description = "Take damage over time.", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_REFRESH,
        )
    
    def on_turn_start(self, game, entity, time_passed):
        current_hp = entity.get(properties.hp)
        damage = self.DMG_PER_AUT * self.intensity * time_passed
        entity.set(properties.hp, current_hp - damage)
        
class Crippled(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Crippled",
            description = "Halved movement speed", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.duration,
        )
        
    def modify_property(self, value, prop, entity):
        if prop == properties.move:
            return int(value / 2)
    
class Weakened(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Weakened",
            description = "Reduced physical damage.", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_INTENSITY,
        )
        
    def modify_property(self, value, prop, entity):
        if prop == properties.damage:
            return int(value * 0.7)
    
class Suppressed(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Suppressed",
            description = "Double fatigue taken from spell casting.", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_INTENSITY,
        )
        
    def on_action(self, action):
        if ('spell' in action.type.tags):
            action.fatigue *= math.log(math.sqrt(self.intensity)) + 2
    
class Sluggish(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Suppressed",
            description = "Increases action time.", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_INTENSITY,
        )
        
    def on_action(self, action):
        action.time *= math.log(math.sqrt(self.intensity)) + 1.5
    
class Vulnerable(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Vulnerable",
            description = "Reduces armour.", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_INTENSITY,
        )
        
    def modify_property(self, value, prop, entity):
        if prop == properties.defense:
            return int(value * 0.7)
    
class Silenced(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Silenced",
            description = "Can't make sounds.", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_DURATION,
        )
    
class Immobile(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Immobile",
            description = "Can't move.", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_DURATION,
        )
    
class Blind(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Blind",
            description = "Can't see", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_DURATION,
        )
    
    def modify_property(self, value, prop, entity):
        if (prop == properties.vision):
            return 1
    
class Deaf(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Deaf",
            description = "Can't hear", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_DURATION,
        )
    
    def modify_property(self, value, prop, entity):
        if (prop == properties.hearing):
            return 0
    
class Confusion(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Hallucinating",
            description = "confused.", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_DURATION,
        )
    
    def on_turn_start(self, game, entity, time_passed):
        pass
        #entity.move(x, y)
    
class Dazed(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Dazed",
            description = "Next turn is delayed.", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_INTENSITY,
        )
    
    def on_turn_start(self, game, entity, time_passed):
        entity.remove_effect(self)
        #entity.skip()
    
class Sleep(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Sleep",
            description = "Target is a sleep.", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_DURATION,
        )
    
    def on_turn_start(self, game, entity, time_passed):
        pass
        #entity.skip()
    
class Soulless(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Soulless",
            description = "No soul", 
            duration = duration, 
            intensity = intensity,
        )
    
    def on_turn_start(self, game, entity, time_passed):
        pass
        #entity.skip()
    
class Charmed(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Charmed",
            description = "friendly", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_REFRESH,
        )
    
class Fearless(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Fearless",
            description = "no fear", 
            duration = duration, 
            intensity = intensity,
        )
    
class Focused(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Focused",
            description = "in the zone", 
            duration = duration, 
            intensity = intensity,
        )
    
class Alert(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Alert",
            description = "paying attention", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_REFRESH,
        )
        
    def modify_property(self, value, prop, entity):
        if prop == properties.dark_vision:
            return int(value * 1.5)
        if prop == properties.vision:
            return int(value * 1.5)
    
class Invisible(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Invisible",
            description = "can't be seen", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_REFRESH,
        )
    
class Feral(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Feral",
            description = "beast mode", 
            duration = duration, 
            intensity = intensity,
            stack_type = Effect.STACK_DURATION,
        )
    
class Decay(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Decay",
            description = "oh noez", 
            duration = duration, 
            intensity = intensity,
        )
    
    def on_turn_start(self, game, entity, time_passed):
        properties = [properties.agility, properties.dexterity, properties.mobility, properties.wits, properties.perception]
        prop = properties[randint(0, len(properties))]
        
        entity.set(prop, entity.get(prop) - 1)
    
class SoulRot(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Soul Rot",
            description = "no more soul", 
            duration = duration, 
            intensity = intensity,
        )
        
    def on_action(self, action):
        if ('spell' in action.type.tags):
            action.power = 0.5
    
class Frostbite(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Frostbite",
            description = "oh so cold", 
            duration = duration, 
            intensity = intensity,
        )
        
    def modify_property(self, value, prop, entity):
        if (prop.type == properties.Property.TYPE_RESISTANCE):
            return value / 2

class Ruin(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Ruin",
            description = "plague", 
            duration = duration, 
            intensity = intensity,
        )
        
    def modify_property(self, value, prop, entity):
        if (prop == properties.regen_hp):
            return 0

class Wither(Effect):
    def __init__(self, duration=100, intensity=1):
        Effect.__init__(self, 
            name = "Wither",
            description = "withered away", 
            duration = duration, 
            intensity = intensity,
        )
        
    def modify_property(self, value, prop, entity):
        if (prop == properties.regen_fp):
            return value / 2
        