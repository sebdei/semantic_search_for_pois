from flask import request

def init(app):

    @app.route("/classify", methods = ['POST'])
    def classify():
        input = request.json
        
        input['userinput']
        return "Hello World!"
