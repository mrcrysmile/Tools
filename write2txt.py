import numpy as np

#
def writeFile(data, path, model=0, joiner='', ender=''):
    output = open(path, 'w', encoding='utf-8')
    if model == 0:
        for strings in data:
            output.writelines(joiner.join(strings))
            output.writelines(ender)
    # full write
    elif model == 1:
        output.writelines(data)
