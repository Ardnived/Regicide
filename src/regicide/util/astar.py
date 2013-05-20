# Copenyright (c) 2010 Brandon Sterne
# Licensed under the MIT license.
# http://brandon.sternefamily.net/files/mit-license.txt
# Python A-Star (A*) Implementation

import heapq

class Node(object):
    def __init__(self, x, y, reachable):
        """
        Initialize new node

        @param x node x coordinate
        @param y node y coordinate
        @param reachable is node reachable? not a wall?
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

class AStar(object):
    def __init__(self):
        self.open = heapq.heapify([])
        self.closed = set()
        self.nodes = []
        self.gridHeight = 6
        self.gridWidth = 6

    def init_grid(self):
        walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3), 
                 (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
        for x in range(self.gridWidth):
            for y in range(self.gridHeight):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.nodes.append(Node(x, y, reachable))
        self.start = self.get_node(0, 0)
        self.end = self.get_node(5, 5)

    def get_heuristic(self, node):
        """
        Compute the heuristic value H for a node: distance between
        this node and the ending node multiply by 10.
    
        @param node
        @returns heuristic value H
        """
        return 10 * (abs(node.x - self.end.x) + abs(node.y - self.end.y))
    
    def get_node(self, x, y):
        """
        Returns a node from the nodes list
    
        @param x node x coordinate
        @param y node y coordinate
        @returns node
        """
        return self.nodes[x * self.gridHeight + y]

    def get_adjacent_nodes(self, node):
        """
        Returns adjacent nodes to a node. closedockwise starting
        from the one on the right.
    
        @param node get adjacent nodes for this node
        @returns adjacent nodes list 
        """
        nodes = []
        if node.x < self.gridWidth-1:
            nodes.append(self.get_node(node.x+1, node.y))
        if node.y > 0:
            nodes.append(self.get_node(node.x, node.y-1))
        if node.x > 0:
            nodes.append(self.get_node(node.x-1, node.y))
        if node.y < self.gridHeight-1:
            nodes.append(self.get_node(node.x, node.y+1))
        return nodes

    def display_path(self):
        node = self.end
        while node.parent is not self.start:
            node = node.parent
            print 'path: node: %d,%d' % (node.x, node.y)

    def update_node(self, adj, node):
        """
        Update adjacent node
    
        @param adj adjacent node to current node
        @param node current node being processed
        """
        adj.g = node.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = node
        adj.f = adj.h + adj.g

    def process(self):
        # add starting node to openen heap queue
        heapq.heappush(self.open, (self.start.f, self.start))
        
        while len(self.open):
            # popen node from heap queue 
            f, node = heapq.heappop(self.open)
            
            # add node to closedosed list so we don't process it twice
            self.closed.add(node)
            
            # if ending node, display found path
            if node is self.end:
                self.display_path()
                break
            
            # get adjacent nodes for node
            for c in self.get_adjacent_nodes(node):
                if c.reachable and c not in self.closed:
                    if (c.f, c) in self.open:
                        # if adj node in openen list, check if current path is
                        # better than the one previously found for this adj
                        # node.
                        if c.g > node.g + 10:
                            self.update_node(c, node)
                    else:
                        self.update_node(c, node)
                        # add adj node to openen list
                        heapq.heappush(self.open, (c.f, c))

