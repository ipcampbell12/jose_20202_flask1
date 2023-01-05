from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserSchema

#compares incoming password with one stored in database
from passlib.hash import pbkdf2_sha256

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import UserModel

blp = Blueprint("Users",__name__,description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):

        #check if username already exists (or you could check for integrity error)
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists")
        
        user = UserModel(
            username= user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()

        return {"message":"User created successfully."}, 201

    

@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200,UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete (self, user_id):
        user = UserModel.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return {"message":f"User {user.username} was deleted"},200