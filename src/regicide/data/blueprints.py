'''
Created on Mar 10, 2013

@author: Devindra

An implementation of the blueprints system from Three Hundred Mechanics
http://www.squidi.net/three/entry.php?id=165

This system is used to define the various data components of this game.
Including Characters, Enemies, Rooms, Skills, Traits, Items, etc.
'''
from itertools import chain

def merge_dicts(*dicts): 
    '''
    A helper function for the blueprints system.
    This method will take an arbitrary number of dictionaries
    and merge them from left to right.
    
    Dictionaries to the right will be given priority for their keys.
    '''
    return dict(chain(*[d.iteritems() for d in dicts]))

class Blueprint(object):
    '''
    An instance of blueprint defines instructions for generating a master.
    Typically this means it defines a parent Blueprint to inherit from,
    and contains some randomisation of various attributes.
    
    Each blueprint defines a set of domains (aka categories), which can be used
    to get a subset of all blueprints.
    '''
    # A dictionary of all blueprints mapped by the domains that they are identified by.
    _blueprints_by_domain = {}
    
    @staticmethod
    def find_blueprints(**domains):
        '''
        Looks for a blueprint which has the given domains.
        '''
        primary_key = domains.keys()[0]
        primary_value = domains.values()[0]
        
        if type(primary_value) == list:
            primary_value = primary_value[0]
        
        output = []
        for blueprint in Blueprint._blueprints_by_domain[primary_key][primary_value]:
            if blueprint.has_domains(**domains):
                output.append(blueprint)
        
        return output
    
    def __init__(self, hidden=False, parents=None, domains={}, properties={}):
        '''
        :param hidden: prevents this blueprint from being added to the list of blueprints.
        Usually used for a blueprint which is used only as a parent, and should not be mastered.
        :param parents: the blueprints to inherit properties from when this blueprint is mastered.
        :param properties: the properties to be resolved when this blueprint is mastered.
        '''
        if isinstance(parents, Blueprint):
            # The Blueprint contructor requires that parents be in a list,
            # but we are simplifying the input syntax by also accepting a single Blueprint.
            parents = [parents]
        
        self.parents = parents
        self.domains = domains
        self.properties = properties
        
        if parents is not None:
            for parent in parents:
                # Loop through the domains of each parent
                # and add them to this blueprint.
                for key, args in parent.domains.iteritems():
                    if self.domains.has_key(key) is False:
                        self.domains[key] = []
                    elif type(self.domains[key]) != list:
                        self.domains[key] = [self.domains[key]]
                    
                    if type(args) != list:
                        args = [args]
                    
                    self.domains[key].extend(args)
        
        if hidden is False:
            # If the blueprint isn't hidden, then loop through it's domains,
            # and add it to the class variable that holds a list of blueprints by domain.
            for domain, values in domains.iteritems():
                if Blueprint._blueprints_by_domain.has_key(domain) is False:
                    Blueprint._blueprints_by_domain[domain] = {}
                
                if type(values) != list:
                    values = [values]
                
                for value in values:
                    if Blueprint._blueprints_by_domain[domain].has_key(value) is False:
                        Blueprint._blueprints_by_domain[domain][value] = []
                    
                    Blueprint._blueprints_by_domain[domain][value].append(self)
                    
    def has_domains(self, **domains):
        '''
        Return whether this blueprint has the specified domain values.
        '''
        for key, items in domains.iteritems():
            if self.domains.has_key(key):
                if (type(items) != list):
                    items = [items]
                
                for item in items:
                    if self.domains[key].count(item) <= 0:
                        # Blueprint doesn't have domain value.
                        return False
            else:
                # Blueprint doesn't have domain key, return false.
                return False
        
        return True
                
    def master(self):
        '''
        Create a new Master object based on this blueprint.
        '''
        return Master(self.parents, self.properties, self)
    
class Factory(object):
    '''
    This class is used to add onto a blueprint with an arbitrary selection of Mods.
    The advantage of this over a blueprint with a paren is that the selection of mods applied
    can be randomized, and that mods and factories can use the regicide.data.functions.source function
    '''
    
    def __init__(self, blueprint, mods=[], properties={}):
        '''
        :param blueprint: the blueprint to serve as the base for this factory.
        :param mods: the mods to apply to the blueprint when the factory is mastered.
        :param properties: any additional properties to add or change after the mods have been applied.
        '''
        self.blueprint = self.evaluate(blueprint)
        
        mods = self.evaluate(mods)
        
        if type(mods) != list:
            mods = [mods]
        
        self.mods = mods
        self.properties = properties
    
    def master(self):
        master = Master(self.blueprint.parents, self.blueprint.properties, self.blueprint)
        
        for mod in self.mods:
            mod.apply_to(master)
            
        for key, value in self.properties.iteritems():
            master.properties[key] = master.evaluate(value)
        
        return master
    
    def evaluate(self, arg):
        '''
        Evaluates a property to resolve randomization and other functions before mastering.
        '''
        # If the argument is a list:
        if type(arg) == list:
            # If the first argument is callable:
            if hasattr(arg[0], '__call__'):
                # Call it with the second argument as a parameter.
                func = arg[0]
                params = self.evaluate(arg[1])
                value = evaluate_function(func, params)
                # Evaluate the results of the call before returning it.
                return self.evaluate(value)
            else:
                # otherwise, evaluate every argument in the list.
                return map(self.evaluate, arg)
        else:
            # The argument is a basic value, return it.
            return arg
        
    
class Mod(object):
    '''
    Defines objects which can be utilised by the Factory class to modify blueprints.
    '''
    _mods_by_category = {}
    
    @staticmethod
    def find_mods(category):
        '''
        Search the list of mods for ones that match the given type (domain).
        '''
        return Mod._mods_by_category[category]
    
    def __init__(self, category=None, properties={}):
        '''
        :param category: a type to categorize this mod. Each mod may only have one category, unlike the Blueprint domains.
        :param properties: the properties to modify when this mod is applied.
        Only properties that exist in the source blueprint will be applied.
        '''
        self.properties = properties
        
        if Mod._mods_by_category.has_key(category) is False:
            # Create the list for this type if it doesn't already exist.
            Mod._mods_by_category[category] = []
        
        if type is not None:
            # Add this mod to the list of such mods.
            Mod._mods_by_category[category].append(self)
    
    def apply_to(self, master):
        '''
        Applies this mod to a Master object.
        '''
        for key, value in self.properties.iteritems():
            if master.properties.has_key(key):
                # Only modify the object if it has the corresponding property to modify.
                master.properties[key] = master.evaluate(value)
     
class Master(object):
    '''
    A finalized version of a Blueprint.
    '''
    
    def __init__(self, parents=None, properties={}, blueprint=None):
        '''
        :param parents: the parent blueprints that should also be mastered and merged into this master.
        '''
        self.blueprint = blueprint
        self.properties = {}
        
        if parents is not None:
            for parent in parents:
                parent = parent.master()
                
                # Merge the properties of the parent into this master.
                self.properties = merge_dicts(self.properties, parent.properties)
        
        # If properties is not empty:
        if properties:
            # Loop through each property and evaluate it.
            for key, args in properties.iteritems():
                value = self.evaluate(args)
                
                # If the property key starts with '+' then add the value to the parent's property.
                if key[0] == '+':
                    key = key[1:]
                    if type(self.properties[key]) == list:
                        if type(value) == list:
                            self.properties[key].extend(value)
                        else:
                            self.properties[key].append(value)
                    else:
                        self.properties[key] += value
                # If the property key starts with '-' then subtract from the parent's property.
                elif key[0] == '-':
                    key = key[1:]
                    if type(self.properties[key]) == list:
                        if type(value) == list:
                            for val in value:
                                self.properties[key].remove(val)
                        else:
                            self.properties[key].remove(value)
                    else:
                        self.properties[key] -= value
                else:
                    # Otherwise, just overwrite the parent's value.
                    self.properties[key] = value

    def evaluate(self, arg):
        '''
        Evaluates a blueprint property. 
        Resolving any functions which have been stored as arrays
        and mastering Blueprints and Factories
        '''
        if (isinstance(arg, Blueprint)):
            return arg.master()
        if (isinstance(arg, Factory)):
            return arg.master()
        elif (type(arg) == list and len(arg) > 0):
            # If the argument is a non-empty list, check if it's callable.
            if (hasattr(arg[0], '__call__')):
                # Evaluate it as a function.
                func = arg[0]
                
                if (func.__name__ is 'source'):
                    # If the given function is the special function, source, then self is passed to it.
                    return func(self, arg[1])
                else:
                    # otherwise, evaluate the function with the send argument as it's params.
                    params = self.evaluate(arg[1])
                    value = evaluate_function(func, params)
                    
                    return self.evaluate(value)
            else:
                # otherwise, evaluate every argument in the list.
                return map(self.evaluate, arg)
        else:
            # The argument is a basic value, return it.
            return arg


def evaluate_function(func, params):
    '''
    Evaluates a function that has been stored as a list.
    The primary purpose of this function is to determine the nature of the params,
    and then call func using them, depending on whether the params are a list, dict, or other.
    '''
    if type(params) == list:
        value = func(*params)
    elif type(params) == dict:
        value = func(**params)
    else:
        value = func(params)

    return value

from regicide.data import items, rooms, units #@UnusedImport #load data
