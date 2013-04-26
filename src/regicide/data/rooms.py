'''
Created on Mar 11, 2013

@author: Devindra

Data definitions for all rooms in the game.
'''
from regicide.data.blueprints import Blueprint
from regicide.data.functions import pick, add

print("Loading Rooms...")

CORRIDOR_HORIZONTAL = Blueprint(
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
    },
)

CORRIDOR_VERTICAL = Blueprint(
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
    },
)

STAIRWELL = Blueprint(
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

