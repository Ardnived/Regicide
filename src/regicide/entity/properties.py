'''
Created on Mar 24, 2013

@author: Devindra

Defines all the valid properties for an entity.
'''

class Property(object):
    TYPE_ATTR = 0 # The property is an attribute.
    TYPE_ATTR_SUB = 1 # sub attribute.
    TYPE_SKILL = 2 # skill level.
    TYPE_PROPERTY = 3 # an arbitrary property.
    
    def __init__(self, name, base, property_type):
        self.name = name
        self.base = base
        self.type = property_type

# Attributes
dexterity = Property('Dexterity', 0, Property.TYPE_ATTR)
agility = Property('Agility', 0, Property.TYPE_ATTR)
mobility = Property('Mobility', 0, Property.TYPE_ATTR)
wits = Property('Wits', 0, Property.TYPE_ATTR)
perception = Property('Perception', 0, Property.TYPE_ATTR)

# Sub Attributes
max_hp = Property('Max Health', 0, Property.TYPE_ATTR_SUB)
hp = Property('Health', max_hp, Property.TYPE_ATTR_SUB)
max_mana = Property('Max Mana', 0, Property.TYPE_ATTR_SUB)
mana = Property('Mana', max_mana, Property.TYPE_ATTR_SUB)

# Item Statistics
damage = Property('Damage', 0, Property.TYPE_ATTR_SUB)
defense = Property('Defense', 0, Property.TYPE_ATTR_SUB)

# Skills
swords = Property('Swords', 0, Property.TYPE_SKILL)
axes = Property('Axes', 0, Property.TYPE_SKILL)
daggers = Property('Daggers', 0, Property.TYPE_SKILL)

voodoo = Property('Voodoo', wits, Property.TYPE_SKILL)
witchcraft = Property('Witchcraft', wits, Property.TYPE_SKILL)
sorcery = Property('Sorcery', wits, Property.TYPE_SKILL)

locks = Property('Lockpicking', dexterity, Property.TYPE_SKILL)
evade = Property('Trap Evasion', agility, Property.TYPE_SKILL)
disarm = Property('Trap Disarm', dexterity, Property.TYPE_SKILL)

dodge = Property('Dodge', mobility, Property.TYPE_SKILL)
initiative = Property('Initiative', mobility, Property.TYPE_SKILL)
move = Property('Move Speed', mobility, Property.TYPE_SKILL)
identify = Property('Identify', wits, Property.TYPE_SKILL)
equip = Property('Equip', agility, Property.TYPE_SKILL)

# Properties
corruption = Property('Corruption', 0, Property.TYPE_PROPERTY)
purity = Property('Purity', 0, Property.TYPE_PROPERTY)
spirit = Property('Spirit', 0, Property.TYPE_PROPERTY)
hexed = Property('Hexed', 0, Property.TYPE_PROPERTY)
toxicity = Property('Toxicity', 0, Property.TYPE_PROPERTY)
finesse = Property('Finesse', 0, Property.TYPE_PROPERTY)
