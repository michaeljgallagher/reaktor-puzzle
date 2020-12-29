from collections import Counter

with open('02.txt', 'r') as file:
    data = file.read()


cur = Counter(data).most_common()[0][0]  # P
res = []

while cur != ';':
    res.append(cur)
    count = Counter()
    for i, c in enumerate(data):
        if c == cur:
            count[data[i+1]] += 1
    cur = count.most_common()[0][0]

print(''.join(res))  # PArietalLobE
