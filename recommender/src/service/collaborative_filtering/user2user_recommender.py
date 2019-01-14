from collections import defaultdict
from surprise import KNNWithMeans
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise import Reader, Dataset
from surprise import SVD

import pandas as pd
import numpy as np

def initializeCollaborativeFiltering():

    # Step 1: Read data from excel <= To replace by database
    ratings = pd.read_excel('/Users/jensmechelhoff/POI-recommender-with-word-embeddings2/recommender/src/service/collaborative_filtering/testTable.xls')

    # Step 2: Transform to training set 
    reader = Reader(rating_scale=(0.0, 1.0))
    data = Dataset.load_from_df(ratings[['userID', 'itemID', 'rating']], reader)
    trainset = data.build_full_trainset()

    # Step 3: Apply training of collaborative filtering (CF) algorithm
    algo = KNNWithMeans(k=50, sim_options={'name': 'pearson_baseline', 'user_based': True})
    algo.fit(trainset)

    return algo, ratings


def getRecommendationsForUser(currentUserId):

    # Step 1: Train recommender algorithm
    algo, ratings = initializeCollaborativeFiltering()

    # Step 2: Get list all items
    allItems = ratings.itemID.unique()
    iid = 1  # rawn item id

    # Step 3: Get prediction for each item (for currentUser)
    predictions_list = []
    for x in np.nditer(allItems):
        pred = algo.predict(currentUserId, x.item(0), r_ui=4, verbose=False)
        predictions_list.append({"itemId":x, "pred_rating":pred.est})
        # should save the prediction somewhere - think about the format first!!!
    predictions = pd.DataFrame(predictions_list)
    print(predictions)

    # get a prediction for specific users and items.
    #pred = algo.predict(currentUserId, iid, r_ui=4, verbose=True)
    print("yoo")
