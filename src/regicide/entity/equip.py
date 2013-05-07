'''
Created on Mar 26, 2013

@author: Devindra

This module defines the various equip slots on a standard character.
'''

class EquipSlot(object):
    
    def __init__(self, name,
            size = 1, 
            size_descriptions = [''],
            equip_description = "equip",
            unequip_description = "unequip",
            slot_descriptions = [],
            plural = None,
        ):
        '''
        :param name: the display name of this slot.
        :param size: an arbitrary number which defines the size of this equip slot.
        This value must be considered in conjunction with the size of various items.
        '''
        self.name = name
        self.size = size
        self.equip_description = equip_description
        self.unequip_description = unequip_description
        self._size_descriptions = size_descriptions
        self._slot_descriptions = slot_descriptions
        
        if plural is None:
            self.plural = name+"s"
        else:
            self.plural = plural
    
    def get_size_description(self, size):
        length = len(self._size_descriptions)
        if length >= size:
            return self._size_descriptions[size-1]
        else:
            return self._size_descriptions[length-1]
    
    def get_slot_description(self, slot):
        if self.size != 1 and len(self._slot_descriptions) >= slot:
            return self._slot_descriptions[slot]
        else:
            return self.name

head = EquipSlot(
    name = "Head",
    unequip_description = "remove",
)
face = EquipSlot(
    name = "Face",
    unequip_description = "remove",
)
torso = EquipSlot(
    name = "Torso",
    equip_description = "don",
    unequip_description = "remove",
)
back = EquipSlot(
    name = "Back",
    equip_description = "don",
    unequip_description = "remove",
)
arm = EquipSlot(
    name = "Arms",
)
hand = EquipSlot(
    name = "Hand", 
    size = 3,
    equip_description = "wield",
    unequip_description = "unwield",
    size_descriptions = ["Light", "Normal", "Two Hand"],
    slot_descriptions = ["Main Hand", "Off Hand"],
)
trinket = EquipSlot(
    name = "Trinket", 
    size = 3,
    equip_description = "wield",
    unequip_description = "unwield",
    size_descriptions = ["Medium", "Large"],
    slot_descriptions = ["Trinket 1", "Trinket 2", "Trinket 3"],
)
finger = EquipSlot(
    name = "Finger", 
    size = 2,
    slot_descriptions = ["Left Ring", "Right Ring"],
)
leg = EquipSlot(
    name = "Legs", 
    equip_description = "don",
    unequip_description = "remove",
)
foot = EquipSlot(
    name = "Feet", 
    equip_description = "don",
    unequip_description = "remove",
)