import re
import networkx as nx

with open('03.txt', 'r') as file:
    data = file.read()


def parse_raw(data):
    strands = {}
    m = re.findall(r'(\d*),(\d*)\s?(\D*)?\n', data)
    for x in m:
        pos = (int(x[0]), int(x[1]))
        moves = x[2].split(',')
        strands[pos] = moves
    strands[(25,95)] = 'R,U,R,D,R,U,R,U,U,L,L,L,U,U,U,U,L,L,D'.split(',')  # my regex missed this one
    return strands


strands = parse_raw(data)
print(len(strands))