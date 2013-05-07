'''
Created on Mar 2, 2013

@author: Devindra
'''

class TileMap(object):
    '''
    A grid of tiles.
    '''

    def __init__(self, width, height):
        '''
        Constructor
        '''
        self.grid = []
        self.width = width
        self.height = height
        
    def get_tile(self, x, y):
        if 0 <= x and x < self.width and 0 <= y and y < self.height:
            return self.grid[x][y]
        else:
            return None

        