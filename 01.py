with open('01.txt', 'r') as file:
    data = file.read()


def parse_raw(data):
    channels = []
    for line in data.split('\n'):
        channels.append([int(line[i:i+8], 2) for i in range(0, len(line), 8)])
    return channels


def eval_channel(channel):
    i = 0
    while channel[i] >= len(channel):
        i += 1
    while channel[i] < len(channel):
        i = channel[i]
    return chr(channel[i])


def solve(channels):
    res = [eval_channel(channel) for channel in channels]
    return ''.join(res)


channels = parse_raw(data)
print(solve(channels))  # left-ventricle
