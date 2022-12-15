import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items


blp = Blueprint("Items",__name__,description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get_item(item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404,message="Item not found")


    def delete_item(item_id):
        try:
            del items[item_id]
            return {"message":"Item deleted"}
        except KeyError:
            abort(404,message="Item not found")



    def update_item(item_id):

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
            