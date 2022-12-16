import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from db import items


blp = Blueprint("Items",__name__,description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
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

    #order of decorators matter
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self,item_data, item_id):

        #item_data = request.get_json()

        #check to make sure it has expecte data
        # if "price" not in item_data or "name" not in item_data:
        #     abort(400, message="Bad request. Need to cinluded 'price' and 'name' ")

        try:
            item=items[item_id]
            #in place modification of item, values in item_data replace values of item
            item |= item_data

            return item
        except:
            abort(404,message="Item not found" )


@blp.route("/item")
class ItemList(MethodView):

    #many = True turns dictionary into a list?
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return items.values()
        #list of items, not object
        #return {"items":list(items.values())}


    #2nd argument after self contains json data that has been validated by the schema
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        #NO LONGER NEEDED 
        #item_data = request.get_json()

        #make sure all the necessary keys are included
        #NO LONGER NEED IF STATEMENTS BECAUSE VALIDATION HANDLED BY SCHEMA
        # if (
        #     "price" not in item_data
        #     or "store_id" not in item_data
        #     or "name" not in item_data
        # ):
        #     abort(
        #         400,
        #         message="Bad request. Ensure 'price', 'store_id' and 'name' are included."
        #     )
        
        #check if item already exists
        for item in items.values():
            if (item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"] ):
                abort(400, message="Item already exists")

        item_id =uuid.uuid4().hex
    
        item = {**item_data, "id":item_id}
    
        items[item_id] = item 

        return item
