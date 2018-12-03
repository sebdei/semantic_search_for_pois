import zipfile
import numpy as np
import os
from urllib.request import urlretrieve

GLOVE_MODEL_BASE_DIR = 'models'
GLOVE_MODEL_TXT_NAME = 'glove.6B.50d.txt'
GLOVE_MODEL_ZIP_NAME = 'glove.6B.zip'
GLOVE_MODEL_URL = 'http://nlp.stanford.edu/data/glove.6B.zip'

def assure_model_exists():
    if not os.path.exists(GLOVE_MODEL_BASE_DIR):
        os.makedirs(GLOVE_MODEL_BASE_DIR)

    if not (os.path.exists(os.path.join(GLOVE_MODEL_BASE_DIR, GLOVE_MODEL_TXT_NAME))):
        if (not os.path.exists(os.path.join(GLOVE_MODEL_BASE_DIR, GLOVE_MODEL_ZIP_NAME))):
            print('downloading GLOVE model (>800MB) ...')
            response = urlretrieve(GLOVE_MODEL_URL, os.path.join(GLOVE_MODEL_BASE_DIR, GLOVE_MODEL_ZIP_NAME))

        zip = zipfile.ZipFile(os.path.join(GLOVE_MODEL_BASE_DIR, GLOVE_MODEL_ZIP_NAME), 'r')
        zip.extract(GLOVE_MODEL_TXT_NAME, GLOVE_MODEL_BASE_DIR)

def provide_glove_model():
    assure_model_exists()

    print('providing word embedding model ...')

    file = open(os.path.join(GLOVE_MODEL_BASE_DIR, GLOVE_MODEL_TXT_NAME),'r')
    model = {}

    for line in file:
        split_line = line.split()
        word = split_line[0]
        model[word] = np.array([ float(val) for val in split_line[1:] ])

    print('model successfully loaded')

    return model
