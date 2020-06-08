import cv2


# Function to generate the border of the map
def generate_border(map):
    height = len(map)
    width = len(map[0])

    # Checking the entire map
    for r in range(height):
        for c in range(width):
            if (c == 0) or (c == width - 1):  # the first and the last column is an obstacle
                map[r][c] = 100
                continue
            if (r == 0) or (r == height - 1):  # the first and the last row is an obstacle
                map[r][c] = 100
                continue
    return map


# Initializing the first map
def map(map_no, snake_block, width=600, height=400):

    map_np = cv2.imread("Map" + str(map_no) + ".png", cv2.IMREAD_GRAYSCALE)

    if map_np is None:
        print("Map not found. Playing standard map")
        map = get_empty_map(int(width / snake_block), int(height / snake_block))
        return map, width, height

    map = map_np.tolist()
    map = generate_border(map)
    height = len(map)
    width = len(map[0])

    # change of pixel value to the map environment
    for idx_r, r in enumerate(map):
        for idx_c, c in enumerate(r):
            if c == 255:  # white color -> movement space
                map[idx_r][idx_c] = 0
            else:  # black color -> obstacle
                map[idx_r][idx_c] = 100

    return map, width, height


# Initializing empty map
def empty_map(width=60, height=40):
    grid = []
    for r in range(height):
        row = []
        for c in range(width):
            if (c == 0) or (c == width - 1):  # the first and the last column is an obstacle
                row.append(100)
                continue
            if (r == 0) or (r == height - 1):  # the first and the last row is an obstacle
                row.append(100)
                continue
            row.append(0)
        grid.append(row)
    return grid


# Function that returns the empty map with specific dimensions
def get_empty_map(width=60, height=40):
    return empty_map(width=width, height=height)
