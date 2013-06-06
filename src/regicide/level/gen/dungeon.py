'''
Created on 2013-06-02

@author: Devindra
'''
from regicide.level.gen.generator import MapGenerator

class DungeonGenerator(MapGenerator):

    def generate(self, options):
        MapGenerator.generate(self, options)
        
        return self.decode_map()
