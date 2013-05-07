'''
Created on Apr 28, 2013

@author: Devindra
'''

class Trait(object):

    def __init__(self, template):
        self.name = template.properties['name']
        self.description = template.properties['description']
        self.modifiers = template.properties['modifiers']
    
    #event
    def modify_property(self, value, prop, entity):
        if prop in self.modifiers.keys():
            #return self.modifiers[prop]
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
            