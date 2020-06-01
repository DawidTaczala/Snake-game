import pygame
import random
import board
import heapq as pq
import heapq
import argparse
from threading import Thread

# Initializes all of the imported Pygame modules
pygame.init()

# Initializing the colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
gray = (128, 128, 128)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Resolution of snake and map (how many pixels equal to one game block)
snake_block = 10
# snake_speed = 15
game_speed = 512 # the speed of game

# The dimensions of the map (pixels)
dis_width = 600
dis_height = 400

#### Global variables to define the initial values
# Position of snake
x1 = None
y1 = None
# Position of food
foodx = None
foody = None
# List of snake elements
snake_List = None
# Flags for path searching thread
search_for_path = False
global_finish = False
# Found path
path = []
###########

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument("map", help="Number of map to play")
args = parser.parse_args()

# Choosing the map to play
if str(args.map).lower() == "1":
    map, width, height = board.Map1()
    dis_width = width * snake_block
    dis_height = height * snake_block
elif str(args.map).lower() == "2":
    map, width, height = board.Map2()
    dis_width = width * snake_block
    dis_height = height * snake_block
elif str(args.map).lower() == "3":
    map, width, height = board.Map3()
    dis_width = width * snake_block
    dis_height = height * snake_block
elif str(args.map).lower() == "4":
    map, width, height = board.Map4()
    dis_width = width * snake_block
    dis_height = height * snake_block
else:
    print("Map not found. Playing standard map")
    # Load default map
    map = board.getEmptyMap(int(dis_width / snake_block), int(dis_height / snake_block))

#Create a surface
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game') # name of the screen

clock = pygame.time.Clock() # Time measurement
###### Random seed - comment this line to randomize food
# random.seed(10)
######
rand = random.Random()

# Create a Pygame font
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Function that draws a map
def drawMap():
    for idxR, row in enumerate(map):
        for idxC, col in enumerate(row):
            if(col == 100): # when there is an obstacle, draw a rectangle
                pygame.draw.rect(dis, black, [idxC * snake_block, idxR * snake_block, snake_block, snake_block])

# Show the result
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

# Draw snake as set of rectangles (squares) based on its elements
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, red, [x[0], x[1], snake_block, snake_block])

# Create the message on the screen with Pygame font
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# Caluclating the heuristics of the distance
def heuristics(st,end):
    # distance = ((st[0] - end[0])**2 + (st[1] - end[1])**2)**(0.5)  # Euclidean
    distance = abs(st[0] - end[0]) + abs(st[1] - end[1]) # Manhattan
    return distance

# Find the global path (thread)
def find_path():
    # Use global variables
    global path
    global search_for_path
    global x1
    global y1
    global foodx
    global foody
    global snake_List
    global global_finish

    # Run this thread forever
    while True:
        if(not search_for_path): # global path starts searching when it gets the flag search_for_path
            continue

        # Initialize supporting data structures
        start = (x1, y1)
        end = (foodx, foody)
        came_from = {}

        gscore = {start: 0}
        fscore = {start: heuristics(start, end)}

        oheap = []

        # Add a starting vertex to the vertex set to visit
        heapq.heappush(oheap, (fscore[start], start))

        # Create the copy of map
        map_copy = []
        for r in map:
            row = []
            for c in r:
                row.append(c)
            map_copy.append(row)

        # Get and mark the actual position of snake on the map
        for el in snake_List[:-1]:
            map_copy[int(el[1] / snake_block)][int(el[0] / snake_block)] = 80

        while oheap: # Until the set of vertices to visit is empty

            current = heapq.heappop(oheap)[1] # Take the vertex from the set whose fscore is the smallest

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
                    cost = heuristics(current, neigh) + gscore[current] # cost of the path

                    if cost < gscore.get(neigh, 0) or neigh not in gscore:
                        came_from[neigh] = current # Set the current considered vertex as the parent of this neighbor
                        gscore[neigh] = cost
                        fscore[neigh] = cost + heuristics(neigh, end) # Set the current distance as the shortest one
                        pq.heappush(oheap, (fscore[neigh], neigh)) # Add to the vertex set to visit this neighbor

        temp_path = [] # our path
        # Going through the visited points and recreate the path from the end to the start
        while current in came_from:
            temp_path.append(current)
            current = came_from[current] # Get the parent of the current point
        temp_path = temp_path[::-1] # reversing the path (we want the start to be the first point of the path)
        path = temp_path.copy()
        search_for_path = False # stop searching for the path
        global_finish = True # path found

# Find connection from current location to global path
def find_local_path(endx, endy):
    # Use global variables
    global path
    global search_for_path
    global x1
    global y1
    global snake_List

    # Initialize supporting data structures
    start = (x1, y1)
    end = (endx, endy)
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristics(start, end)}

    oheap = []
    # Add a starting vertex to the vertex set to visit
    heapq.heappush(oheap, (fscore[start], start))

    # Create the copy of map
    map_copy = []
    for r in map:
        row = []
        for c in r:
            row.append(c)
        map_copy.append(row)

    # Get the actual position of snake on the map
    for el in snake_List[:-1]:
        map_copy[int(el[1] / snake_block)][int(el[0] / snake_block)] = 80

    while oheap: # Until the set of vertices to visit is empty

        current = heapq.heappop(oheap)[1] # Take the vertex from the set whose fscore is the smallest

        # Check if this vertex is the end vertex
        if current == end:
            # if so end the algorithm and display the path
            break

        # Check if the current vertex is a free space
        if map_copy[int(current[1] / snake_block)][int(current[0] / snake_block)] == 0:
            # Mark this vertex as visited
            map_copy[int(current[1] / snake_block)][int(current[0] / snake_block)] = 50
            neighbors = []

            # Get the neighbors of the current vertex
            for new in [(0, -snake_block), (0, snake_block), (-snake_block, 0), (snake_block, 0)]:
                position = (current[0] + new[0], current[1] + new[1])

                # Check if the neighbor is a free space
                if map_copy[int(position[1] / snake_block)][int(position[0] / snake_block)] == 0:
                    neighbors.append(position)

            # For each of its neighbors, check that the path length from the start to that neighbor
            for neigh in neighbors:
                cost = heuristics(current, neigh) + gscore[current] # cost of the path

                if cost < gscore.get(neigh, 0) or neigh not in gscore:
                    came_from[neigh] = current # Set the currently considered vertex as the parent of this neighbor
                    gscore[neigh] = cost
                    fscore[neigh] = cost + heuristics(neigh, end) # Set the current distance as the shortest one
                    pq.heappush(oheap, (fscore[neigh], neigh)) # Add to the vertex set to visit this neighbor

    temp_path = [] # our path
    # Going through the visited points and recreate the path from the end to the start
    while current in came_from:
        temp_path.append(current)
        current = came_from[current] #Get the parent of the current point
    temp_path = temp_path[::-1] # reversing the path (we want the start to be the first point of the path)

    return temp_path

# Function that defines snake behaviour, when there is no global path found to the food
def blind_path(x1,y1,x1_change, y1_change,snakeList):

    # Create the copy of map
    map_copy = []
    for r in map:
        row = []
        for c in r:
            row.append(c)
        map_copy.append(row)

    # Get the actual position of snake on the map
    for el in snakeList[:-1]:
        map_copy[int(el[1] / snake_block)][int(el[0] / snake_block)] = 80

    # Checking two steps forward from the actual position of snake

    counter = 4 # Defines the four trials to find the path (each for one direction)

    while counter: # until snake tries 4 times to find the path
        next = []
        # Get the next position
        next.append(x1 + x1_change)
        next.append(y1 + y1_change)

        # Check if the next postion is an allowed space
        if (map_copy[int(next[1] / snake_block)][int(next[0] / snake_block)] == 0):
            next2 = []
            # Check two steps forward
            next2.append(x1 + x1_change*2)
            next2.append(y1 + y1_change*2)

            # Check if that position is allowed
            if (map_copy[int(next2[1] / snake_block)][int(next2[0] / snake_block)] == 0):
                # return next move
                return [next]

            # Check the four directions for two steps forward
            if ((x1_change > 0) and (y1_change == 0)):
                x1_change = 0
                y1_change = snake_block
            elif ((x1_change == 0) and (y1_change > 0)):
                x1_change = -snake_block
                y1_change = 0
            elif ((x1_change < 0) and (y1_change == 0)):
                x1_change = 0
                y1_change = -snake_block
            elif ((x1_change == 0) and (y1_change < 0)):
                x1_change = snake_block
                y1_change = 0

        # Check the four directions for the next position
        else:
            if ((x1_change > 0) and (y1_change == 0)):
                x1_change = 0
                y1_change = snake_block
            elif ((x1_change == 0) and (y1_change > 0)):
                x1_change = -snake_block
                y1_change = 0
            elif ((x1_change < 0) and (y1_change == 0)):
                x1_change = 0
                y1_change = -snake_block
            elif ((x1_change == 0) and (y1_change < 0)):
                x1_change = snake_block
                y1_change = 0

        counter -= 1

    # Checking oneforward position from the actual one of snake

    counter = 4 # Defines the four trials to find the path

    while counter: # until snake tries 4 times to find the path
        next = []
        # Get the next position
        next.append(x1 + x1_change)
        next.append(y1 + y1_change)

        # Check if the next position is allowed
        if (map_copy[int(next[1] / snake_block)][int(next[0] / snake_block)] == 0):
            # return next move
            return [next]
        else:
            # Check the four directions for the next position
            if ((x1_change > 0) and (y1_change == 0)):
                x1_change = 0
                y1_change = snake_block
            elif ((x1_change == 0) and (y1_change > 0)):
                x1_change = -snake_block
                y1_change = 0
            elif ((x1_change < 0) and (y1_change == 0)):
                x1_change = 0
                y1_change = -snake_block
            elif ((x1_change == 0) and (y1_change < 0)):
                x1_change = snake_block
                y1_change = 0

        counter -= 1


    return [[(x1 + x1_change), (y1 + y1_change)]] # go straight

# Connect local and global paths
def evaluate_new_path():
    # Use global variables
    global path
    global snake_List
    global x1, y1

    # Create the copy of map
    map_copy = []
    for r in map:
        row = []
        for c in r:
            row.append(c)
        map_copy.append(row)

    # Get the actual position of snake on the map
    for el in snake_List[:-1]:
        map_copy[int(el[1] / snake_block)][int(el[0] / snake_block)] = 80

    # Find the shortest distance from the local to the found global path
    shortest_dist = 99999999999
    shortest_idx = 0
    # For every element in global path
    for idx, el in enumerate(path):
        # Check if position is valid
        if (map_copy[int(el[1] / snake_block)][int(el[0] / snake_block)] == 0):
            # Calculate distance
            distance = ((el[0] - x1)**2 + (el[1] - y1)**2)**0.5  # Euclidean
            if(distance < shortest_dist):
                shortest_dist = distance
                shortest_idx = idx

    # Remove beginning sequence of the path to the connection vertex
    for i in range(shortest_idx):
        path.pop(0)
    for i in range(len(path)):
        if(not len(path)):
            break
        # Find the closest vertex in the graph to path
        elem = [path[0][0], path[0][1]]
        # Find
        short_path = find_local_path(elem[0], elem[1])
        if(len(short_path)):
            while(short_path[-1] == path[0]): # Until there will be no repeated vertex in short path, we can connect those paths
                short_path.pop(-1)
                if (not len(short_path)):
                    break

        short_copy = short_path.copy()
        for el in short_copy:
            if el in path:
                short_path.pop(0) # Delete repeated vertex from short path
            else:
                break

        short_path.extend(path) # Merge paths
        if(len(short_path)):
            # Delete the head of snake from the path
            if((short_path[0][0] == x1) and (short_path[0][1] == y1)):
                short_path.pop(0)
        path = short_path.copy()
        return

    return

# Main game loop
def gameLoop():
    # Initialize values
    astar = Thread(target=find_path, daemon=True)
    # Use global variables
    global search_for_path
    global global_finish
    global x1
    global y1
    global foodx
    global foody
    global snake_List
    global path

    # Do not search for global path now
    search_for_path = False
    astar.start() # Start the thread

    # Set initial direction of move
    x1_change = snake_block
    y1_change = 0

    # Variables defininf end of the game
    game_over = False
    game_close = False

    # Set starting position of snake
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Initialize snake elements and his length
    snake_List = []
    Length_of_snake = 1

    # Get the random position of the food
    foodValid = False
    while not foodValid:
        foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
        if(map[int(foody / snake_block)][int(foodx / snake_block)] == 0): # Prevent getting food on the obstacle
            foodValid = True

    # Now look for global path to found food
    search_for_path = True # Start searching global path

    # Variable initialization - every defined number of moves try to find new, possibly shorter, global path
    count = 0

    # While game is not over
    while not game_over:

        # If game is over (snake died), show final score and message
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press Q-Quit", red) # Shows the meassage on the screen
            Your_score(Length_of_snake - 1) # The obtained score
            pygame.display.update() # Updates the screen
            for event in pygame.event.get(): # All the actions that take place on the screen
                # Press q to quit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False

        # Every defined number of moves try to find new, possibly shorter, global path
        if (count <= 0):
            count = 5
            search_for_path = True
        # If global path exists
        if(global_finish):
            if(len(path)):
                if(path[-1] == (foodx,foody)):
                    evaluate_new_path() # Start connecting the global path with current position
            global_finish = False

        path_copy = path.copy()

        # for every position in path
        for i in path:
            # if new global path found then restart this loop
            if (global_finish):
                break
            # Delete first (current) position in path sequence
            if(len(path_copy)):
                path_copy.pop(0)

            # Evaluate temporary current moving direction
            x1_change_temp = i[0] - x1
            y1_change_temp = i[1] - y1
            # If next step is the same point, where the snake currently is (snake must move all the time)
            if ((i[0] == x1) and (i[1] == y1)):
                continue
            # If the next step is higher than the snake body
            if ((abs(x1_change_temp) > snake_block) or (abs(y1_change_temp) > snake_block)):
                continue
            # Evaluate the current moving direction
            x1_change = i[0] - x1
            y1_change = i[1] - y1
            x1 += x1_change
            y1 += y1_change

            # If snake hit an obstacle
            if map[int(y1 / snake_block)][int(x1 / snake_block)] >= 50:
                game_close = True

            # Draw map
            dis.fill(blue)
            # Draw the food
            pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
            # Update snake elements
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            # Add the new coordinates to the snake body
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            # Check if the snake is not eating his head
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
                    break

            # if game is over, exit this loop
            if(game_close):
                break

            our_snake(snake_block, snake_List) # Draw snake
            drawMap() # Draws the map
            Your_score(Length_of_snake - 1) # Shows the score
            pygame.time.Clock().tick(game_speed) #  Helps tracking time
            pygame.display.update() # Updates the screen

            # Decrement the count variable to search new global path
            count -= 1
            if (count <= 0):
                if(not global_finish):
                    path = path_copy.copy()
                break

        # If snake is consuming food
        if x1 == foodx and y1 == foody:
            foodValid = False

            #  Get new random position of the food
            while not foodValid:
                foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
                foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
                food = []
                food.append(foodx)
                food.append(foody)
                # Prevent spawning food on the obstacle
                if (map[int(foody / snake_block)][int(foodx / snake_block)] == 0):
                    foodValid = True
                for block in snake_List:
                    if (food == block): # Prevent getting food on  snake body
                        foodValid = False
                        break
            # New length of the snake
            Length_of_snake += 1
            # Find new global path
            search_for_path = True
            path = []
            continue

        # If there is no path or the food is not found -> play on time (local planner)
        if ((len(path) == 0) or (not(path[-1] == (foodx,foody)))):
            path = blind_path(x1, y1, x1_change, y1_change, snake_List)


    # Initialize and uninitialize everything at the start and the end of the code
    pygame.quit()
    quit()

gameLoop()
