from db import db

#sqlalchemy turns table rows into python objects
#each item is associated with one store, but each item could have many items associated with it

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=False, nullable=False)
    price = db.Column(db.Float(precision=2),unique=False, nullable=False)
    store_id = db.Column(db.Intger,db.ForeignKey('stores.id'), unique=False, nullable=False)

    #store variable will get populated with StoreModel object, whose id matches the Foreign key
    store = db.relationship("StoreModel",back_populates="items")

    #I think the "store" is like a hypothetical column that gets added to this table