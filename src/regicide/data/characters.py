'''
Created on Mar 23, 2013

@author: Devindra

Contains a list of blueprint for playable characters.
All the data that differentiates one character from another is included below.
'''
from regicide.data.blueprints import Blueprint
from regicide.data.units import UNIT
from regicide.resources import visual

print("Loading Characters...")

CHARACTER = Blueprint(
    hidden = True,
    parents = UNIT,
    domains = {
        'type': 'player',
    },
    properties = {
        'sprite' : visual.Entity.RANGER,
        'ascii'  : visual.ASCII.get_index(15, 13),
        'hp'     : 10,
        'mana'   : 2,
        'dexterity'  : 5,
        'agility'    : 5,
        'mobility'   : 5,
        'wits'       : 5,
        'perception' : 5,
    },
)

ELLIOT = Blueprint(
    parents = CHARACTER,
    properties = {
        'name'     : "Elliot",
        'portrait' : visual.Character.ELLIOT,
        '+hp'      : 2,
        '+mana'    : -1,
        '+dexterity'  : 0,
        '+agility'    : 0,
        '+mobility'   : 0,
        '+wits'       : 0,
        '+perception' : 0,
    }
)

HELENA = Blueprint(
    parents = CHARACTER,
    properties = {
        'name'     : "Helen",
        'portrait' : visual.Character.HELENA,
        '+hp'      : 1,
        '+mana'    : -1,
        '+dexterity'  : 0,
        '+agility'    : 0,
        '+mobility'   : 0,
        '+wits'       : 0,
        '+perception' : 0,
    }
)

LANCEL = Blueprint(
    parents = CHARACTER,
    properties = {
        'name'     : "Aristo",
        'portrait' : visual.Character.LANCEL,
        '+hp'      : 4,
        '+mana'    : -2,
        '+dexterity'  : 0,
        '+agility'    : 0,
        '+mobility'   : 0,
        '+wits'       : 0,
        '+perception' : 0,
    }
)

VIVIEN = Blueprint(
    parents = CHARACTER,
    properties = {
        'name'     : "Leana",
        'portrait' : visual.Character.VIVIEN,
        '+hp'      : 1,
        '+mana'    : 1,
        '+dexterity'  : 0,
        '+agility'    : 0,
        '+mobility'   : 0,
        '+wits'       : 0,
        '+perception' : 0,
    }
)

SHALOTT = Blueprint(
    parents = CHARACTER,
    properties = {
        'name'     : "Shalott",
        'portrait' : visual.Character.SHALOTT,
        '+hp'      : -3,
        '+mana'    : 2,
        '+dexterity'  : 0,
        '+agility'    : 0,
        '+mobility'   : 0,
        '+wits'       : 0,
        '+perception' : 0,
    }
)

YORICK = Blueprint(
    parents = CHARACTER,
    properties = {
        'name'     : "Yorick",
        'portrait' : visual.Character.YORICK,
        '+hp'      : 1,
        '+mana'    : 1,
        '+dexterity'  : 0,
        '+agility'    : 0,
        '+mobility'   : 0,
        '+wits'       : 0,
        '+perception' : 0,
    }
)