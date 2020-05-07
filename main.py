import pygame
import time
import random
import board
import heapq as pq
import heapq
import argparse

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
gray = (128, 128, 128)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

snake_block = 10
snake_speed = 15 # don't know why we need this
game_speed = 64

dis_width = 600
dis_height = 400

# argument parser
parser = argparse.ArgumentParser()
parser.add_argument("map", help="Number of map to play")
args = parser.parse_args()

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
else:
    print("Map not found. Playing standard map")
    map = board.getEmptyMap(int(dis_width / snake_block), int(dis_height / snake_block))

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
random.seed(10)
rand = random.Random()

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def drawMap():
    for idxR, row in enumerate(map):
        for idxC, col in enumerate(row):
            if(col == 100):
                pygame.draw.rect(dis, black, [idxC * snake_block, idxR * snake_block, snake_block, snake_block])

def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, red, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def heuristics(st,end):
    distance = abs(st[0] - end[0]) + abs(st[1] - end[1]) # Manhattan
    return distance


def find_path(x1, y1, foodx, foody, snakeList):
    start = (x1, y1)
    end = (foodx, foody)
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristics(start, end)}

    oheap = []
    heapq.heappush(oheap, (fscore[start], start))

    map_copy = []
    for r in map:
        row = []
        for c in r:
            row.append(c)
        map_copy.append(row)

    for el in snakeList[:-1]:
        map_copy[int(el[1] / snake_block)][int(el[0] / snake_block)] = 80

    while oheap:

        current = heapq.heappop(oheap)[1]
        if current == end:
            break
        if map_copy[int(current[1] / snake_block)][int(current[0] / snake_block)] == 0:
            map_copy[int(current[1] / snake_block)][int(current[0] / snake_block)] = 50
            neighbours = []

            for new in [(0, -snake_block), (0, snake_block), (-snake_block, 0), (snake_block, 0)]:
                position = (current[0] + new[0], current[1] + new[1])

                if map_copy[int(position[1] / snake_block)][int(position[0] / snake_block)] == 0:
                    neighbours.append(position)

            for neigh in neighbours:
                cost = heuristics(current, neigh) + gscore[current] # cost of the path

                if cost < gscore.get(neigh, 0) or neigh not in gscore:
                    came_from[neigh] = current
                    gscore[neigh] = cost
                    fscore[neigh] = cost + heuristics(neigh, end)
                    pq.heappush(oheap, (fscore[neigh], neigh))

    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path = path[::-1]

    return path

def blind_path(x1,y1,x1_change, y1_change,snakeList):

    map_copy = []
    for r in map:
        row = []
        for c in r:
            row.append(c)
        map_copy.append(row)

    for el in snakeList[:-1]:
        map_copy[int(el[1] / snake_block)][int(el[0] / snake_block)] = 80
    counter = 4

    while counter:
        next = []
        next.append(x1 + x1_change)
        next.append(y1 + y1_change)

        if (map_copy[int(next[1] / snake_block)][int(next[0] / snake_block)] == 0):
            next2 = []
            next2.append(x1 + x1_change*2)
            next2.append(y1 + y1_change*2)
            if (map_copy[int(next2[1] / snake_block)][int(next2[0] / snake_block)] == 0):
                return [next]

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

    counter = 4

    while counter:
        next = []
        next.append(x1 + x1_change)
        next.append(y1 + y1_change)

        if (map_copy[int(next[1] / snake_block)][int(next[0] / snake_block)] == 0):
            return [next]
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


    return [[(x1 + x1_change), (y1 + y1_change)]] # go straight





def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    snake_List = []
    Length_of_snake = 1

    foodValid = False
    while not foodValid:
        foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
        if(map[int(foody / snake_block)][int(foodx / snake_block)] == 0):
            foodValid = True
    path = find_path(x1, y1, foodx, foody, snake_List)

    count = 0

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        if (count <= 0):
            count = 5
        for i in path:
            x1_change = i[0] - x1
            y1_change = i[1] - y1
            if ((abs(x1_change) > snake_block) or (abs(y1_change) > snake_block)):
                game_close = True
            x1 += x1_change
            y1 += y1_change

            if map[int(y1 / snake_block)][int(x1 / snake_block)] >= 50:
                game_close = True

            dis.fill(blue)
            pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
                    break

            if(game_close):
                break

            our_snake(snake_block, snake_List)
            drawMap()
            Your_score(Length_of_snake - 1)
            # pygame.time.Clock().tick(game_speed)
            pygame.display.update()

            count -= 1
            if (count <= 0):
                break
        path = find_path(x1, y1, foodx, foody, snake_List)

        if x1 == foodx and y1 == foody:
            foodValid = False
            while not foodValid:
                foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
                foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
                food = []
                food.append(foodx)
                food.append(foody)
                if (map[int(foody / snake_block)][int(foodx / snake_block)] == 0):
                    foodValid = True
                for block in snake_List:
                    if (food == block):
                        foodValid = False
                        break
            Length_of_snake += 1
            path = find_path(x1, y1, foodx, foody, snake_List)
        # if (len(path) == 0):
        #     game_close = True
        #     print("Path not found. Killing myself")
        #     continue

        if ((len(path) == 0) or (not(path[-1] == (foodx,foody)))):
            path = blind_path(x1, y1, x1_change, y1_change, snake_List)

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
