from .model_provider import loadModel
from .embedding_calculator import calculateMeanOfWordEmbeddingsForText

def run():
    articleString = "suck it down dude"

    model = loadModel()
    meanVectorOfArticle = calculateMeanOfWordEmbeddingsForText(articleString, model)

    print(meanVectorOfArticle)
