from db import db

#sqlalchemy turns table rows into python objects

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=False, nullable=False)
    price = db.Column(db.Float(precision=2),unique=False, nullable=False)
    store_id = db.Column(db.Intger, unique=False, nullable=False)