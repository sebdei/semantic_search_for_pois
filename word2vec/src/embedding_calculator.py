import numpy as np

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
