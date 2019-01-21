from flask import Flask
from flask_cors import CORS

from .controller import points_of_interests_controller
from .controller import users_controller

def bindRoutes():
    app = Flask(__name__)
    CORS(app)

    print('binding Routes...')

    points_of_interests_controller.init(app)
    users_controller.init(app)

    app.run(host='0.0.0.0')
