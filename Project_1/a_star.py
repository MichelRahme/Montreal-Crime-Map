# -------------------------------------------------------
# Assignment 1
# Written by Michel Rahme 40038465
# For COMP 472 Section IX – Summer 2020
# --------------------------------------------------------

import numpy as np
import bisect


class Node:
    def __init__(self, parent, location):
        self.parent = parent
        self.location = location
        self.g = 100000000
        self.h = 0
        self.f = 0

    # Sort nodes
    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        else:
            return self.f < other.f

    def __eq__(self, other):
        return self.location == other.location


class PathGenerator:

    def __init__(self, grid_size, grid_count, bound):
        self.grid_size = grid_size
        self.grid_count = grid_count
        self.bound = bound

    # The actual A star algorithm
    def a_star(self, start, end):
        startNode = Node(None, start)
        endNode = Node(None, end)
        openList = []
        closedList = []
        openList.append(startNode)
        while len(openList) > 0:

            current_node = openList[0]

            if current_node.location == endNode.location:
                path = []
                current = current_node
                while current is not None:
                    path.append(current)
                    current = current.parent
                return path[::-1]

            openList.pop(0)
            closedList.append(current_node)
            neighbours = self.get_neighbors(current_node)

            for neighbour in neighbours:
                insert = True

                if neighbour in closedList:
                    insert = False # if neighbour is already in closed list, do not add to the open list

                if insert:
                    neighbour.h = self.heuristic(neighbour.location, endNode.location)
                    neighbour.f = neighbour.g + neighbour.h
                    bisect.insort_left(openList, neighbour)
        return False

    # This function will get the neighbours of each node, calculate their G function based
    # on the threshold then return them in a list
    def get_neighbors(self, parent):
        neighbours = []
        grid_size = self.grid_size

        # List that holds all possible 8-sided movements
        around = np.array([[0, grid_size],
                           [grid_size, 0],
                           [-grid_size, 0],
                           [0, -grid_size],
                           [grid_size, grid_size],
                           [grid_size, -grid_size],
                           [-grid_size, grid_size],
                           [-grid_size, -grid_size]
                           ])
        # These condition makes sure the boundary edges of the map are considered as inaccessible.
        if parent.location[0] == -73.59 and parent.location[1] == 45.49:
            around = np.array([[grid_size, grid_size]])
        if parent.location[0] == -73.59 and parent.location[1] == round((45.530 - grid_size), 3):
            around = np.array([[grid_size, 0], [grid_size, -grid_size]])
        if parent.location[0] == round((-73.55 - grid_size), 3) and parent.location[1] == round((45.530 - grid_size),
                                                                                                3):
            around = np.array([[0, -grid_size], [-grid_size, 0], [-grid_size, -grid_size]])
        if parent.location[0] == round((-73.55 - grid_size), 3) and parent.location[1] == 45.49:
            around = np.array([[0, grid_size]])

        # check each neighbour
        for x in around:
            neighbour = [round(parent.location[0] + x[0], 3), round(parent.location[1] + x[1], 3)]

            if x[0] == 0 and x[1] == grid_size:
                testNode_1 = [neighbour[0], neighbour[1] - grid_size]
                testNode_2 = [neighbour[0] - grid_size, neighbour[1] - grid_size]
                newNode = self.adjacent_neighbour_node(testNode_1, testNode_2, parent, neighbour)
                if newNode is not None:
                    neighbours.append(newNode)

            if x[0] == grid_size and x[1] == 0:
                testNode_1 = [neighbour[0] - grid_size, neighbour[1]]
                testNode_2 = [neighbour[0] - grid_size, neighbour[1] - grid_size]
                newNode = self.adjacent_neighbour_node(testNode_1, testNode_2, parent, neighbour)
                if newNode is not None:
                    neighbours.append(newNode)

            if x[0] == -grid_size and x[1] == 0:
                testNode_1 = [neighbour[0], neighbour[1]]
                testNode_2 = [neighbour[0], neighbour[1] - grid_size]
                newNode = self.adjacent_neighbour_node(testNode_1, testNode_2, parent, neighbour)
                if newNode is not None:
                    neighbours.append(newNode)

            if x[0] == 0 and x[1] == -grid_size:
                testNode_1 = [neighbour[0], neighbour[1]]
                testNode_2 = [neighbour[0] - grid_size, neighbour[1]]
                newNode = self.adjacent_neighbour_node(testNode_1, testNode_2, parent, neighbour)
                if newNode is not None:
                    neighbours.append(newNode)

            if x[0] == grid_size and x[1] == grid_size:
                testNode = [neighbour[0] - grid_size, neighbour[1] - grid_size]
                newNode = self.diagonal_neighbour_node(testNode, parent, neighbour)
                if newNode is not None:
                    neighbours.append(newNode)

            if x[0] == grid_size and x[1] == -grid_size:
                testNode = [neighbour[0] - grid_size, neighbour[1]]
                newNode = self.diagonal_neighbour_node(testNode, parent, neighbour)
                if newNode is not None:
                    neighbours.append(newNode)

            if x[0] == -grid_size and x[1] == grid_size:
                testNode = [neighbour[0], neighbour[1] - grid_size]
                newNode = self.diagonal_neighbour_node(testNode, parent, neighbour)
                if newNode is not None:
                    neighbours.append(newNode)

            if x[0] == -grid_size and x[1] == -grid_size:
                testNode = [neighbour[0], neighbour[1]]
                newNode = self.diagonal_neighbour_node(testNode, parent, neighbour)
                if newNode is not None:
                    neighbours.append(newNode)

        return neighbours

    def adjacent_neighbour_node(self, testNode_1, testNode_2, parent, neighbour):
        testNode_1_state = 1
        testNode_2_state = 1
        for y in self.grid_count:
            if round(testNode_1[0], 3) == y[0] and round(testNode_1[1], 3) == y[1] and y[2] < self.bound:
                testNode_1_state = 0
            if round(testNode_2[0], 3) == y[0] and round(testNode_2[1], 3) == y[1] and y[2] < self.bound:
                testNode_2_state = 0
        if testNode_1_state == 0 and testNode_2_state == 0:
            newNode = Node(parent, neighbour)
            newNode.g = parent.g + 1
        if (testNode_1_state == 1 and testNode_2_state == 0) or (testNode_1_state == 0 and testNode_2_state == 1):
            newNode = Node(parent, neighbour)
            newNode.g = parent.g + 1.3
        if testNode_1_state == 1 and testNode_2_state == 1:
            return None
        return newNode

    def diagonal_neighbour_node(self, testNode, parent, neighbour):
        testNode_state = 1
        for y in self.grid_count:
            if round(testNode[0], 3) == y[0] and round(testNode[1], 3) == y[1] and y[2] < self.bound:
                testNode_state = 0
        if testNode_state == 0:
            newNode = Node(parent, neighbour)
            newNode.g = parent.g + 1.5
        else:
            return None
        return newNode

    # Diagonal heuristic because of 8-Movement. Please not that I multiplied it by 500 and 250 to match the G function
    # or else the heuristic would be useless.
    def heuristic(self, current, end):
        distance_x = round(abs((current[0]) - (end[0])), 3)
        distance_y = round(abs((current[1]) - (end[1])), 3)
        return round(((500 * (distance_x + distance_y)) + ((750 - 2 * 500) * min(distance_x, distance_y))), 3)
