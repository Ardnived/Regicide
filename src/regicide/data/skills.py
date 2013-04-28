'''
Created on Mar 28, 2013

@author: Devindra

Data definitions for all skills in the game.
'''
from regicide.data.blueprints import Blueprint
from regicide.entity import properties

print("Loading Skills...")

SKILL = Blueprint(
    hidden = True,
    domains = {
        'category': 'skill',
    },
)

STANCE = Blueprint(
    hidden = True,
    parents = SKILL,
    domains = {
        'type': 'stance',
    },
)

def do_test_action(skill, user, target):
    print("Executing "+skill.properties['name']+" on "+target.name+" from "+user.name)

def do_stance_defensive(skill, user, target):
    pass

DEFENSIVE_STANCE = Blueprint(
    parents = STANCE,
    properties = {
        'name': "Defensive Stance",
        'modifiers': {
            properties.max_hp: ['+', 4],
            properties.blades: ['+', 5],
        },
        'action': do_test_action,
    }
)

SPELL = Blueprint(
    hidden = True,
    parents = SKILL,
    domains = {
        'type': 'spell',
    },
)

HEX = Blueprint(
    parents = SPELL,
    domains = {
        'magic': 'voodoo',
    },
    properties = {
        'name': "Hex",
        'modifiers': {
            properties.max_hp: ['+', 4],
            properties.blades: ['+', 5],
        },
        'action': do_test_action,
    }
)
