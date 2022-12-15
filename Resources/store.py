import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores


blp = Blueprint("Stores",__name__,description="Operations on stores")

#connects methods this endpoint
@blp.route("/store/<string:store_id>")
class Store(MethodView):

    def get(self, store_id):
        try:
            return stores[store_id]
        except:
            abort(404,message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message":"Store deleted"}
        except KeyError:
            abort(404,message="Store not found")

    
@blp.route("/store")
class StoresList(MethodView):

    def get(self):
        return {"stores":list(stores.values())}


    def post(self):
        store_data = request.get_json()

        #make sure name key is included
        if "name" not in store_data:
            abort(
                400,
                message="Bade request. Make sure 'name' is included"
            )
        
        #make sure the store name isn't already included
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, "That store already exists")

        #UUID
        store_id = uuid.uuid4().hex

        # ** will unpack values and store them in new dictionary
        # similar functioanlity to spread operator in python, expect for dictionaries instead of arrays
        store = {**store_data, "id":store_id}
        stores[store_id] = store
        return store, 201 
        #201 = data has been accepted 