from flask import request

from src.service import classifier_service

import numpy as np

def init(app):

    @app.route("/classify", methods = ['POST'])
    def classify():
        body = request.json

        arrayOfDicts = classifier_service.classify(body['userinput'])

        # work in progress
        result = ''
        for dict in arrayOfDicts:
            str(dict)
            result += str(dict)

        return result
