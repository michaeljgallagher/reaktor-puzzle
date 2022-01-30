import re
import networkx as nx

with open("03.txt", "r") as file:
    data = file.read()

DIRS = {
    "U": (0, -1),
    "D": (0, 1),
    "R": (1, 0),
    "L": (-1, 0),
}


def parse_raw(data):
    strands = {}
    m = re.findall(r"(\d*),(\d*)\s?(\D*)?\n", data)
    for x in m:
        pos = (int(x[0]), int(x[1]))
        moves = x[2].split(",")
        strands[pos] = moves
    strands[(25, 95)] = "R,U,R,D,R,U,R,U,U,L,L,L,U,U,U,U,L,L,D".split(
        ","
    )  # my regex missed this one
    strands[(104, 15)] = []  # make this empty list rather than ['']
    return strands


strands = parse_raw(data)


def find_points(strands):
    valid, start, finish, walls = set(), set(), set(), set()
    for k, v in strands.items():
        valid.add(k)
        cur = k
        for d in v:
            if d == "F":
                finish.add(cur)
            elif d == "S":
                start.add(cur)
            elif d == "X":
                walls.add(cur)
            else:  # d in DIRS
                x, y = cur
                dx, dy = DIRS[d]
                cur = (x + dx, y + dy)
                valid.add(cur)
    return valid, start, finish, walls


valid, start, finish, walls = find_points(strands)
# print(start)  # starting point is (2, 2)
# print(finish)  # length of valid finishes is 11
# all_points = valid | start | finish | walls
# print(max(all_points, key=lambda x: x[1]))  # (127, 69), (22, 127) max points


def display_graph(valid, start, finish, walls, path=None):
    grid = [["." for _ in range(128)] for _ in range(128)]
    for x, y in valid:
        grid[y][x] = "#"
    if path:
        for x, y in path:
            grid[y][x] = chr(9608)
    for x, y in start:
        grid[y][x] = "S"
    for x, y in finish:
        grid[y][x] = "F"
    for x, y in walls:
        grid[y][x] = "X"
    for line in grid:
        print("".join(line))


# display_graph(valid, start, finish, walls)


def build_graph(valid, start, finish):
    valid |= start | finish
    G = nx.Graph()
    for x, y in valid:
        for dx, dy in DIRS.values():
            if (x + dx, y + dy) in valid:
                G.add_edge((x + dx, y + dy), (x, y))
    return G


G = build_graph(valid, start, finish)


def find_shortest_path(G, finish):
    res = []
    for f in finish:
        try:
            cur = nx.shortest_path(G, (2, 2), f)
        except:
            continue
        res = cur if not res else min(res, cur, key=len)
    return res


path = find_shortest_path(G, finish)
# display_graph(valid, start, finish, walls, path=path)


def convert_to_steps(path):
    res = []
    for i, step in enumerate(path):
        if i == 0:
            continue
        x, y = step
        dx, dy = path[i - 1]
        res.append((x - dx, y - dy))
    return res


path = convert_to_steps(path)
REVERSE = {v: k for k, v in DIRS.items()}
print("".join(REVERSE[step] for step in path))

"""
RRRDDDDRRRUURURURRRRRRRRRRRRRDRRRRRRRRRRRRRRRRDRRDRRRRRRDRRDDRR
DRDDDDDLDDDDDLDDLLDLDDDLLLLLLLLLDDLLDLLLDDDLDLDDLLLLLLLLLLLDLLL
LLLLLLLLLLLLLLLDDDDDDDDDDDDDDDDDDDRDDDDRDDDDDRRUUUUURUURRURRRRR
DRDDDDRRRRRUUURRDDDRRRRRRRRRRRRRRRRDRRRRRRRURRDRRRRRRRRDDLDDRRR
RDDDLLLLLDDLLUULLDDLLLUULLDDLLLLLUULLDDLLLLDDDDDDDDDDDDRRRRRRRR
DDDDDLDLLLDDLLLLLLLULLLLULLDDDDLDDLLDLLULUURUUULLLUULLLLDDDDDDR
DDDRDDDDRDRDDDRDRDDLDDDDDDDLLLLLLLLLLLDLLLLDDDDDRRRRRRRDRRRRRDD
RRRRRRRRRRDDRDRRRRURRRRRRRRRRRRRRRRRURRRRRRRRRRRRURRRRRRRRDDRRR
RURRRDRRRRRRUUURRRRDDDRRUUUUUUUUURRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
RRRRURRUUUUUUUUUUUUUULUULUUUULUUUULLDLLLLLLLLLULLUULLLLDLLLLLLL
LLUURUUUULUURRRRRRRURUURRRDDDRRUUUUUUUUULLLDDDDLLLLDLDLLDLLLLLL
DDRDDLLDDLLULUULULLDLDDDLLULUULUULLLLLDLLDLLUUUUUURRRUUUULLULLU
LLUURRRUURRRRRURUUUUUUUUUUUUUUURURRRURRUURURRDDRDDDDDRDDDDDDDDD
DRRRRRRRURRRRRDRRRRRURURUURUURRRRUURRRURURRRRRRUUUUUUUURUURUUUU
UUUUUULLLULLLULULLLLLDLLLULLLLLLLLLLLLUUUUULLLLLLLLDDDLLLDDLLLL
LLLLLLLLLLLLLLLLUUUUUULUUUUUUUUURUURRUUURRURRRRRRRRRRUUUUUURURR
RRRRRRRRRRRDDDDDDDRRDRRDDDLLLLLLLLDDRRRDRRDDRRRURRRRRUUURUURRRR
"""
