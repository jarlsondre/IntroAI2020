import Map
import math


# Implementation of the A* algorithm :)

class Node:

    def __init__(self, pos=[0, 0]):
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0
        self.status = "open"
        self.parent = None
        self.kids = []
        self.pos = pos

    def set_h_cost(self, goal):
        self.h_cost = manhattan_distance(self.pos, goal)

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

    def get_g_cost(self):
        return self.g_cost

    def __str__(self):
        pos = "[" + str(self.pos[0]) + ", " + str(self.pos[1]) + "]"
        return pos

def task(task_number):
    # Making the list of nodes:
    opened = []
    closed = []
    frontier = []  # the nodes we're going to be looking at next, sorted by their heuristic

    # Creating a map object:
    myMap = Map.Map_Obj(task_number)
    myMap.show_map()

    # Creating some instances of nodes and testing their positions;

    startNode = Node(myMap.get_start_pos())
    startNode.set_g_cost(0)
    startNode.set_h_cost(myMap.get_goal_pos())
    startNode.set_f_cost()
    print("Start node:", startNode)
    print("Goal node:", myMap.get_goal_pos())

    # Adding node to list:
    opened.append(startNode)
    frontier.append(startNode)

    goal_not_found = True

    # This loop will run until we find the shortest path
    while goal_not_found:
        currentNode = frontier[0]

        # Checking if it´s the goal node:
        if currentNode.h_cost == 0:
            print("Hurra, du fant noden på: ", currentNode)
            break

        # If not, then we have to search further :)

        # Creating children in a plus shape
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i == 0) ^ (j == 0):
                    if myMap.get_cell_value([currentNode.get_pos()[0] + i, currentNode.get_pos()[1] + j]) != -1:
                        nodeExist = False
                        for elem in opened:
                            if elem.pos == [currentNode.get_pos()[0] + i, currentNode.get_pos()[1] + j]:
                                node = elem
                                nodeExist = True
                                break

                        if not nodeExist:
                            node = Node([currentNode.get_pos()[0] + i, currentNode.get_pos()[1] + j])
                        if not node in closed:
                            node.set_parent(currentNode)
                            currentNode.add_child(node)
                            node.set_g_cost(node.parent.get_g_cost() + myMap.get_cell_value([currentNode.get_pos()[0] + i, currentNode.get_pos()[1] + j]))
                            node.set_h_cost(myMap.get_goal_pos())
                            node.set_f_cost()
                            opened.append(node)
                            frontier.append(node)

        frontier.sort(key=lambda x: x.f_cost)

        frontier.remove(currentNode)
        closed.append(currentNode)

        goal_path = [currentNode]

    while currentNode.parent is not None:
        currentNode = currentNode.parent
        goal_path.append(currentNode)

    for node in goal_path:
        myMap.set_cell_value(node.get_pos(), 'G')
    myMap.show_map()

def main():
    task(1)
    task(2)
    task(3)
    task(4)




def manhattan_distance(first_pos, second_pos):  # Calculating the distance in how many steps it takes to move there
    hor_dist = abs(first_pos[0] - second_pos[0])
    ver_dist = abs(first_pos[1] - second_pos[1])
    return hor_dist + ver_dist


if __name__ == "__main__":
    main()
