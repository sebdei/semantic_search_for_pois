import numpy as np

GLOVE_MODEL_DIR = 'models/glove.6B.50d.txt'


def load_model():
    model = {}
    print('loading word embedding model ...')

    file = open(GLOVE_MODEL_DIR,'r')

    for line in file:
        split_line = line.split()
        word = split_line[0]
        embedding = np.array([float(val) for val in split_line[1:]])
        model[word] = embedding

    print('model successfully loaded')

    return model
