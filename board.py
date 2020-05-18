import numpy as np
import cv2

# Function to generate the border of the map
def generateBorder(map):
    height = len(map)
    width = len(map[0])

    #checking the entire map
    for r in range(height):
        for c in range(width):
            if ((c == 0) or (c == width - 1)): #the first and the last column is an obstacle
                map[r][c] = 100
                continue
            if ((r == 0) or (r == height - 1)):#the first and the last row is an obstacle
                map[r][c] = 100
                continue
    return map

# Initializing the first map
def Map1():
    map_np = cv2.imread("Map1.png", cv2.IMREAD_GRAYSCALE)
    map = map_np.tolist()
    map = generateBorder(map)
    height = len(map)
    width = len(map[0])

    # change of pixel value to the map environment
    for idx_r, r in enumerate(map):
        for idx_c, c in enumerate(r):
            if (c == 255): # white color -> movement space
                map[idx_r][idx_c] = 0
            else:  # black color -> obstacle
                map[idx_r][idx_c] = 100

    return map, width, height

# Initializing the second map
def Map2():
    map_np = cv2.imread("Map2.png", cv2.IMREAD_GRAYSCALE)
    map = map_np.tolist()
    map = generateBorder(map)
    height = len(map)
    width = len(map[0])

    # change of pixel value to the map environment
    for idx_r, r in enumerate(map):
        for idx_c, c in enumerate(r):
            if (c == 255):  # white color -> movement space
                map[idx_r][idx_c] = 0
            else: # black color -> obstacle
                map[idx_r][idx_c] = 100

    return map, width, height

# Initializing the third map
def Map3():
    map_np = cv2.imread("Map3.png", cv2.IMREAD_GRAYSCALE)
    map = map_np.tolist()
    map = generateBorder(map)
    height = len(map)
    width = len(map[0])

    # change of pixel value to the map environment
    for idx_r, r in enumerate(map):
        for idx_c, c in enumerate(r):
            if (c == 255): # white color -> movement space
                map[idx_r][idx_c] = 0
            else: # black color -> obstacle
                map[idx_r][idx_c] = 100

    return map, width, height

# Initializing empty map
def emptyMap(width = 60, height = 40):
    grid = []
    for r in range(height):
        row = []
        for c in range(width):
            if((c == 0) or (c == width - 1)): #the first and the last column is an obstacle
                row.append(100)
                continue
            if((r == 0) or (r == height - 1)): #the first and the last row is an obstacle
                row.append(100)
                continue
            row.append(0)
        grid.append(row)
    return grid

#Function that returns the empty map with specific dimensions
def getEmptyMap(width = 60, height = 40):
    return emptyMap(width=width, height=height)