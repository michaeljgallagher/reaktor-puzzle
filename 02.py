from collections import Counter

with open('02.txt', 'r') as file:
    data = file.read()


count = Counter(data)
c = count.most_common()[0][0]
print(c)