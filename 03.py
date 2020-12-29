import re
import networkx as nx

with open('03.txt', 'r') as file:
    data = file.read()

DIRS = {
    'U': (0, -1),
    'D': (0, 1),
    'R': (1, 0),
    'L': (-1, 0),
}


def parse_raw(data):
    strands = {}
    m = re.findall(r'(\d*),(\d*)\s?(\D*)?\n', data)
    for x in m:
        pos = (int(x[0]), int(x[1]))
        moves = x[2].split(',')
        strands[pos] = moves
    strands[(25,95)] = 'R,U,R,D,R,U,R,U,U,L,L,L,U,U,U,U,L,L,D'.split(',')  # my regex missed this one
    strands[(104,15)] = []  # make this empty list rather than ['']
    return strands


strands = parse_raw(data)


def find_points(strands):
    valid, start, finish, walls = set(), set(), set(), set()
    for k, v in strands.items():
        valid.add(k)
        cur = k
        for d in v:
            if d == 'F':
                finish.add(cur)
            elif d == 'S':
                start.add(cur)
            elif d == 'X':
                walls.add(cur)
            else:  # d in DIRS
                x, y = cur
                dx, dy = DIRS[d]
                cur = (x+dx, y+dy)
                valid.add(cur)
    return valid, start, finish, walls


valid, start, finish, walls = find_points(strands)
# print(start)  # starting point is (2, 2)
# print(finish)  # length of valid finishes is 11
# all_points = valid | start | finish | walls
# print(max(all_points, key=lambda x: x[1]))  # (127, 69), (22, 127) max points

def display_graph(valid, start, finish, walls):
    grid = [['.' for _ in range(128)] for _ in range(128)]
    for x, y in valid:
        grid[x][y] = '#'
    for x, y in start:
        grid[x][y] = 'S'
    for x, y in finish:
        grid[x][y] = 'F'
    for x, y in walls:
        grid[x][y] = 'X'
    for line in grid:
        print(''.join(line))


display_graph(valid, start, finish, walls)


def build_graph(valid, start, finish):
    valid |= (start | finish)
    G = nx.Graph()
    for x, y in valid:
        for dx, dy in DIRS.values():
            if (x+dx, y+dy) in valid:
                G.add_edge((x+dx, y+dy), (x, y))
    return G


G = build_graph(valid, start, finish)
