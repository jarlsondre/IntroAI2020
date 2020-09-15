import Map
import math
# Implementation of the A* algorithm :)
def A_star_impl():

    # We want a heuristic function. To calculate this we'll use the euclidean distance.

    # placeholder while we're figuring things out
    return 0

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
