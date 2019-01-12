from collections import defaultdict
from surprise import KNNWithMeans
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise import Reader, Dataset
from surprise import SVD

import pandas as pd

def userToUser2():
    ratings = pd.read_excel('recommender/src/service/collaborative_filtering/testTable.xls')

    # Creation of the dataframe. Column names are irrelevant.
    ratings_dict = {'itemID': list(ratings.item),
                    'userID': list(ratings.user),
                    'rating': list(ratings.rating)}
    df = pd.DataFrame(ratings_dict)
    reader = Reader(rating_scale=(0.0, 1.0))
    data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)
    trainset, testset = train_test_split(data, test_size=.15)

    algo = KNNWithMeans(k=50, sim_options={'name': 'pearson_baseline', 'user_based': True})
    algo.fit(trainset)

    # we can now query for specific predicions
    uid = 6  # raw user id
    iid = 1  # rawn item id

    # get a prediction for specific users and items.
    pred = algo.predict(uid, iid, r_ui=4, verbose=True)
    print("yoo")
