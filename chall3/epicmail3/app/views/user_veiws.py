from app.conn_database.database import DatabaseConnection
from flask.views import MethodView
from flask import request ,jsonify
from app.views.validations import Validations
from app.models.user_model import User


class SignupUser(MethodView):
  def post(self):
    data = request.get_json()
    contentType = request.content_type
 
    #validate posted data for create user
    validate = Validations()
    if validate.create_user_validation(contentType, data) is not True:
      return validate.create_user_validation(contentType, data)

    # we ceate an object user from our class User
    user = User(first_name=data["first_name"], last_name=data["last_name"], email=data["email"], password=data["password"] ,is_admin=data["is_admin"])
    
    # persist user in the database 
    user.save()
    return jsonify({
      "status":201,
      "message": "User created successfully",
      "data":User.check_user(data["email"])[0]
    }), 201
