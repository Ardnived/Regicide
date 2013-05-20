'''
Created on Mar 2, 2013

@author: Devindra
'''
from __future__ import division
import heapq
import math

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
        
        # Stores line of sight mappings that have already been determined.
        # This might end up costing too much memory to store.
        # So consider removing it.
        self.los_map = {}
        
    def get_tile(self, x, y):
        if 0 <= x and x < self.width and 0 <= y and y < self.height:
            return self.grid[x][y]
        else:
            return None

    def modify_light(self, source_x, source_y, strength):
        if strength == 0:
            return
        elif strength < 0:
            positive = False
            strength = abs(strength)
        else:
            positive = True
        
        for x in xrange(-strength, strength+1):
            light_range = strength - abs(x)
            for y in xrange(-light_range, light_range+1):
                target_x = source_x + x
                target_y = source_y + y
                tile = self.get_tile(target_x, target_y)
            
                if tile is not None and self.has_line_of_sight(source_x, source_y, target_x, target_y):
                    modifier = strength - abs(x) - abs(y)
                    
                    if positive:
                        #print("Decreasing Shadows by "+str(modifier))
                        tile.shadow -= modifier
                    else:
                        #print("Increasing Shadows by "+str(modifier))
                        tile.shadow += modifier
    
    def has_line_of_sight(self, source_x, source_y, target_x, target_y):
        response = self._has_los(source_x, source_y, target_x, target_y)
        
        if response is False:
            target = self.get_tile(target_x, target_y)
            if target is not None and target.is_opaque():
                sign_x = int(math.copysign(1, target_x - source_x))
                sign_y = int(math.copysign(1, target_y - source_y))
                
                tile = self.get_tile(target_x - sign_x, target_y)
                if tile is not None and not tile.is_opaque() and self._has_los(source_x, source_y, target_x - sign_x, target_y):
                    return True
                
                tile = self.get_tile(target_x, target_y - sign_y)
                if tile is not None and not tile.is_opaque() and self._has_los(source_x, source_y, target_x, target_y - sign_y):
                    return True
                
                tile = self.get_tile(target_x - sign_x, target_y - sign_y)
                if tile is not None and not tile.is_opaque() and self._has_los(source_x, source_y, target_x - sign_x, target_y - sign_y):
                    return True
        
        return response

    def _has_los(self, source_x, source_y, target_x, target_y):
        '''
        Brensenham line algorithm
        '''
        steep = 0
        
        dx = abs(target_x - source_x)
        if target_x - source_x > 0: 
            sign_x = 1
        else: 
            sign_x = -1
            
        dy = abs(target_y - source_y)
        if (target_y - source_y) > 0: 
            sign_y = 1
        else: 
            sign_y = -1
        
        x = source_x
        y = source_y
        
        if dy > dx:
            steep = 1
            x, y = y, x
            dx, dy = dy, dx
            sign_x, sign_y = sign_y, sign_x
        
        d = (2 * dy) - dx
        for _ in xrange(0,dx):
            if steep: 
                tile = self.get_tile(y, x)
            else: 
                tile = self.get_tile(x, y)
                
            if tile is None or tile.is_opaque():
                return False
            
            while d >= 0:
                y = y + sign_y
                d = d - (2 * dx)
            
            x = x + sign_x
            d = d + (2 * dy)
        
        return True
    
    def find_path(self, algorithm, source_x, source_y, target_x, target_y):
        return algorithm(source_x, source_y, target_x, target_y)
    
    class _astar_node(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.parent = None
            self.g = 0
            self.h = 0
            self.f = 0
            
        @property
        def key(self):
            return (self.x, self.y)
    
    def _astar_passage_reachable(self, x, y):
        return self.get_tile(x, y) is None
    
    def _astar_passage(self, source_x, source_y, target_x, target_y):
        return self._astar_helper(source_x, source_y, target_x, target_y, strict=True, reachable_func=self._astar_passage_reachable)
    
    def _astar_reachable(self, x, y):
        tile = self.get_tile(x, y)
        return tile is not None and tile.is_passable()
    
    def _astar(self, source_x, source_y, target_x, target_y):
        return self._astar_helper(source_x, source_y, target_x, target_y, strict=False, reachable_func=self._astar_reachable)
    
    def _astar_helper(self, source_x, source_y, target_x, target_y, strict, reachable_func):
        open_list = []
        closed_list = set([])
        node_list = {}
        start = TileMap._astar_node(source_x, source_y)
        end = TileMap._astar_node(target_x, target_y)
        
        # add starting node to open heap queue
        heapq.heappush(open_list, (start.f, start.key))
        node_list[start.key] = start
        
        while len(open_list):
            # pop node from heap queue 
            _, node_key = heapq.heappop(open_list)
            node = node_list[node_key]
            
            # add node to closed list so we don't process it twice
            closed_list.add(node.key)
            
            # if ending node, display found path
            if node_key == end.key:
                results = []
                while node.parent.key != start.key:
                    node = node.parent
                    results.append(node.key)
                
                return results
            
            # get adjacent nodes for node
            for adj_node in self._astar_adjacent_nodes(node, node_list, strict):
                reachable = reachable_func(adj_node.x, adj_node.y) or adj_node.key == end.key
                if reachable and adj_node.key not in closed_list: #adj_node not in closed_list:
                    if (adj_node.f, adj_node.key) in open_list:
                        # if adj node in open list, check if current path is
                        # better than the one previously found for this adj
                        # node.
                        if adj_node.g > node.g + 1:
                            # update node
                            adj_node.g = node.g + 1
                            adj_node.h = self._astar_heuristic(adj_node, end)
                            adj_node.parent = node
                            adj_node.f = adj_node.h + adj_node.g
                    else:
                        # update node
                        adj_node.g = node.g + 1
                        adj_node.h = self._astar_heuristic(adj_node, end)
                        adj_node.parent = node
                        adj_node.f = adj_node.h + adj_node.g
                        
                        # add adj node to openen list
                        heapq.heappush(open_list, (adj_node.f, adj_node.key))
                        node_list[adj_node.key] = adj_node
                        
        return None # Can't reach target.
    
    def _astar_heuristic(self, source, target):
        return (abs(source.x - target.x) + abs(source.y - target.y))/2

    def _astar_adjacent_nodes(self, node, node_list, strict):
        """
        Returns adjacent nodes to a node. clockwise starting
        from the one on the right.
    
        @param node get adjacent nodes for this node
        @returns adjacent nodes list 
        """
        east = node.x < self.width - 2
        south = node.y > 1
        west = node.x > 1
        north = node.y < self.height - 2
        
        nodes = []
        if east:
            nodes.append(self._astar_get_node(node.x+1, node.y, node_list))
        if not strict and east and south:
            nodes.append(self._astar_get_node(node.x+1, node.y-1, node_list))
        if south:
            nodes.append(self._astar_get_node(node.x, node.y-1, node_list))
        if not strict and south and west:
            nodes.append(self._astar_get_node(node.x-1, node.y-1, node_list))
        if west:
            nodes.append(self._astar_get_node(node.x-1, node.y, node_list))
        if not strict and west and north:
            nodes.append(self._astar_get_node(node.x-1, node.y+1, node_list))
        if north:
            nodes.append(self._astar_get_node(node.x, node.y+1, node_list))
        if not strict and north and east:
            nodes.append(self._astar_get_node(node.x+1, node.y+1, node_list))
        return nodes
    
    def _astar_get_node(self, x, y, node_list):
        if node_list.has_key((x, y)):
            return node_list[(x, y)]
        else:
            return TileMap._astar_node(x, y)
    
    def _dijkstra(self, source_x, source_y, target_x, target_y):
        pass
    
    ALGORITHM_ASTAR = _astar
    ALGORITHM_ASTAR_PASSAGE = _astar_passage
    ALGORITHM_DIJKSTRA = _dijkstra

    
        