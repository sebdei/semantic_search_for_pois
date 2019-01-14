from collections import defaultdict
from surprise import KNNBaseline
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise import Reader, Dataset
from surprise import SVD
from ..persistency import persistence_service

import pandas as pd
import numpy as np
import os

def initializeCollaborativeFiltering():

    # Step 1: Read data from excel <= To replace by database
    #ratings = pd.read_excel('/Users/jensmechelhoff/POI-recommender-with-word-embeddings2/recommender/src/service/collaborative_filtering/testTable.xls')
    ratings = pd.read_excel('recommender/src/service/collaborative_filtering/testTable.xls')

    # Step 2: Transform to training set 
    reader = Reader(rating_scale=(0.0, 1.0))
    data = Dataset.load_from_df(ratings[['userID', 'itemID', 'rating']], reader)
    trainset = data.build_full_trainset()

    # Step 3: Apply training of collaborative filtering (CF) algorithm
    algo = KNNBaseline(k=50, sim_options={'name': 'pearson_baseline', 'user_based': True})
    algo.fit(trainset)

    return algo, ratings


def getRecommendationsForUser(currentUserId):

    # Step 1: Train recommender algorithm
    algo, ratings = initializeCollaborativeFiltering()

    # Step 2: Get list all items
    # a) Collect items which this user has rated
    userRatedItems = ratings[(ratings.userID == currentUserId)].loc[:,'itemID'].values
    # b) Get relevent items for recommendations because only new locations (which are not rated yet)
    allItems = ratings.itemID.unique()
    relevantItems = np.setdiff1d(allItems, userRatedItems)

    # Step 3: Get prediction for each item (for currentUser) + item information are enriched by relevant 
    predictions_list = []
    for x in np.nditer(relevantItems):
        itemID = x.item(0) # save itemId in local variable
        poiInformation = persistence_service.get_points_of_interests_by_id(itemID) # request information from database
        pred = algo.predict(currentUserId, itemID, r_ui=4, verbose=False) # execute the calculation
        predictions_list.append({"itemId":itemID, "pred_rating":pred.est, "name":poiInformation[1], "long":poiInformation[5], "lat":poiInformation[6], "opening_hours":poiInformation[7], "is_building":poiInformation[8]})
        
    predictions = pd.DataFrame(predictions_list)

    # Step 4: Sort locations their predicted ratings
    predictions = predictions.sort_values(by=['pred_rating'], ascending=[0])

    print(predictions)

    print("yoo")
