from .model_provider import loadModel
from .embedding_calculator import calculateMeanVectorOfWordEmbeddingsForText

def run():
    articleString = "hello how are you"

    model = loadModel()
    meanVectorOfArticle = calculateMeanVectorOfWordEmbeddingsForText(articleString, model)

    print(meanVectorOfArticle)
