from .model_provider import load_model
from .word_embedding_service import calculate_mean_vector_of_word_embeddings_for_text
from .similarity_service import determine_similar_items_with_cosine_similarity

import numpy as np

articles = [
    {
        'id': 1,
        'word2vec_vector': [ 0.22687541,  0.14207963,  0.04068134, -0.1960955,   0.08015795,  0.14385143,
         -0.46472762, -0.07975457, -0.27986677, -0.35660814,  0.04075904, -0.31710287,
         -0.35912295, -0.01576023,  0.14928315,  0.10652329,  0.0416041,  -0.08716148,
         -0.52387694,  0.01466572,  0.28573009, -0.07747771,  0.03651196, -0.08177578,
         -0.19050083, -1.32774361, -0.11496927,  0.1369291,   0.00910556, -0.07364546,
          2.83385254, -0.22015066, -0.11836334, -0.33067918, -0.08596471,  0.03430548,
          0.20401384,  0.13020622, -0.06854444,  0.05951666, -0.15154164, -0.05515559,
          0.15285274, -0.24563734, -0.12448038,  0.10502858, -0.24720076, -0.29486655,
         -0.12967974, -0.36756519]
    },
    {
        'id': 2,
        'word2vec_vector': [ 0.12337541,  0.12313207963,  0.04068134, -0.1960955,   0.08015795,  0.14385143,
         -0.46472762, -0.07975457, -0.27986677, -0.870814,  0.04075904, -0.31710287,
         -0.35912295, -0.01576023,  0.14928315,  0.10652329,  0.0416041,  -0.08716148,
         -0.512394,  0.01466572,  0.28573009, -0.07747771,  0.03651196, -0.08177578,
         -0.19050083, -1.392774361, -0.896927,  0.23459291,   0.00910556, -0.9864546,
          2.83385254, -0.22015066, -0.11836334, -0.33067918, -0.08596471,  0.78430548,
          0.20401384,  0.13020622, -0.06854444,  0.05951666, -0.15154164, -0.895559,
          0.8785274, -0.24563734, -0.12448038,  0.98502858, -0.9876, -0.29486655,
         -0.98967974, -0.36756519]
    },
    {
        'id': 3,
        'word2vec_vector': [ 0.12337541,  0.12313207963,  0.4068134, -0.1960955,   0.2015795,  0.85143,
         -0.46472762, -0.07975457, -0.27986677, -0.870814,  0.04075904, -0.31710287,
         -0.35912295, -0.01576023,  0.14928315,  0.10652329,  0.0416041,  -0.08716148,
         -0.512394,  0.01466572,  0.28573009, -0.07747771,  0.03651196, -0.08177578,
         -0.19050083, -1.392774361, -0.896927,  0.23459291,   0.00910556, -0.9864546,
          1.83385254, -0.22015066, -0.9836334, -0.33067918, -0.08596471,  0.78430548,
          0.20401384,  0.13020622, -0.06854444,  0.05951666, -0.15154164, -0.895559,
          0.8785274, -0.24563734, -0.12448038,  1.98502858, -0.9876, -0.29486655,
         -0.98967974, -0.36756519]
    }
]

def run():
    model = load_model()

    article_string = 'The Berlin Wall (German: Berliner Mauer, pronounced [b\u025b\u0281\u02c8li\u02d0n\u0250 \u02c8ma\u028a\u032f\u0250] (listen)) was a guarded concrete barrier that physically and ideologically divided Berlin from 1961 to 1989. Constructed by the German Democratic Republic (GDR, East Germany), starting on 13 August 1961, the Wall cut off (by land) West Berlin from virtually all of surrounding East Germany and East Berlin until government officials opened it in November 1989. Its demolition officially began on 13 June 1990 and finished in 1992. The barrier included guard towers placed along large concrete walls, accompanied by a wide area (later known as the \"death strip\") that contained anti-vehicle trenches, \"fakir beds\" and other defenses.'
    mean_vector_of_article = calculate_mean_vector_of_word_embeddings_for_text(article_string, model)

    article_similarity = determine_similar_items_with_cosine_similarity(mean_vector_of_article, articles)
    print(article_similarity)
