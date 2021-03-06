from flask import Flask, render_template
from flask_cors import CORS

from .controller import points_of_interests_controller
from .controller import users_controller

def bind_index_render_route(app):
    @app.route('/')
    def index():
        return render_template("index.html")

def bind_routes():
    app = Flask(__name__, static_folder = "./dist", template_folder = "./dist")
    CORS(app)

    print('binding Routes...')

    bind_index_render_route(app)

    # API
    points_of_interests_controller.init(app)
    users_controller.init(app)

    app.run(host='0.0.0.0')
