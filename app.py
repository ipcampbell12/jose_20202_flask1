import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items,stores

#creates flask app
#allows you to run app
#makes endpoints available to client
app = Flask(__name__)

#will be easier to document if we use abort
#flask endpoint/function definition/route

#1. GET ALL STORE DATA
@app.get('/store')
def get_stores():
    return {"stores":list(stores.values())}



#DELETE STORE
@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message":"Store deleted"}
    except KeyError:
        abort(404,message="Store not found")


#GET STORE
@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except:
        abort(404,message="Store not found")

#2. CREATE STORE
@app.post('/store')
def create_store():
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


###############################################################################################
#ITEMS


#GET ALL ITEMS 
@app.get('/item')
def get_all_items():
    return {"items":list(items.values())}


#GET ITEM
@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404,message="Item not found")


#2. CREATE ITEM 
@app.post('/item')
def create_item():
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

    #make sure the store is present
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found")
    

    item_id =uuid.uuid4().hex
  
    item = {**item_data, "id":item_id}
  
    items[item_id] = item 

    return item, 201


#DELETE ITEM
@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message":"Item deleted"}
    except KeyError:
        abort(404,message="Item not found")


#UPDATE ITEM
@app.put('/item/<string:item_id>')
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
        
