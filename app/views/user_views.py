""""""
from flask import request, jsonify
import datetime
from app.models.user_model import User
from flask.views import MethodView
from app.views.validations import Validations
from app.models.user_model import user_list
from app.models.user_model import current_user

class CreateUser(MethodView):
    def post(self):
        data = request.get_json(force=True)
        contentType = request.content_type

        valids = Validations()
        validation_result = valids.create_user_validation(contentType, data)
        if validation_result:
            return jsonify(validation_result), 400

        first_name = data.get("first_name", None)
        last_name = data.get("last_name", None)
        password = data.get("password", None)
        email = data.get("email", None)
        is_admin = data.get("is_admin", None)

        for user in user_list:
            if user.email == email:
                return jsonify({
                    "status": 400,
                    "message": "User email already exits,Register again"
                }), 400
        
        user = User(first_name, last_name, email, password, is_admin)
        user_list.append(user)
        auth_token = user.encode_auth_token(user.id)
        response = {
            "status": 201,
            "message": "User account created successfully",
            "data": [{
                'token':str(auth_token)
                }]
        }
        return jsonify(response), 201


class LoginUser(MethodView):
    def post(self):
        data = request.get_json()
        contentType = request.content_type

        validate_login = Validations()
        login_results = validate_login.login_validations(contentType, data)
        if login_results:
            return jsonify(login_results), 400
        
        data = request.get_json(force=True)
        email = data.get("email", None)
        password = data.get("password", None)

        for user in user_list:
            if user.email == email and user.password == password:
                auth_token = user.encode_auth_token(user.id)
                return jsonify({
                    "status": 200,
                    "message": "Login successful",
                    "data": [{
                        'token':str(auth_token)
                    }]
                }), 200

        return jsonify({
          "status": 400,
          "error": "Invaild email or password"
          }), 400
