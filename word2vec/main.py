import numpy as np

GLOVE_MODEL_DIR = "./models/glove.6B.50d.txt"


def loadGloveModel(filePath):
    model = {}
    print("loading word embedding model ...")

    file = open(filePath,'r')

    for line in file:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding

    print('model successfully loaded')

    return model

def getInitSumVector(model):
    firstElementInModel = next(iter(model.values()))
    numberOfDimensions = len(firstElementInModel)

    return np.zeros(numberOfDimensions)

# assumes, that text is already cleaned
def calculateMeanOfWordEmbeddingsForText(articleString, model):
    sumVector = getInitSumVector(model)

    wordsArray = articleString.split()
    numberOfWordsInArticle = len(wordsArray)

    if (numberOfWordsInArticle > 0 ):
        for word in wordsArray:
            lowerCaseWord = word.lower()
            wordVector = model[lowerCaseWord]
            sumVector = np.add(sumVector, wordVector)

        meanVector = sumVector / numberOfWordsInArticle

        return meanVector


model = loadGloveModel(GLOVE_MODEL_DIR)

articleString = ""

calculateMeanOfWordEmbeddingsForText(articleString, model)
