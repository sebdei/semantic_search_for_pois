from flask import request
from flask import jsonify
import json

from src.service import classifier_service

def init(app):

    @app.route("/classify", methods = ['POST'])
    def classify():
        body = request.json

        similarArticle = classifier_service.classify(body['query'])

        return similarArticle.reset_index().to_json(orient='records')
