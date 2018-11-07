import numpy as np

GLOVE_MODEL_DIR = 'models/glove.6B.50d.txt'


def loadModel():
    model = {}
    print('loading word embedding model ...')

    file = open(GLOVE_MODEL_DIR,'r')

    for line in file:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding

    print('model successfully loaded')

    return model
