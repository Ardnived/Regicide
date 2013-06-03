'''
Created on Mar 23, 2013

@author: Devindra
'''
from regicide.mvc import State
from regicide.data import traits, items
from regicide.entity.entity import Entity
from regicide.entity.traits import Trait
from regicide.entity.actions import voodoo
from regicide.entity.items import Item
from regicide.entity import effects, properties

class Player(Entity):
    TURN = False

    def __init__(self, template, x=0, y=0):
        '''
        :param template: the blueprints.Master object to base this entity on.
        :param x: the initial x location on the map of this entity.
        :param y: the initial y location on the map of this entity.
        '''
        Entity.__init__(self, template=template, x=x, y=y)
        self.portrait = template.properties['portrait']
        
        
        # TODO: remove the following test code

        self.add_trait(Trait(traits.DEMON_PACT.master()))
        
        aptitude = Trait(traits.BLADE_APTITUDE.master())
        self.add_trait(aptitude)
        self.remove_trait(aptitude)
        self.add_trait(Trait(traits.BLADE_APTITUDE.master()))
        
        armour = Item(items.LEATHER_ARMOUR.master())
        self.add_item(armour)
        self.equip_item(armour)
        
        armour = Item(items.LEATHER_ARMOUR.master())
        self.add_item(armour)
        
        sword = Item(items.SWORD.master())
        self.add_item(sword)
        self.equip_item(sword)
        
        sword = Item(items.AXE.master())
        self.add_item(sword)
        
        sword = Item(items.POTION.master())
        self.add_item(sword)
        
        self.add_action(voodoo.AvianWisdom())
        self.add_action(voodoo.Possess())
        self.add_action(voodoo.Exorcism())
        
        self.add_effect(effects.Alert(12500))
        self.add_effect(effects.Ruin(4240))
        self.add_effect(effects.Wither(16310))
        self.add_effect(effects.Weakened(13520))

        self.recalculate_properties()
    
    def on_turn(self, game):
        game.accept_input = True
        
        game.log_message("Awaiting user input...")
        game.do_update('log')
    
    def on_death(self, game):
        game.move_entity(self, target=None)
        game.log_message("You die.")
        game.log_message("GAME OVER")
        game.do_update('log')
        
    def set(self, prop, value):
        Entity.set(self, prop, value)
        model = State.model()
        
        max_hp = self.get(properties.max_hp)
        
        if value <= 3 and prop.type == properties.Property.TYPE_ATTR:
            model.log_message("LOW ATTRIBUTE WARNING: "+prop.name)
            model.do_update('log')
        elif prop == properties.hp and self.get(properties.hp) <= max_hp*0.4:
            model.log_message("LOW HP WARNING: "+str(self.get(properties.hp)))
            model.do_update('log')
    
    def is_player(self):
        return True
        
        
        