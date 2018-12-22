from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

from .controller import classify_controller

def bindRoutes():
    print('binding Routes...')

    classify_controller.init(app)

    CORS(app)

    app.run()
