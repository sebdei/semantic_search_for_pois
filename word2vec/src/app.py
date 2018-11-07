from .model_provider import loadModel
from .embedding_calculator import calculateMeanVectorOfWordEmbeddingsForText

def run():
    articleString = 'suck it down dude'

    model = loadModel()
    meanVectorOfArticle = calculateMeanVectorOfWordEmbeddingsForText(articleString, model)

    print(meanVectorOfArticle)
