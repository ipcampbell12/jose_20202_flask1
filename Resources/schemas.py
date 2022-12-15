from marshmallow import Schema, fields

#dump_only = True basically means this filed is read only 
#only used for returning data
#id field won't be used for validation


#validate the types
class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name=fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

# for put request
# fields are NOT required because the user may not choose to update either or both fields
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name=fields.Str(required=True)


#use marshmallow schemas to make sure data has been correclty typed