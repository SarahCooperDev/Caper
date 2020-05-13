import os

currentPath = 'logs'
#currentPath = os.path.join('caper', 'heist', 'logs')

def printLog(text):
    filename = os.path.join(currentPath, 'log.txt')
    with open(filename, 'a') as f:
        f.write(str(text) + '\n')
    return None