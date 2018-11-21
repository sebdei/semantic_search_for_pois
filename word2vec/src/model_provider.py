import zipfile
import numpy as np
import os
import urllib

GLOVE_MODEL_BASE_DIR = 'models'
GLOVE_MODEL_TXT_NAME = 'glove.6B.50d.txt'
GLOVE_MODEL_ZIP_NAME = 'glove.6B.zip'
GLOVE_MODEL_URL = 'http://nlp.stanford.edu/data/glove.6B.zip'

def assure_model_exists():
    if (not os.path.exists(os.path.join(GLOVE_MODEL_BASE_DIR, GLOVE_MODEL_ZIP_NAME))
    and not os.path.exists(os.path.join(GLOVE_MODEL_BASE_DIR, GLOVE_MODEL_TXT_NAME))):
        print('downloading GLOVE model (>800MB) ...')
        response = urllib.urlretrieve(GLOVE_MODEL_URL, os.path.join(GLOVE_MODEL_BASE_DIR, GLOVE_MODEL_ZIP_NAME))

    if (os.path.exists(os.path.join(GLOVE_MODEL_BASE_DIR, GLOVE_MODEL_ZIP_NAME))
    and not os.path.exists(os.path.join(GLOVE_MODEL_BASE_DIR, GLOVE_MODEL_TXT_NAME))):
        zip = zipfile.ZipFile(os.path.join(GLOVE_MODEL_BASE_DIR, GLOVE_MODEL_ZIP_NAME), 'r')
        zip.extract(GLOVE_MODEL_TXT_NAME, GLOVE_MODEL_BASE_DIR)

def load_model():
    assure_model_exists()

    model = {}
    print('loading word embedding model ...')

    file = open(os.path.join(GLOVE_MODEL_BASE_DIR, GLOVE_MODEL_TXT_NAME),'r')

    for line in file:
        split_line = line.split()
        word = split_line[0]
        embedding = np.array([float(val) for val in split_line[1:]])
        model[word] = embedding

    print('model successfully loaded')

    return model
