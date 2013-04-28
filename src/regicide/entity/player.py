'''
Created on Mar 23, 2013

@author: Devindra
'''
from regicide.entity.entity import Entity
from regicide.data import traits, items
from regicide.actions import voodoo
from regicide.entity import effects

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

        self.add_trait(traits.DEMON_PACT.master())
        
        aptitude = traits.BLADE_APTITUDE.master()
        self.add_trait(aptitude)
        self.remove_trait(aptitude)
        self.add_trait(traits.BLADE_APTITUDE.master())
        
        armour = items.LEATHER_ARMOUR.master()
        self.add_item(armour)
        self.equip_item(armour)
        
        sword = items.SWORD.master()
        self.add_item(sword)
        self.equip_item(sword)
        
        self.add_action(voodoo.AvianWisdom())
        self.add_action(voodoo.Possess())
        self.add_action(voodoo.Exorcism())
        
        self.add_effect(effects.Alert())
        self.add_effect(effects.Ruin())
        self.add_effect(effects.Wither())
        self.add_effect(effects.Weakened())
    
    def on_turn(self, game):
        game.accept_input = True
        
        game.log_message("Awaiting user input...")
        game.do_update('log')
        
        
        