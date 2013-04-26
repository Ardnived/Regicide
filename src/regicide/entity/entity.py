'''
Created on Mar 2, 2013

@author: Devindra

An entity in the game. Currently this indicates any Player or NPC.
Entities get turns to act.
'''
import abc
import types
from pyglet import sprite
from regicide.resources import visual
from regicide.entity import properties

class Entity(object):
    '''
    classdocs
    '''
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
        
        self._equipment = {}
        self._inventory = []
        self._traits = []
        self._modifiers = {}
        
        self._base_properties = {}
        self._properties = {}
        
        self.set(properties.max_hp, template.properties['hp'])
        self.set(properties.hp, template.properties['hp'])
        self.set(properties.max_mana, template.properties['mana'])
        self.set(properties.mana, template.properties['mana'])
        
        self.set(properties.dexterity, template.properties['dexterity'])
        self.set(properties.agility, template.properties['agility'])
        self.set(properties.mobility, template.properties['mobility'])
        self.set(properties.wits, template.properties['wits'])
        self.set(properties.perception, template.properties['perception'])
        
        self.recalculate_properties()
        
    def get(self, prop, base=False):
        '''
        Gets the stored value of one of this entity's properties. 
        Use recalculate_properties(properties) to refresh the data.
        '''
        if (base):
            if (self._base_properties.has_key(prop)):
                return self._base_properties[prop]
            else:
                if (type(prop.base) == properties.Property):
                    return self.get(prop.base)
                else:
                    return prop.base
        else:
            if (self._properties.has_key(prop)):
                return self._properties[prop]
            else:
                return self.get(prop, True)
    
    def set(self, prop, value):
        '''
        Sets the base value for one of this entity's properties. 
        '''
        self._base_properties[prop] = value
        
    @property
    def properties(self):
        return self._properties

    def add_trait(self, trait):
        '''
        Adds the given Master object to this entity's trait list,
        and adds the Trait's modifiers to the entity as well.
        A trait should be mastered from one of the Blueprints
        defined in regicide.data.traits
        '''
        self._traits.append(trait)
        self.add_modifier(trait)

    def remove_trait(self, trait):
        '''
        Removes a trait from this entity.
        A trait should be mastered from one of the Blueprints
        defined in regicide.data.traits
        '''
        self._traits.remove(trait)
        self.remove_modifier(trait)
        
    @property
    def traits(self):
        return self._traits
        
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
    
    def equip_item(self, item):
        '''
        Attempts to equip an item to the item's equip slot on this entity.
        Also adds any modifiers that this item has.
        Returns success or failure.
        '''
        if (item not in self._inventory):
            self.add_item(item)
        
        equip_slot = item.properties['equip_slot']
        equip_size = item.properties['equip_size']
        free_space = equip_slot.size
        
        if (self._equipment.has_key(equip_slot) is False):
            self._equipment[equip_slot] = []
        else:
            for item in self._equipment[equip_slot]:
                free_space -= item['equip_size']
        
        if (equip_size <= free_space):
            self._equipment[equip_slot].append(item)
            self.add_modifier(item)
            return True
        else:
            return False
    
    def unequip_item(self, item):
        '''
        Attempts to unequip an item from this entity.
        Also removes any modifiers that this item has.
        Returns success or failure.
        '''
        equip_slot = item.properties['equip_slot']
        if (self._equipment.has_key(equip_slot) and item in self._equipment[equip_slot]):
            self._equipment[equip_slot].remove(item)
            self.remove_modifier(item)
            return True
        else:
            return False
    
    def get_equips(self, equip_slot):
        '''
        Gets a list of all items in a particular equip slot for this entity.
        '''
        return self._equipment[equip_slot]
        
    @property
    def equipment(self):
        return self._equipment
        
    def add_modifier(self, modifier_set):
        '''
        Adds a set of property modifiers to this entity.
        The relevant properties are then recalculated.
        '''
        properties = modifier_set.properties['modifiers']
        for key, modifier in properties.iteritems():
            if (self._modifiers.has_key(key) is False):
                self._modifiers[key] = {}
            
            self._modifiers[key][modifier_set] = modifier
        
        self.recalculate_properties(properties.keys())
        
    def remove_modifier(self, modifier_set):
        '''
        Removes a set of property modifiers from this entity.
        The relevant properties are then recalculated.
        '''
        properties = modifier_set.properties['modifiers']
        for key in properties.iterkeys():
            self._modifiers[key].pop(modifier_set)
        
        self.recalculate_properties(properties.keys())
        
    def recalculate_properties(self, update_list = None):
        '''
        Recalculates each property in a given list.
        This is typically called after property modifiers are added/removed
        '''
        if (update_list is None):
            update_list = self._base_properties.keys()
        
        for prop in update_list:
            if (type(prop.base) == properties.Property):
                value = self._base_properties[prop.base]
            else:
                value = prop.base
            
            if (self._base_properties.has_key(prop)):
                value = self._base_properties[prop]
            
            if (self._modifiers.has_key(prop)):
                for modifier in self._modifiers[prop].itervalues():
                    value = self.apply_modifier(value, modifier)
            
            self._properties[prop] = value
    
    def apply_modifier(self, value, modifier):
        '''
        Returns the given value modified by the given modifier.
        '''
        if (type(modifier) == types.FunctionType):
            # If the modifier is a function pass the value to it and return the result.
            return modifier(self, value)
        else:
            operation = modifier[0]
            adjustment = modifier[1]
            
            if (operation == '+'):
                return value + adjustment
            elif (operation == '-'):
                return value - adjustment
            elif (operation == '*'):
                return value * adjustment
            elif (operation == '/'):
                return value / adjustment
        
    @property
    def modifiers(self):
        return self._modifiers

