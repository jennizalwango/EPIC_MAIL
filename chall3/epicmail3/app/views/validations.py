import datetime
import re
from flask import request, jsonify
from app.models.user_model import User


class Validations:
    def create_user_validation(self, contentType, data):
        if contentType != "application/json":
            return jsonify({
                "status": 400,
                "message": "Wrong content Type"
            }), 400

        if "first_name" not in data or "last_name" not in data or "email"\
            not in data or "password" not in data or "is_admin" not in data:
            return jsonify({
                "status": 400,
                "message": "wrong Body Format"
            }), 400

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        is_admin = data.get("is_admin")
    
        if not first_name:
            return jsonify({
                "status": 400,
                "message": "first name should not be empty"
            }), 400

            if not email:
                return jsonify({
                "status": 400,
                "message": "Email should not be empty"
            }), 400

            elif not last_name:
                return jsonify({
                "status": 400,
                "message": "Last name should not be empty"
            }), 400

            elif not password:
                return jsonify({
                "status": 400,
                "message": "Password should not be empty"
            }), 400

            elif not is_admin:
                return jsonify({
                "status": 400,
                "message": "Is Admin should not be empty"
            }), 400

        if not isinstance(first_name, str) and len(password) < 5:
            return jsonify({
                "status": 400,
                "message": "First name should be strings and password should have more than 5 characters"
            }), 400

            if not isinstance(last_name, str):
                return jsonify({
                "status": 400,
                "message": "A Last name should be an strings"
            }), 400

            elif not isinstance(email, str):
                return jsonify({
                "status": 400,
                "message": "Email should be  strings"
            }), 400

            elif not isinstance(is_admin,bool):
                return jsonify({
                "status": 400,
                "message": "is_admin should be a Boolean" 
            }), 400

        if  not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({
                "status":400,
                "message": "Wrong format of the email"
            }), 400
       
        # check if the user is in the database by using the email.
        user = User.check_user(email)
        if user:
            return jsonify({
                "status": 400,
                "message": "User already exists,Please check your email"
            }), 400
        return True
        