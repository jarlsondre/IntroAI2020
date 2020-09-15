import Map
import math
# Implementation of the A* algorithm :)

class Node:
    
    def __init__(self):
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        self.status = "open"
        self.parent = None
        self.kids = []

    def set_h_cost(self, pos, goal):
        self.h_cost = heuristic(pos, goal)

    def close_node(self):
        self.status = "closed"

    def set_g_cost(self, cost):
        self.g_cost = cost

    def set_f_cost(self):
        self.f_cost = self.h_cost + self.g_cost

    def set_parent(self, parent):
        self.parent = parent

    def add_child(self, child):
        self.kids.append(child)

def A_star_impl():
    pass

def heuristic(node, goal):
    # Calculating the euclidean distance between a node and the goal node:
    hor_dist = abs(node[0] - goal[0])
    ver_dist = abs(node[1] - goal[1])
    distance = math.sqrt(hor_dist**2 + ver_dist**2) 
    print(distance)
    return distance
    

# task = int(input("Which task are you on? (int)"))
myMap = Map.Map_Obj(1)
myMap.show_map()
heuristic([5, 5], myMap.get_goal_pos())
