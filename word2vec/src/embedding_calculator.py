import numpy as np

def getInitSumVector(model):
    firstElementInModel = next(iter(model.values()))
    numberOfDimensions = len(firstElementInModel)

    return np.zeros(numberOfDimensions)

# assumes, that text is already cleaned
def calculateMeanVectorOfWordEmbeddingsForText(articleString, model):
    wordsArray = articleString.split()
    return calculateMeanVectorOfWordEmbeddingsForArray(wordsArray, model)

def calculateMeanVectorOfWordEmbeddingsForArray(wordsArray, model):
    sumVector = getInitSumVector(model)
    numberOfWords = len(wordsArray)
    wordsNotFoundInModel = []

    if (numberOfWords > 0 ):
        for word in wordsArray:
            lowerCaseWord = word.lower()

            try:
                wordVector = model[lowerCaseWord]
                sumVector = np.add(sumVector, wordVector)

            except KeyError:
                wordsNotFoundInModel.append(word)
                numberOfWords -= 1

        if (len(wordsNotFoundInModel) > 0):
            print("The following words were not found in model:")
            print(wordsNotFoundInModel)

        meanVector = sumVector / numberOfWords

        return meanVector
