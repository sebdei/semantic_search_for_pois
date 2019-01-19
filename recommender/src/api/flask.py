from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

from .controller import points_of_interests

def bindRoutes():
    print('binding Routes...')

    points_of_interests.init(app)

    CORS(app)

    app.run(host='0.0.0.0')
