'''
Created on Apr 28, 2013

@author: Devindra
'''

class Item(object):

    def __init__(self, template):
        self.name = template.properties['name']
        self.description = template.properties['description']
        self.type = template.properties['type']
        
        if template.properties.has_key('weight'):
            self.weight = template.properties['weight']
        else:
            self.weight = 1.0
        
        if template.properties.has_key('modifiers'):
            self.modifiers = template.properties['modifiers']
        else:
            self.modifiers = {}
        
        if template.properties.has_key('equip_slot'):
            self.equip_slot = template.properties['equip_slot']
        if template.properties.has_key('equip_size'):
            self.equip_size = template.properties['equip_size']
        
        skills = template.properties['skills']
        if skills.has_key('wield'):
            self.wield_skill = skills['wield']
        if skills.has_key('equip'):
            self.equip_skill = skills['equip']
        if skills.has_key('use'):
            self.use_skill = skills['use']
    
    #event
    def modify_property(self, value, prop, entity):
        if prop in self.modifiers.keys():
            modifier = self.modifiers[prop]
            operator = modifier[0]
            modification = modifier[1]
            
            if operator == '+':
                return value + modification
            elif operator == '-':
                return value - modification
            elif operator == '/':
                return int(value / modification)
            elif operator == '*':
                return int(value * modification)

class Equippable(Item):
    
    def __init__(self, template):
        Item.__init__(self, template)
    
class Weapon(Equippable):
    
    def __init__(self, template):
        Equippable.__init__(self, template)
    
class Potion(Item):
    
    def __init__(self, template):
        Item.__init__(self, template)
    
class Ammunition(Item):
    
    def __init__(self, template):
        Item.__init__(self, template)
    
