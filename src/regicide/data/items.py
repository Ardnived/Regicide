'''
Created on Mar 11, 2013

@author: Devindra

Data definitions for all items in the game.
'''
from regicide.data.blueprints import Blueprint, Factory, Mod
from regicide.data.functions import source, pick, add, multiply, divide, mod
from regicide.resources import visual
from regicide.entity import equip
from regicide.entity import properties

print("Loading Items...")

ITEM = Blueprint(
    hidden = True,
    domains = {
        'category': 'item',
    },
    properties = {
        'skills': {
            'wield': properties.dexterity,
            'equip': properties.agility,
            'use': properties.wits,
        },
    },
)

ARMOUR = Blueprint(
    hidden = True,
    parents = ITEM,
    domains = {
        'type': 'armour'
    },
    properties = {
        'skills': {
            'wield': properties.agility,
            'equip': properties.agility,
        },
    },
)

LEATHER_ARMOUR = Blueprint(
    parents = ARMOUR,
    domains = {
        'type': 'axe'
    },
    properties = {
        'name'   : "Leather Armour",
        #'sprite' : visual.Misc.AXE_6,
        'equip_slot': equip.torso,
        'equip_size': 1,
        'modifiers': {
            properties.defense: ['+', 3],
        },
    },
)

WEAPON = Blueprint(
    hidden = True,
    parents = ITEM,
    domains = {
        'type': 'weapon'
    },
    properties = {
        
    },
)

AXE = Blueprint(
    parents = WEAPON,
    domains = {
        'type': 'axe'
    },
    properties = {
        'name'   : "Axe",
        #'sprite' : visual.Misc.AXE_6,
        'equip_slot': equip.hand,
        'equip_size': 3,
        'modifiers': {
            properties.damage: ['+', 4],
        },
        'skills': {
            'wield': properties.axes,
            'equip': properties.agility,
        },
    },
)

SWORD = Blueprint(
    parents = WEAPON,
    domains = {
        'type': 'blade'
    },
    properties = {
        'name'   : "Sword",
        #'sprite' : visual.Misc.SWORD_7,
        'equip_slot': equip.hand,
        'equip_size': 2,
        'modifiers': {
            properties.damage: ['+', 2],
        },
        'skills': {
            'wield': properties.swords,
            'equip': properties.dexterity,
        },
    },
)

POTION = Blueprint(
    parents = ITEM,
    domains = {
        'type': 'consumable'
    },
    properties = {
        'name'   : "Main Potion",
        'effect' : 'normal',
        'strength' : (pick, range(4, 6)),
        #'sprite' : visual.Misc.SWORD_7,
        'equip_slot': equip.hand,
        'equip_size': 1,
    },
)

ALT_POTION = Blueprint(
    parents = ITEM,
    domains = {
        'type': 'consumable'
    },
    properties = {
        'name'   : "Alt Potion",
        'effect' : 'normal',
        'strength' : (pick, range(4, 6)),
        #'sprite' : visual.Misc.SWORD_7,
    },
)

CRAZY = Mod(
    category = 'effect',
    properties = {
        'effect': "death",
        'strength': (multiply, [(source, 'strength'), 1.5]),
        'name': (add, ["Crazy ", (source, 'name')]),
    },
)

ZANY = Mod(
    category = 'effect',
    properties = {
        'effect': "insanity",
        'strength': (divide, ((source, 'strength'), 2)),
        'name': (add, ("Zany ", (source, 'name'))),
    },
)

CRAZY_POTION = Factory(
    blueprint = (pick, (POTION, ALT_POTION)),
    mods = (pick, (mod, 'effect')),
    properties = {
        #'name': (add, ("Random ", (source, 'name'))),
    },
)
