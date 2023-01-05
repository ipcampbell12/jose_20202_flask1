from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token
from schemas import UserSchema

#can only get access token by providing correct username and password
#whenever APi receives an access token, you know that the client logged in



#compares incoming password with one stored in database
from passlib.hash import pbkdf2_sha256

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from models import UserModel

blp = Blueprint("Users",__name__,description="Operations on users")


@blp.route("/login")
class UserLoginClass(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):

        #check to make sure user exists in database
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        #check password recieved from client against password from database
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):

            #user_id is stored in access token
            access_token = create_access_token(identity=user.id)

            return {"access_token":access_token}
            
        abort(401, message = "Invalide credentials")



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


@blp.route("/user")
class UserList(MethodView):
    @blp.response(200,UserSchema(many=True))
    def get(self):
        return UserModel.query.all()
       