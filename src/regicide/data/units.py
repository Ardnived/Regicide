'''
Created on Mar 11, 2013

@author: Devindra

Data definitions for all npcs in the game.
'''
from regicide.data.blueprints import Blueprint
from regicide.data.functions import pick, chance, domain, add
from regicide.resources import visual

print("Loading Units...")

UNIT = Blueprint(
    hidden = True,
    domains = {
        'category': 'unit',
    },
    properties = {
        'hp'   : 5,
        'mana' : 0,
        'dexterity'  : 3,
        'agility'    : 3,
        'mobility'   : 3,
        'wits'       : 3,
        'perception' : 3,
    },
)

NPC = Blueprint(
    hidden = True,
    parents = UNIT,
    domains = {
        'type': 'npc',
    },
)

SAVAGE = Blueprint(
    hidden = True,
    parents = NPC,
    domains = {
        'race': 'savage',
    },
    properties = {
        'traits': ['brutal'],
    }
)

GOBLIN = Blueprint(
    parents = SAVAGE,
    domains = {
        'race': 'goblin',
        'floor': 'commons',
        'zone': 'castle',
    },
    properties = {
        'name'    : [add, [[pick, ["Blue", "Red", "Green"]], " Goblin"]],
        'hp'      : [pick, range(5, 11)],
        'threat'  : [chance, ['low', 3, 'medium', 4, 'high', 1]],
        'sprite'  : visual.Entity.GOBLIN,
        'loot'    : [pick, [domain, {'category':'item', 'type':'weapon'}]],
        '+traits' : 'dumb',
        'sprite'  : visual.Entity.GOBLIN,
        'ascii'   : visual.ASCII.get_index(0, 6),
    },
)

GOBLIN_RUNT = Blueprint(
    parents = GOBLIN,
    properties = {
        'name'    : 'Goblin Runt',
        '-hp'     : [pick, range(2, 5)],
        'threat'  : 'low',
        'sprite'  : visual.Entity.GOBLIN,
        'loot'    : [[pick, [domain, {'category':'item', 'type':'weapon'}]], [pick, [domain, {'category':'item', 'type':'weapon'}]]],
        '+traits' : ['small', 'rash'],
        '-traits' : 'brutal',
    },
)

