import Map
import math
# Implementation of the A* algorithm :)

class Node:
    
    def __init__(self, pos=[0,0]):
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        self.status = "open"
        self.parent = None
        self.kids = []
        self.pos = pos

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

    def get_pos(self):
        return self.pos

    def __str__(self):
        pos = "[" + str(self.pos[0]) + ", " + str(self.pos[1]) + "]"
        return pos 


def main():
    
    # Making the list of nodes:
    opened = []
    closed = []
    frontier = [] # the nodes we're going to be looking at next, sorted by their heuristic

    # Creating a map object:
    myMap = Map.Map_Obj(1)
    myMap.show_map()

    # Creating some instances of nodes and testing their positions;
    startNode = Node(myMap.get_start_pos())
    goalNode = Node(myMap.get_goal_pos())
    print("Goal node:", goalNode)
    print("Start node:", startNode)

    # Adding nodes to list:
    opened.append(startNode)
    frontier.append(startNode)

    # Testing the distance function:
    print("Manhattan distance between start and goal: ", manhattan_distance(startNode.get_pos(), goalNode.get_pos()))

def manhattan_distance(first_pos, second_pos): # Calculating the distance in how many steps it takes to move there
    hor_dist = abs(first_pos[0] - second_pos[0])
    ver_dist = abs(first_pos[1] - second_pos[1])
    return hor_dist + ver_dist
       

if __name__ == "__main__":
    main()

