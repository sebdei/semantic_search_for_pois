from flask import request
from flask import jsonify

from src.service import classifier_service

import numpy as np

def init(app):

    @app.route("/classify", methods = ['POST'])
    def classify():
        body = request.json

        result = classifier_service.classify(body['query'])

        return result.to_json(orient='index')
