import random
import heapq as pq
import heapq

###### Random seed - comment this line to randomize food
# random.seed(10)
######


def check_neighbors(x1_change, y1_change, snake_block):
    if (x1_change > 0) and (y1_change == 0):
        x1_change = 0
        y1_change = snake_block
    elif (x1_change == 0) and (y1_change > 0):
        x1_change = -snake_block
        y1_change = 0
    elif (x1_change < 0) and (y1_change == 0):
        x1_change = 0
        y1_change = -snake_block
    elif (x1_change == 0) and (y1_change < 0):
        x1_change = snake_block
        y1_change = 0

    return x1_change, y1_change


def generate_food(width, height, map, snake_block, snake_list=[]):
    foodValid = False
    while not foodValid:
        food_x = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
        food_y = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
        if map[int(food_y / snake_block)][int(food_x / snake_block)] == 0:  # Prevent getting food on the obstacle
            if [food_x, food_y] in snake_list:
                foodValid = False  # Prevent getting food on  snake body
                continue

            return food_x, food_y


def copy_map(map):
    map_copy = []
    for r in map:
        row = []
        for c in r:
            row.append(c)
        map_copy.append(row)

    return map_copy


# Calculating the heuristics of the distance
def heuristics(st, end):
    # distance = ((st[0] - end[0])**2 + (st[1] - end[1])**2)**(0.5)  # Euclidean
    distance = abs(st[0] - end[0]) + abs(st[1] - end[1])  # Manhattan
    return distance


def find_path_a_star(map, start, end, snake_block, snake_list):
    came_from = {}

    g_score = {start: 0}
    f_score = {start: heuristics(start, end)}

    oheap = []

    # Add a starting vertex to the vertex set to visit
    heapq.heappush(oheap, (f_score[start], start))

    # Create the copy of map
    map_copy = copy_map(map)

    # Get and mark the actual position of snake on the map
    for el in snake_list[:-1]:
        map_copy[int(el[1] / snake_block)][int(el[0] / snake_block)] = 80

    current = None
    while oheap:  # Until the set of vertices to visit is empty

        current = heapq.heappop(oheap)[1]  # Take the vertex from the set whose f_score is the smallest

        # Check if this vertex is the end vertex
        if current == end:
            # if so end the algorithm and display the path
            break

        # Check if the current vertex is a free space
        if map_copy[int(current[1] / snake_block)][int(current[0] / snake_block)] == 0:
            # Mark this vertex as visited
            map_copy[int(current[1] / snake_block)][int(current[0] / snake_block)] = 50
            neighbors = []

            # Get neighbors of the current vertex
            for new in [(0, -snake_block), (0, snake_block), (-snake_block, 0), (snake_block, 0)]:
                position = (current[0] + new[0], current[1] + new[1])

                # Check if the neighbor is a free space (allowed)
                if map_copy[int(position[1] / snake_block)][int(position[0] / snake_block)] == 0:
                    neighbors.append(position)

            # For each of its neighbors, check the path length from the start to that neighbor
            for neigh in neighbors:
                cost = heuristics(current, neigh) + g_score[current]  # cost of the path

                if cost < g_score.get(neigh, 0) or neigh not in g_score:
                    came_from[neigh] = current  # Set the current considered vertex as the parent of this neighbor
                    g_score[neigh] = cost
                    f_score[neigh] = cost + heuristics(neigh, end)  # Set the current distance as the shortest one
                    pq.heappush(oheap, (f_score[neigh], neigh))  # Add to the vertex set to visit this neighbor

    temp_path = []  # our path
    # Going through the visited points and recreate the path from the end to the start
    while current in came_from:
        temp_path.append(current)
        current = came_from[current]  # Get the parent of the current point
    # Reversing the path (we want the start to be the first point of the path)
    return temp_path[::-1]
