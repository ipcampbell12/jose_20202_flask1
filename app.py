
from flask import Flask
from flask_smorest import Api

from db import db
import models 
#models need to have been imported so sqlalchemy can create our tables

#same as models.__init__
#can just say models because imports are in __init__

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

#creates flask app
#allows you to run app
#makes endpoints available to client

#application factory pattern
#can call function whenever you need, includign for when you want to write tests for your flask app
#call the function istead of running the file to create a new flask app
def create_app():
    app = Flask(__name__)

    #configuration variables
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config['API_VERSION'] = "v1"
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI'] = ""


    api = Api(app)

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app


#DATABSE
#all database providers use connection string that contain information that allow the client to connect to the database (flask app is client)



