from marshmallow import Schema, fields

#dump_only = True basically means this filed is read only 
#only used for returning data (e.g. sending data back to the client)
#id field won't be used for validation


#validate the types
class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name=fields.Str(required=True)
    price = fields.Float(required=True)
    

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name=fields.Str(required=True)

# for put request
# fields are NOT required because the user may not choose to update either or both fields
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

#use marshmallow schemas to make sure data has been correclty typed

#need to use inheritance for nested fields

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(),dump_only=True)

# 
""" {
    name: 'asdf',
    store: {
        id: 1,
        name: 'store 1'
    }
}

// StoreSchema
class StoreSchema:
    id: fields.Int,
    name: fields.Str """

name = fields.Str()
store = fields.Nested(StoreSchema())


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only=True)