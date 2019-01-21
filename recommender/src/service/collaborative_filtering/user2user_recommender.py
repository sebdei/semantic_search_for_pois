from collections import defaultdict
from surprise import KNNBaseline
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise import Reader, Dataset
from surprise import SVD
from surprise.model_selection import KFold
from ..persistency import persistence_service as ps
from ..persistency import pandas_persistence_service as pps
from ..persistency.data_model import *

import pandas as pd
import numpy as np
import os

def eval(currentUserId):

    # Step 1: Define variables
    ratings = pps.get_all_ratings_as_df() # read ratings from database
    reader = Reader(rating_scale=(0.0, 1.0))

    allItems = ratings.poi_id.unique() # find all items
    rmseData_forUser = pd.DataFrame(columns=['est', 'true']) # define resulting dataframe for storing the probabilites

    # Step 2: Iterating over all items and leave out the current iteration's item (x) for training
    for x in np.nditer(allItems):

        # Step 2a: Define test dataset -> rating of currentUser and current (leaved out) item
        testset = ratings[(ratings.u_id == currentUserId)]
        testset = testset[(testset.poi_id == x)]

        # Step 2b: If user has given no rating for this item, the prediction cannot be compared to something true => thus skip
        if testset.rating.size == 0:
            continue

        # Step 2c: Define train dataset -> leave out the current item x
        trainset = ratings[~ratings.isin(testset).all(1)]
        trainset = Dataset.load_from_df(trainset[[U_ID, POI_ID, RATING]], reader)
        trainset = trainset.build_full_trainset()

        # Step 2d: Apply algorithm by training and predicting of the item x that was leaved out
        algo = KNNBaseline(k=50, sim_options={'name': 'pearson_baseline', 'user_based': True})
        algo.fit(trainset)

        pred = algo.predict(currentUserId, np.asscalar(x), r_ui=4, verbose=False) # execute the calculation

        # Step 2e: Store estimate and true value into output dataframe
        rmseData_forUser.loc[len(rmseData_forUser)] = [pred.est, np.asscalar(testset.rating)]

    # Step 3: Calculate the RMSE over all leave out estimatieons
    confidence = np.mean((rmseData_forUser.est - rmseData_forUser.true)**2)

    return confidence


def initializeCollaborativeFiltering():

    # Step 1: Read data from excel <= To replace by database
    ratings = pps.get_all_ratings_as_df()

    # Step 2: Transform to training set 
    reader = Reader(rating_scale=(0.0, 1.0))
    data = Dataset.load_from_df(ratings[[U_ID, POI_ID, RATING]], reader)
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
    userRatedItems = ratings[(ratings.u_id == currentUserId)].loc[:,POI_ID].values
    # b) Get relevent items for recommendations because only new locations (which are not rated yet)
    allItems = ratings.poi_id.unique()
    relevantItems = np.setdiff1d(allItems, userRatedItems)

    # Step 3: Get prediction for each item (for currentUser) + item information are enriched by relevant 
    predictions_list = []
    for x in np.nditer(relevantItems):
        itemID = x.item(0) # save itemId in local variable
        poiInformation = ps.get_points_of_interests_by_id(itemID) # request information from database
        pred = algo.predict(currentUserId, itemID, r_ui=4, verbose=False) # execute the calculation
        predictions_list.append({"poi_id":itemID, "pred_rating":pred.est, "name":poiInformation[1], "long":poiInformation[5], "lat":poiInformation[6], "opening_hours":poiInformation[7], "is_building":poiInformation[8]})

    predictions = pd.DataFrame(predictions_list)

    # Step 4: Sort locations their predicted ratings
    predictions = predictions.sort_values(by=['pred_rating'], ascending=[0])

    return predictions
