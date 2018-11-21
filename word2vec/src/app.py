from .model_provider import load_model
from .embedding_calculator import calculate_mean_vector_of_word_embeddings_for_text

from flask import Flask
import numpy as np

def run():
    app = Flask(__name__)

    model = load_model()

    @app.route("/")
    def home():

        article_string = 'The Berlin Wall (German: Berliner Mauer, pronounced [b\u025b\u0281\u02c8li\u02d0n\u0250 \u02c8ma\u028a\u032f\u0250] (listen)) was a guarded concrete barrier that physically and ideologically divided Berlin from 1961 to 1989. Constructed by the German Democratic Republic (GDR, East Germany), starting on 13 August 1961, the Wall cut off (by land) West Berlin from virtually all of surrounding East Germany and East Berlin until government officials opened it in November 1989. Its demolition officially began on 13 June 1990 and finished in 1992. The barrier included guard towers placed along large concrete walls, accompanied by a wide area (later known as the \"death strip\") that contained anti-vehicle trenches, \"fakir beds\" and other defenses.'

        mean_vector_of_article = calculate_mean_vector_of_word_embeddings_for_text(article_string, model)
        return np.array2string(mean_vector_of_article)

    app.run()
