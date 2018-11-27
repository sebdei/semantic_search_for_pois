from flask import Flask

app = Flask(__name__)

from .controller import classify_controller

def bindRoutes():
    print('binding Routes...')

    classify_controller.init(app)

    app.run()
