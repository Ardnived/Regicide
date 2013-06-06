'''
Created on Mar 11, 2013

@author: Devindra

A list of functions designed to be used by the Blueprints system.
The input for these functions are designed to prioritize cleanliness 
when inputing the information through the blueprint system.
'''
from random import randint
from regicide.data.blueprints import Blueprint, Mod

def pick(*options):
    '''
    Returns one of the given parameters.
    Each option has an equal chance of being chosen.
    '''
    if len(options) == 1:
        return options[0]
    elif len(options) > 0:
        return options[randint(0, len(options)-1)]

def chance(*options):
    '''
    Takes a list of options and chances.
    Starting with the option you should alternate between options and chances.
    So the first option will correspond to the first chance, and so on.
    The function will then randomly choose one of the options.
    Options with a higher corresponding chance,
    have a proportionately better chance of being chosen.
    '''
    if len(options) == 1:
        return options[0]
    
    # Split the input into a list of values and a list of options.
    values = options[0::2]
    chances = options[1::2]
    # Make the choice
    choice = randint(0, sum(chances))
    
    # Determine which option the choice corresponds to.
    i = 0
    while choice > chances[i]:
        i += 1
        choice -= chances[i]
    
    return values[i]

def domain(**domains):
    '''
    Returns a list of all Blueprints with the given domains.
    '''
    return Blueprint.find_blueprints(**domains)

def mod(category):
    '''
    Returns a list of all Mods with the given category.
    '''
    return Mod.find_mods(category)

def add(*values):
    '''
    Returns the sum of all parameters.
    '''
    output = values[0]
    for value in values[1:]:
        output += value
    
    return output

def subtract(*values):
    '''
    Subtracts each subsequent parameter from the first one.
    '''
    output = values[0]
    for value in values[1:]:
        output -= value
    
    return output

def multiply(*values):
    '''
    Returns the product of all parameters.
    '''
    output = values[0]
    for value in values[1:]:
        output *= value
    
    return output

def divide(*values):
    '''
    Returns the first parameter divided by each subsequent parameter in turn.
    '''
    output = values[0]
    for value in values[1:]:
        output /= value
    
    return output

def source(master, property_key):
    '''
    Returns a property from the given master object.
    This method is used by Mods and Factories to refer to the object they are modifying.
    
    Should only be used by Mods and Factories
    '''
    return master.properties[property_key]
