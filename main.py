import pygame
import board
# import heapq as pq
# import heapq
import argparse
from threading import Thread
from utils import check_neighbors, generate_food, copy_map, find_path_a_star

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
# Define the speed of game
game_speed = 512

# The dimensions of the map (pixels)
dis_width = 600
dis_height = 400

########### Global variables defines initial values
# Position of snake
x1 = 0
y1 = 0
# Position of food
food_x = None
food_y = None
# List of snake elements
snake_list = list([])
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
map, width, height = board.map(str(args.map).lower(), snake_block)

# Create a surface
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')  # Name of the screen

clock = pygame.time.Clock()  # Time measurement

# Create a Pygame font
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


# Function that draws a map
def draw_map():
    for idxR, row in enumerate(map):
        for idxC, col in enumerate(row):
            if col == 100:  # When there is an obstacle, draw a rectangle
                pygame.draw.rect(dis, black, [idxC * snake_block, idxR * snake_block, snake_block, snake_block])


# Show the result
def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


# Draw snake as set of rectangles (squares) based on its elements
def our_snake():
    for x in snake_list:
        pygame.draw.rect(dis, red, [x[0], x[1], snake_block, snake_block])


# Create the message on the screen with Pygame font
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


# # Calculating the heuristics of the distance
# def heuristics(st, end):
#     # distance = ((st[0] - end[0])**2 + (st[1] - end[1])**2)**(0.5)  # Euclidean
#     distance = abs(st[0] - end[0]) + abs(st[1] - end[1])  # Manhattan
#     return distance


# Find the global path (thread)
def find_path():
    # Use global variables
    global path
    global search_for_path
    global x1
    global y1
    global food_x
    global food_y
    global snake_list
    global global_finish

    # Run this thread forever
    while True:
        if not search_for_path:  # global path starts searching when it gets the flag search_for_path
            continue

        # Initialize supporting data structures
        start = (x1, y1)
        end = (food_x, food_y)

        path = find_path_a_star(map, start, end, snake_block, snake_list)

        search_for_path = False  # Stop searching for the path
        global_finish = True  # Path found


# Find connection from current location to global path
def find_local_path(end_x, end_y):
    # Use global variables
    global path
    global search_for_path
    global x1
    global y1
    global snake_list

    # Initialize supporting data structures
    start = (x1, y1)
    end = (end_x, end_y)

    return find_path_a_star(map, start, end, snake_block, snake_list)


# Function that defines snake behaviour, when there is no global path found to the food
def blind_path(x1_change, y1_change):
    global x1
    global y1
    # Create the copy of map
    map_copy = copy_map(map)

    # Get the actual position of snake on the map
    for el in snake_list[:-1]:
        map_copy[int(el[1] / snake_block)][int(el[0] / snake_block)] = 80

    # Checking two steps forward from the actual position of snake
    counter = 4  # Defines the four trials to find the path (each for one direction)

    while counter:  # until snake tries 4 times to find the path
        next = list([])
        # Get the next position
        next.append(x1 + x1_change)
        next.append(y1 + y1_change)

        # Check if the next position is an allowed space
        if map_copy[int(next[1] / snake_block)][int(next[0] / snake_block)] == 0:
            next2 = list([])
            # Check two steps forward
            next2.append(x1 + x1_change*2)
            next2.append(y1 + y1_change*2)

            # Check if that position is allowed
            if map_copy[int(next2[1] / snake_block)][int(next2[0] / snake_block)] == 0:
                # return next move
                return [next]

            # Check the four directions for two steps forward
            x1_change, y1_change = check_neighbors(x1_change, y1_change, snake_block)

        # Check the four directions for the next position
        else:
            x1_change, y1_change = check_neighbors(x1_change, y1_change, snake_block)

        counter -= 1

    # Checking one forward position from the actual one of snake
    counter = 4  # Defines the four trials to find the path

    while counter:  # until snake tries 4 times to find the path
        next = list([])
        # Get the next position
        next.append(x1 + x1_change)
        next.append(y1 + y1_change)

        # Check if the next position is allowed
        if map_copy[int(next[1] / snake_block)][int(next[0] / snake_block)] == 0:
            # return next move
            return [next]
        else:
            # Check the four directions for the next position
            x1_change, y1_change = check_neighbors(x1_change, y1_change, snake_block)

        counter -= 1

    return [[(x1 + x1_change), (y1 + y1_change)]]  # go straight


# Connect local and global paths
def evaluate_new_path():
    # Use global variables
    global path
    global snake_list
    global x1, y1

    # Create the copy of map
    map_copy = copy_map(map)

    # Get the actual position of snake on the map
    for el in snake_list[:-1]:
        map_copy[int(el[1] / snake_block)][int(el[0] / snake_block)] = 80

    # Find the shortest distance from the local to the found global path
    shortest_dist = 1e10
    shortest_idx = 0
    # For every element in global path
    for idx, el in enumerate(path):
        # Check if position is valid
        if map_copy[int(el[1] / snake_block)][int(el[0] / snake_block)] == 0:
            # Calculate distance
            distance = ((el[0] - x1)**2 + (el[1] - y1)**2)**0.5  # Euclidean
            if distance < shortest_dist:
                shortest_dist = distance
                shortest_idx = idx

    # Remove beginning sequence of the path to the connection vertex
    path = path[slice(shortest_idx, len(path))]

    for i in range(len(path)):
        if not len(path):
            break
        # Find the closest vertex in the graph to path
        elem = [path[0][0], path[0][1]]
        # Find
        short_path = find_local_path(elem[0], elem[1])
        if len(short_path):
            # Until there will be no repeated vertex in short path, we can connect those paths
            while short_path[-1] == path[0]:
                short_path.pop(-1)
                if not len(short_path):
                    break

        short_copy = short_path.copy()
        for el in short_copy:
            if el in path:
                short_path.pop(0)  # Delete repeated vertex from short path
            else:
                break

        short_path.extend(path)  # Merge paths
        if len(short_path):
            # Delete the head of snake from the path
            if (short_path[0][0] == x1) and (short_path[0][1] == y1):
                short_path.pop(0)
        path = short_path.copy()
        return
    return


# Main game loop
def game_loop():
    # Initialize values
    a_star = Thread(target=find_path, daemon=True)
    # Use global variables
    global search_for_path
    global global_finish
    global x1
    global y1
    global food_x
    global food_y
    global snake_list
    global path

    # Do not search for global path now
    search_for_path = False
    a_star.start()  # Start the thread

    # Set initial direction of move
    x1_change = snake_block
    y1_change = 0

    # Variables defining end of the game
    game_over = False
    game_close = False

    # Set starting position of snake
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Initialize snake elements and his length
    snake_list = []
    Length_of_snake = 1

    # Get the random position of the food
    food_x, food_y = generate_food(dis_width, dis_height, map, snake_block, snake_list)

    # Now look for global path to found food
    search_for_path = True  # Start searching global path

    # Variable initialization - every defined number of moves try to find new, possibly shorter, global path
    count = 0

    # While game is not over
    while not game_over:
        # If game is over (snake died), show final score and message
        while game_close:
            dis.fill(blue)
            message("You Lost! Press Q-Quit", red)  # Shows the meassage on the screen
            your_score(Length_of_snake - 1)  # The obtained score
            pygame.display.update()  # Updates the screen
            for event in pygame.event.get():  # All the actions that take place on the screen
                # Press q to quit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False

        # Every defined number of moves try to find new, possibly shorter, global path
        if count <= 0:
            count = 5
            search_for_path = True
        # If global path exists
        if global_finish:
            if len(path):
                if path[-1] == (food_x, food_y):
                    evaluate_new_path()  # Start connecting the global path with current position
            global_finish = False

        path_copy = path.copy()

        # for every position in path
        for i in path:
            # if new global path found then restart this loop
            if global_finish:
                break
            # Delete first (current) position in path sequence
            if len(path_copy):
                path_copy.pop(0)

            # Evaluate temporary current moving direction
            x1_change_temp = i[0] - x1
            y1_change_temp = i[1] - y1
            # If next step is the same point, where the snake currently is (snake must move all the time)
            if (i[0] == x1) and (i[1] == y1):
                continue
            # If the next step is higher than the snake body
            if (abs(x1_change_temp) > snake_block) or (abs(y1_change_temp) > snake_block):
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
            pygame.draw.rect(dis, green, [food_x, food_y, snake_block, snake_block])
            # Update snake elements
            snake_head = list([])
            snake_head.append(x1)
            snake_head.append(y1)
            # Add the new coordinates to the snake body
            snake_list.append(snake_head)
            if len(snake_list) > Length_of_snake:
                del snake_list[0]

            # Check if the snake is not eating his head
            for x in snake_list[:-1]:
                if x == snake_head:
                    game_close = True
                    break

            # if game is over, exit this loop
            if game_close:
                break

            our_snake()  # Draw snake
            draw_map()  # Draws the map
            your_score(Length_of_snake - 1)  # Shows the score
            pygame.time.Clock().tick(game_speed)  # Helps tracking time
            pygame.display.update()  # Updates the screen

            # Decrement the count variable to search new global path
            count -= 1
            if count <= 0:
                if not global_finish:
                    path = path_copy.copy()
                break

        # If snake is consuming food
        if x1 == food_x and y1 == food_y:
            # Get new random position of the food
            food_x, food_y = generate_food(dis_width, dis_height, map, snake_block, snake_list)

            # New length of the snake
            Length_of_snake += 1
            # Find new global path
            search_for_path = True
            path = []
            continue

        # If there is no path or the food is not found -> play on time (local planner)
        if (len(path) == 0) or (not(path[-1] == (food_x, food_y))):
            path = blind_path(x1_change, y1_change)

    # Initialize and uninitialize everything at the start and the end of the code
    pygame.quit()
    quit()


if __name__ == '__main__':
    game_loop()