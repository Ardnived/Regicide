'''
Created on Mar 11, 2013

@author: Devindra

Data definitions for all rooms in the game.
'''
from regicide.data.blueprints import Blueprint
from regicide.data.functions import pick, add

print("Loading Rooms...")

ROOM = Blueprint(
    hidden = True,
    domains = {
        'category': 'room',
    },
    properties = {
        'max_connections': 5,
        'allow_passages': True,
    },
)

CORRIDOR_HORIZONTAL = Blueprint(
    parents = ROOM,
    domains = {
        'type': ['corridor', 'horizontal corridor'],
        'floor': 'commons',
        'zone': 'castle',
    },
    properties = {
        'name': "Corridor",
        'width': [pick, range(5, 12)],
        'height': [pick, range(2, 3)],
        'connections': ['vertical corridor', 'room'],
        'add_doors': ['room'],
        'allow_passages': False,
    },
)

CORRIDOR_VERTICAL = Blueprint(
    parents = ROOM,
    domains = {
        'type': ['corridor', 'vertical corridor'],
        'floor': 'commons',
        'zone': 'castle',
    },
    properties = {
        'name': "Corridor",
        'width': [pick, range(2, 3)],
        'height': [pick, range(5, 12)],
        'connections': ['horizontal corridor', 'room'],
        'add_doors': ['room'],
        'allow_passages': False,
    },
)

STAIRWELL = Blueprint(
    parents = ROOM,
    domains = {
        'type': 'stairwell',
        'floor': 'commons',
        'zone': 'castle',
    },
    properties = {
        'name': "Stairwell",
        'width': [pick, range(2, 3)],
        'height': [pick, range(2, 3)],
        'connections': ['corridor'],
    },
)

BEDROOM = Blueprint(
    parents = ROOM,
    domains = {
        'type': 'room',
        'floor': 'commons',
        'zone': 'castle',
    },
    properties = {
        'name': [add, [[pick, ["King's", "Jester's"]], " Room"]],
        'width': [pick, range(2, 4)],
        'height': [pick, range(2, 4)],
        'guards': [{'race': 'goblin'}],
        'connections': ['corridor'],
    },
)

ARMOURY = Blueprint(
    parents = ROOM,
    domains = {
        'type': 'room',
        'floor': 'commons',
        'zone': 'castle',
    },
    properties = {
        'name': "Armoury",
        'width': [pick, range(2, 4)],
        'height': [pick, range(2, 4)],
        'guards': [{'race': 'goblin'}],
        'connections': ['corridor'],
    },
)

ANTECHAMBER = Blueprint(
    parents = ROOM,
    domains = {
        'type': 'room',
        'floor': 'commons',
        'zone': 'castle',
    },
    properties = {
        'name': "Antechamber",
        'width': [pick, range(2, 4)],
        'height': [pick, range(2, 4)],
        'guards': [{'race': 'goblin'}],
        'connections': ['room'],
    },
)

DINING_HALL = Blueprint(
    parents = ROOM,
    domains = {
        'type': 'room',
        'floor': 'commons',
        'zone': 'castle',
    },
    properties = {
        'name': "Dining Hall",
        'width': [pick, range(5, 8)],
        'height': [pick, range(5, 8)],
        'guards': [{'race': 'goblin'}],
        'connections': ['kitchen'],
        'max_connections': 3,
    },
)

KITCHEN = Blueprint(
    parents = ROOM,
    domains = {
        'type': 'kitchen',
        'floor': 'commons',
        'zone': 'castle',
    },
    properties = {
        'name': "Kitchen",
        'width': [pick, range(2, 3)],
        'height': [pick, range(3, 6)],
        'guards': [{'race': 'goblin'}],
        'connections': [],
    },
)

THRONE_ROOM = Blueprint(
    parents = ROOM,
    domains = {
        'type': 'throne',
        'floor': 'commons',
        'zone': 'castle',
    },
    properties = {
        'name': "Throne Room",
        'width': [pick, range(5, 8)],
        'height': [pick, range(5, 8)],
        'guards': [{'race': 'goblin'}],
        'connections': ['room'],
        'max_connections': 3,
    },
)

