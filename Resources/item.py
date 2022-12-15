import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items


blp = Blueprint("Items",__name__,description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self,item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404,message="Item not found")


    def delete(item_id):
        try:
            del items[item_id]
            return {"message":"Item deleted"}
        except KeyError:
            abort(404,message="Item not found")



    def put(self,item_id):

        item_data = request.get_json()

        #check to make sure it has expecte data
        if "price" not in item_data or "name" not in item_data:
            abort(400, message="Bad request. Need to cinluded 'price' and 'name' ")

        try:
            item=items[item_id]
            #in place modification of item, values in item_data replace values of item
            item |= item_data

            return item
        except:
            abort(404,message="Item not found" )


@blp.route("/item")
class ItemList(MethodView):

    def get(self):
        return {"items":list(items.values())}


    def post(self):
        item_data = request.get_json()

        #make sure all the necessary keys are included
        if (
            "price" not in item_data
            or "store_id" not in item_data
            or "name" not in item_data
        ):
            abort(
                400,
                message="Bad request. Ensure 'price', 'store_id' and 'name' are included."
            )
        
        #make sure you don't include same item twice
        for item in items.values():
            if (item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"] ):
                abort(400, message="Item already exists")

        item_id =uuid.uuid4().hex
    
        item = {**item_data, "id":item_id}
    
        items[item_id] = item 

        return item, 201
