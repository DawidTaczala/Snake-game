import numpy as np
import cv2

def generateBorder(map):
    height = len(map)
    width = len(map[0])
    for r in range(height):
        # row = np.array([])
        # row = []
        for c in range(width):
            if ((c == 0) or (c == width - 1)):
                # row = np.append(row, [100])
                # row.append(100)
                map[r][c] = 100
                continue
            if ((r == 0) or (r == height - 1)):
                # row = np.append(row, [100])
                map[r][c] = 100
                continue
            # row = np.append(row, [0])
            # row.append(0)
        # grid = np.append(grid, row)
    #     grid.append(row)
    # grid[5][20] = 100
    return map


def Map1():
    map_np = cv2.imread("Map1.png", cv2.IMREAD_GRAYSCALE)
    map = map_np.tolist()
    map = generateBorder(map)
    height = len(map)
    width = len(map[0])

    for idx_r, r in enumerate(map):
        for idx_c, c in enumerate(r):
            if (c == 255):
                map[idx_r][idx_c] = 0
            elif (c == 0):
                map[idx_r][idx_c] = 100

    return map, width, height

def Map2():
    map_np = cv2.imread("Map2.png", cv2.IMREAD_GRAYSCALE)
    map = map_np.tolist()
    map = generateBorder(map)
    height = len(map)
    width = len(map[0])

    for idx_r, r in enumerate(map):
        for idx_c, c in enumerate(r):
            if (c == 255):
                map[idx_r][idx_c] = 0
            else:
                map[idx_r][idx_c] = 100

    return map, width, height

def Map3():
    map_np = cv2.imread("Map3.png", cv2.IMREAD_GRAYSCALE)
    map = map_np.tolist()
    map = generateBorder(map)
    height = len(map)
    width = len(map[0])

    for idx_r, r in enumerate(map):
        for idx_c, c in enumerate(r):
            if (c == 255):
                map[idx_r][idx_c] = 0
            else:
                map[idx_r][idx_c] = 100

    return map, width, height

def emptyMap(width = 60, height = 40):
    grid = []
    for r in range(height):
        row = []
        for c in range(width):
            if((c == 0) or (c == width - 1)):
                row.append(100)
                continue
            if((r == 0) or (r == height - 1)):
                row.append(100)
                continue
            row.append(0)
        grid.append(row)
    return grid

def getEmptyMap(width = 60, height = 40):
    return emptyMap(width=width, height=height)