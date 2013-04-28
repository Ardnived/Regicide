'''
Created on Mar 24, 2013

@author: Devindra

Data definitions for all traits in the game.
'''
from regicide.data.blueprints import Blueprint
from regicide.entity import properties

print("Loading Traits...")

TRAIT = Blueprint(
    hidden = True,
    domains = {
        'category': 'trait',
    },
)

SPIRIT = Blueprint(
    hidden = True,
    parents = TRAIT,
    domains = {
        'type': 'spirit',
    },
)

BLADE_APTITUDE = Blueprint(
    parents = TRAIT,
    domains = {
        'type': 'skill',
        'gear': 'blade',
    },
    properties = {
        'name': "Blade Aptitude",
        'description': "weapon skill",
        'modifiers': {
            properties.max_hp: ['+', 4],
            properties.blades: ['+', 5],
        },
    }
)

DEMON_PACT = Blueprint(
    parents = TRAIT,
    domains = {
        'type': 'skill',
    },
    properties = {
        'name': "Pact With Xashak",
        'description': "pact",
        'modifiers': {
            properties.corruption : ['+', 4],
            properties.witchcraft : ['+', 2],
        },
    }
)

