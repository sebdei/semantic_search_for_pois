from collections import defaultdict
from surprise import KNNBaseline
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise import Reader, Dataset
from surprise import SVD
from surprise.model_selection import KFold
import pandas as pd
import numpy as np
import os

from src.service.persistency import pandas_persistence_service as pps
from src.service.persistency import persistence_service as ps
from src.service.persistency.data_model import *

RATING = 'rating'

def eval(user_id):

    # Step 1: Define variables
    ratings = pps.get_all_ratings_as_df() # read ratings from database
    ratings[RATING] = None
    ratings.loc[ratings[LIKED] == True, RATING] = 1
    ratings.loc[ratings[LIKED] == False, RATING] = 0

    reader = Reader(rating_scale=(0.0, 1.0))

    all_items = ratings.poi_id.unique() # find all items
    user_rmse = pd.DataFrame(columns=['est', 'true']) # define resulting dataframe for storing the probabilites

    # Step 2: Iterating over all items and leave out the current iteration's item (x) for training
    for x in np.nditer(all_items):

        # Step 2a: Define test dataset -> rating of currentUser and current (leaved out) item
        testset = ratings[(ratings.user_id == user_id)]
        testset = testset[(testset.poi_id == x)]

        # Step 2b: If user has given no rating for this item, the prediction cannot be compared to something true => thus skip
        if testset.rating.size == 0:
            continue

        # Step 2c: Define train dataset -> leave out the current item x
        trainset = ratings[~ratings.isin(testset).all(1)]
        trainset = Dataset.load_from_df(trainset[[USER_ID, POI_ID, RATING]], reader)
        trainset = trainset.build_full_trainset()

        # Step 2d: Apply algorithm by training and predicting of the item x that was leaved out
        algo = KNNBaseline(k=50, sim_options={'name': 'pearson_baseline', 'user_based': True})
        algo.fit(trainset)

        pred = algo.predict(user_id, np.asscalar(x), r_ui=4, verbose=False) # execute the calculation

        # Step 2e: Store estimate and true value into output dataframe
        user_rmse.loc[len(user_rmse)] = [pred.est, np.asscalar(testset.rating)]

    # Step 3: Calculate the RMSE over all leave out estimatieons
    confidence = np.mean((user_rmse.est - user_rmse.true)**2)

    return confidence


def init_collaborative_filtering():

    # Step 1: Read data from database
    ratings = pps.get_all_ratings_as_df()
    ratings[RATING] = None
    ratings.loc[ratings[LIKED] == True, RATING] = 1
    ratings.loc[ratings[LIKED] == False, RATING] = 0

    # Step 2: Transform to training set
    reader = Reader(rating_scale=(0.0, 1.0))
    data = Dataset.load_from_df(ratings[[USER_ID, POI_ID, RATING]], reader)
    trainset = data.build_full_trainset()

    # Step 3: Apply training of collaborative filtering (CF) algorithm
    algo = KNNBaseline(k=50, sim_options={'name': 'pearson_baseline', 'user_based': True})
    algo.fit(trainset)

    return algo, ratings


def get_recommendations_for_user(user_id):

    # Step 1: Train recommender algorithm
    algo, ratings = init_collaborative_filtering()

    # Step 2: Get list all items
    # a) Collect items which this user has rated
    rated_items = ratings[(ratings.user_id == user_id)].loc[:,POI_ID].values
    # b) Get relevent items for recommendations because only new locations (which are not rated yet)
    all_items = ratings.poi_id.unique()
    relevant_items = np.setdiff1d(all_items, rated_items)

    # Step 3: Get prediction for each item (for currentUser) + item information are enriched by relevant
    predictions_list = []
    for x in np.nditer(relevant_items):
        item_id = x.item(0) # save itemId in local variable
        poi_information = ps.get_points_of_interests_by_id(item_id) # request information from database
        pred = algo.predict(user_id, item_id, r_ui=4, verbose=False) # execute the calculation
        predictions_list.append({'id':item_id, 'pred_rating':pred.est, 'name':poi_information[1], 'long':poi_information[5], 'lat':poi_information[6], 'opening_hours':poi_information[7], 'is_building':poi_information[8]})

    predictions = pd.DataFrame(predictions_list)

    # Step 4: Sort locations their predicted ratings
    predictions = predictions.sort_values(by=['pred_rating'], ascending=[0])

    return predictions
