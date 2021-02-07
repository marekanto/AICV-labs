import numpy as np
import a_star_algorithm as alg


# S - starting pos
# G - goal pos
# '#' - obstacle
# ' ' - can move here

maze1 = np.array([['#', '#', '#', ' ', ' ', ' ', '#', '#'],
                   ['#', ' ', ' ', ' ', '#', ' ', '#', '#'],
                   ['#', ' ', '#', '#', '#', ' ', '#', '#'],
                   [' ', ' ', ' ', ' ', '#', 'G', '#', '#'],
                   [' ', '#', '#', '#', '#', ' ', '#', '#'],
                   [' ', '#', '#', ' ', ' ', ' ', '#', '#'],
                   [' ', '#', '#', ' ', '#', '#', '#', '#'],
                   ['S', ' ', ' ', ' ', '#', '#', '#', '#']])

maze2 =       np.array([['#', '#', '#', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', '#', '#'],
                        ['#', ' ', ' ', ' ', '#', '#', ' ', '#', '#', '#', ' ', '#', '#'],
                        ['#', ' ', '#', '#', '#', '#', ' ', ' ', ' ', ' ', ' ', '#', '#'],
                        [' ', ' ', ' ', ' ', '#', '#', '#', '#', '#', '#', 'G', ' ', ' '],
                        [' ', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', ' '],
                        [' ', '#', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', ' ', ' '],
                        [' ', '#', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#', ' ', '#'],
                        ['S', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#', ' ', ' ', ' ', '#']])


def bfs(width, height, start_pos, end_pos, obstacle):
    front = [(start_pos[0][0], start_pos[1][0])]
    visit = []
    prev = [(start_pos[0][0], start_pos[1][0])]
    while len(front) > 0:
        (x_c, y_c) = front[0]

        if (x_c, y_c) == (end_pos[0][0], end_pos[1][0]):
            visit.append((x_c, y_c))
            del front
            break

        if (x_c, y_c) not in visit:

            if x_c + 1 < height and (x_c + 1, y_c) not in obstacle and (x_c + 1, y_c) not in visit:
                front.append((x_c + 1, y_c))
                prev.append((x_c, y_c))
            if x_c - 1 >= 0 and (x_c-1, y_c) not in obstacle and (x_c - 1, y_c) not in visit:
                front.append((x_c - 1, y_c))
                prev.append((x_c, y_c))
            if y_c + 1 < width and (x_c, y_c + 1) not in obstacle and (x_c, y_c + 1) not in visit:
                front.append((x_c, y_c + 1))
                prev.append((x_c, y_c))
            if y_c - 1 >= 0 and (x_c, y_c-1) not in obstacle and (x_c, y_c - 1) not in visit:
                front.append((x_c, y_c - 1))
                prev.append((x_c, y_c))
            visit.append((x_c, y_c))

        del front[0]
    del prev[len(prev) - 1]
    return visit, prev


# calculation BFS
end = np.where(maze1 == "G")
start = np.where(maze1 == "S")
walls = []
cords_bfs = np.where(maze1 == "#")
for index in range(len(cords_bfs[0])):
    walls.append((cords_bfs[0][index], cords_bfs[1][index]))
height, width = maze1.shape
child, parent = bfs(height, width, start, end, walls)
solution = {}
for idx in range(len(child)):
    solution[child[idx]] = parent[idx]

x_s, y_s = start[0][0], start[1][0]
x, y = end[0][0], end[1][0]
path_bfs = [(x, y)]
while (x, y) != (x_s, y_s):
    (x, y) = solution[x, y]
    path_bfs.append((x, y))
del walls
# A-star calculations
a = alg.AStar()
cords_astar = np.where(maze2 == '#')
walls = []
for index in range(len(cords_astar[0])):
    walls.append((cords_astar[0][index], cords_astar[1][index]))
a.init_grid(8, 13, walls, (7, 0), (3, 10))
path = a.solve()
# Solution for First_maze
while len(path_bfs) > 0:
    i, j = path_bfs[0]
    maze1[i][j] = "x"
    del path_bfs[0]
print("solved first maze:")
print(maze1)
# Solution for Second maze
while len(path) > 0:
    x, y = path[0]
    maze2[x][y] = "x"
    del path[0]
print("solved second maze:")
print(maze2)
