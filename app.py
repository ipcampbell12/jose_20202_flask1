import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items,stores

#creates flask app
#allows you to run app
#makes endpoints available to client
app = Flask(__name__)



#flask endpoint/function definition/route
#1. RETURN STORES AND ALL ITEMS
@app.get('/store')
def get_stores():
    return {"stores":list(stores.values())}


#2. CREATE NEW STORE
@app.post('/store')
def create_store():
    store_data = request.get_json()

    #UUID
    store_id = uuid.uuid4().hex

    # ** will unpack values and store them in new dictionary
    store = {**store_data, "id":store_id}
    stores[store_id] = store
    return store, 201 
    #201 = data has been accepted 

#2. CREATE ITEM IN STORE
@app.post('/item')
def create_item():
    item_data = request.get_json()
    if item_data['store_id'] not in stores:
        abort(404,message="Store not found")
    
    #creates item id
    item_id =uuid.uuid4().hex
    #saves to dictionary 
    item = {**item_data, "id":item_id}
    #places in item dictionary
    items[item_id] = item 

    return item, 201


#3. RETURN SPECIFIC STORE
@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except:
        abort(404,message="Store not found")

#4. GET ALL ITEMS 
@app.get('/item')
def get_all_items():
    return {"items":list(items.values())}


#5. RETURN SPECIFIC ITEM
@app.get('/item/<string:item_id')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404,message="Item not found")
        
