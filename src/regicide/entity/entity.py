'''
Created on Mar 2, 2013

@author: Devindra

An entity in the game. Currently this indicates any Player or NPC.
Entities get turns to act.
'''
import abc
from random import randint
from pyglet import sprite
from regicide.model import event
from regicide.resources import visual
from regicide.entity import properties

class Entity(event.FilterDispatcher, event.EventDispatcher):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, template, x, y):
        '''
        :param template: the blueprints.Master object that defines the parameters for this entity.
        :param x: the initial x position of this entity on the grid.
        :param y: the initial y position of this entity on the grid.
        '''
        self.x = x
        self.y = y
        self.name = template.properties['name']
        self.sprite = sprite.Sprite(visual.Entity.get(template.properties['sprite']))
        self.ascii = sprite.Sprite(visual.ASCII.get(template.properties['ascii']))
        self.dead = False
        
        self._equipment = {}
        self._inventory = []
        self._traits = []
        self._actions = []
        self._spirits = []
        self._effects = []
        self._modifiers = {}
        
        self._properties_value = {}
        self._properties_cache = {}
        
        self.set(properties.max_hp, template.properties['hp'])
        self.set(properties.max_mana, template.properties['mana'])
        
        self.set(properties.dexterity, template.properties['dexterity'])
        self.set(properties.agility, template.properties['agility'])
        self.set(properties.mobility, template.properties['mobility'])
        self.set(properties.wits, template.properties['wits'])
        self.set(properties.perception, template.properties['perception'])
        
        self.recalculate_properties()
        
    def on_turn_start(self, game, entity, time_passed):
        if self.dead:
            self.on_death(game)
            return event.EVENT_CANCELED
        
        if self.effects:
            for effect in self.effects:
                effect.duration -= time_passed
                if effect.duration <= 0:
                    self.effects.remove(effect)
            
            game.do_update('playercard')   
    
    def on_death(self, game):
        game.move_entity(self, target=None)
        game.log_message(self.name+" dies.")
        game.do_update('log')
        game.end_turn() 
    
    # ==================================
    
    def get(self, prop, unmodified=False):
        '''
        Gets the stored value of one of this entity's properties. 
        Use recalculate_properties(properties) to refresh the data.
        '''
        if unmodified:
            collection = self._properties_value
        else:
            collection = self._properties_cache
        
        if collection.has_key(prop):
            return collection[prop]
        elif not unmodified:
            if type(prop.base) == properties.Property:
                return self.get(prop.base)
            else:
                return prop.base
        else:
            return 0
    
    def set(self, prop, value):
        '''
        Sets the base value for one of this entity's properties. 
        '''
        self._properties_value[prop] = value
        self.recalculate_properties()
        
        if value <= 0 and prop.type == properties.Property.TYPE_ATTR:
            self.dead = True
        elif prop == properties.hp and value <= -self.get(properties.max_hp):
            self.dead = True
    
    @property
    def properties(self):
        return self._properties
        
    # ==================================

    def add_spirit(self, spirit):
        '''
        Adds the given Master object to this entity's trait list,
        and adds the Action's modifiers to the entity as well.
        '''
        self._spirits.append(spirit)
        self.add_modifier(spirit)
        self.add_handler(spirit)
        
        if (self.primary_spirit is None):
            self.primary_spirit = spirit

    def remove_spirit(self, spirit):
        '''
        Removes an action from this entity.
        '''
        self._spirits.remove(spirit)
        self.remove_modifier(spirit)
        self.remove_handler(spirit)
        
        if self.primary_spirit == spirit:
            self.primary_spirit = self._spirits[randint(0, len(self._spirits))]
        
    @property
    def spirits(self):
        return self._spirits
        
    # ==================================

    def add_action(self, action):
        '''
        Adds the given Master object to this entity's trait list,
        and adds the Action's modifiers to the entity as well.
        '''
        self._actions.append(action)
        self.add_handler(action)

    def remove_action(self, action):
        '''
        Removes an action from this entity.
        '''
        self._actions.remove(action)
        self.remove_handler(action)
        
    @property
    def actions(self):
        return self._actions
        
    # ==================================

    def add_trait(self, trait):
        '''
        Adds the given Master object to this entity's trait list,
        and adds the Trait's modifiers to the entity as well.
        A trait should be mastered from one of the Blueprints
        defined in regicide.data.traits
        '''
        self._traits.append(trait)
        self.add_handler(trait)

    def remove_trait(self, trait):
        '''
        Removes a trait from this entity.
        A trait should be mastered from one of the Blueprints
        defined in regicide.data.traits
        '''
        self._traits.remove(trait)
        self.remove_handler(trait)
        
    @property
    def traits(self):
        return self._traits
        
    # ==================================

    def add_effect(self, effect):
        '''
        Adds an effect to this entity.
        '''
        self._effects.append(effect)
        self.add_handler(effect)

    def remove_effect(self, effect):
        '''
        Removes an effect from this entity.
        '''
        self._effects.remove(effect)
        self.remove_handler(effect)
        
    @property
    def effects(self):
        return self._effects
        
    # ==================================
        
    def add_item(self, item):
        '''
        Adds an item to this entity's inventory.
        An item should be mastered from one of the Blueprints
        defined in regicide.data.items
        '''
        self._inventory.append(item)
    
    def remove_item(self, item):
        '''
        Removes an item from this entity's inventory.
        An item should be mastered from one of the Blueprints
        defined in regicide.data.items
        '''
        self._inventory.remove(item)
        
    @property
    def inventory(self):
        return self._inventory
        
    # ==================================
    
    def equip_item(self, item):
        '''
        Attempts to equip an item to the item's equip slot on this entity.
        Also adds any modifiers that this item has.
        Returns success or failure.
        '''
        if item not in self._inventory:
            self.add_item(item)
        
        if self._equipment.has_key(item.equip_slot) is False:
            self._equipment[item.equip_slot] = []
        
        if self.could_equip(item):
            self._equipment[item.equip_slot].append(item)
            self.add_handler(item)
            return True
        else:
            return False
    
    def unequip_item(self, item):
        '''
        Attempts to unequip an item from this entity.
        Also removes any modifiers that this item has.
        Returns success or failure.
        '''
        if self._equipment.has_key(item.equip_slot) and item in self._equipment[item.equip_slot]:
            self._equipment[item.equip_slot].remove(item)
            self.remove_handler(item)
            return True
        else:
            return False
    
    def could_equip(self, item):
        '''
        Checks to see if a given item could be equipped on this entity.
        '''
        equip_slot = item.equip_slot
        free_space = equip_slot.size
        
        if self._equipment.has_key(equip_slot):
            for equip in self._equipment[equip_slot]:
                free_space -= equip.equip_size
        
        return item.equip_size <= free_space
    
    def get_equips(self, equip_slot):
        '''
        Gets a list of all items in a particular equip slot for this entity.
        '''
        return self._equipment[equip_slot]
        
    @property
    def equipment(self):
        return self._equipment
        
    # ==================================
    
    def add_handler(self, handler, priority=0):
        event.FilterDispatcher.add_handler(self, handler, priority)
        self.recalculate_properties()
    
    def remove_handler(self, handler):
        event.FilterDispatcher.remove_handler(self, handler)
        self.recalculate_properties()
    
    def recalculate_properties(self):
        '''
        Recalculates all properties.
        This is typically called after property modifiers are added/removed
        '''
        self._properties_cache.clear()
        
        for prop in properties.Property.all:
            if self._properties_cache.has_key(prop):
                # We've already recalculated this property
                continue
            else:
                if type(prop.base) == properties.Property and not self._properties_cache.has_key(prop.base):
                    self.recalculate_property(prop.base)
                
                self.recalculate_property(prop)
    
    def recalculate_property(self, prop):
        '''
        Recalculates the given property.
        '''
        value = self.get(prop, unmodified=True)
        
        if type(prop.base) == properties.Property:
            value += self.get(prop.base)
        else:
            value += prop.base
        
        self._properties_cache[prop] = self.filter_property(prop, value)
    
    def filter_property(self, prop, value):
        return self.filter('modify_property', value, prop, self)
        
    def get_property_modifiers(self, prop):
        if type(prop.base) == properties.Property:
            value = self._properties_value[prop.base]
        else:
            value = prop.base
        
        if self._properties_value.has_key(prop):
            value = self._properties_value[prop]
        
        modifications = []
        for item in self.handlers['modify_property']:
            handler = item[1]
            func = getattr(handler, 'modify_property')
            response = func(value, prop, self)
            
            if response is not None:
                modifications.append((response - value, handler.name))
                value = response
        
        return modifications
        
    @property
    def modifiers(self):
        return self._modifiers
        
    # ==================================
    
    def is_player(self):
        return False
    
Entity.register_dispatch_type('modify_property');
Entity.register_dispatch_type('on_turn_start');
Entity.register_dispatch_type('on_turn_end');
Entity.register_dispatch_type('on_action');

