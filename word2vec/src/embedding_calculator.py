import numpy as np

def getInitSumVector(model):
    firstElementInModel = next(iter(model.values()))
    numberOfDimensions = len(firstElementInModel)

    return np.zeros(numberOfDimensions)

# assumes, that text is already cleaned
def calculateMeanOfWordEmbeddingsForText(articleString, model):
    wordsArray = articleString.split()
    return calculateMeanOfWordEmbeddingsForArray(wordsArray, model)

def calculateMeanOfWordEmbeddingsForArray(wordsArray, model):
    sumVector = getInitSumVector(model)
    numberOfWords = len(wordsArray)

    if (numberOfWords > 0 ):
        for word in wordsArray:
            lowerCaseWord = word.lower()
            wordVector = model[lowerCaseWord]
            sumVector = np.add(sumVector, wordVector)

        meanVector = sumVector / numberOfWords

        return meanVector
