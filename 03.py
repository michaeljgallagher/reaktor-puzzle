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
                valid.add(k)
    valid |= (start | finish)
    return valid, start, finish, walls


valid, start, finish, walls = find_points(strands)
# print(start)  # starting point is (2, 2)
# print(finish)  # length of valid finishes is 11

