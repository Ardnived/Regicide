'''
Created on Mar 26, 2013

@author: Devindra

This module defines the various equip slots on a standard character.
'''

class EquipSlot(object):
    def __init__(self, name, size):
        '''
        :param name: the display name of this slot.
        :param size: an arbitrary number which defines the size of this equip slot.
        This value must be considered in conjunction with the size of various items.
        '''
        self.name = name
        self.size = size

head = EquipSlot("Head", 1)
face = EquipSlot("Face", 1)
torso = EquipSlot("Torso", 1)
back = EquipSlot("Back", 1)
arm = EquipSlot("Arms", 2)
hand = EquipSlot("Hands", 3)
trinket = EquipSlot("Trinket", 1)
finger = EquipSlot("Fingers", 8)
leg = EquipSlot("Legs", 2)
foot = EquipSlot("Feet", 2)
