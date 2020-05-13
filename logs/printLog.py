import os

def printLog(text):
    filename = os.path.join('logs', 'log.txt')
    with open(filename, 'a') as f:
        f.write(str(text) + '\n')
    return None