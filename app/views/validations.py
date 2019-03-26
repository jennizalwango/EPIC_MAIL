import datetime
import re
from flask import request, jsonify
from app.models.user_model import User


class Validations:
    def create_user_validation(self, contentType, data):
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")
        email = data.get("email")
        is_admin = data.get("is_admin")

        if contentType != "application/json":
            return {
                "status": 400,
                "error": "Wrong content Type"
            }

        if "first_name" not in data or "last_name" not in data or "password"\
                not in data or "email" not in data or "is_admin" not in data:
            return {
                "status": 400,
                "error": "Wrong body format for user fields"
            }

        if first_name == "":
            return {
                "status": 400,
                "message": "Firsname should not be empty"
            }
        if email == "":
            return {
                "status": 400,
                "error": "Email should not be empty"
            }
        if last_name == "":
            return {
                "status": 400,
                "error": "Last name should not be empty"
            }
        if password == "":
            return {
                "status": 400,
                "error": "Password should not be empty"
            }

        if is_admin == "":
            return {
                "status": 400,
                "error": "is_admin should not be empty"
            }

        if not isinstance(first_name, str) and len(password) < 6:
            return {
                "status": 400,
                "error": "Firstname should be strings and password should \
                    have be greater or equal to 6 characters"
            }

            if not isinstance(last_name, str):
                return {
                    "status": 400,
                    "error": "Is_ admin should be an boolean"
                }
            elif not isinstance(email, str):
                return {
                    "status": 400,
                    "error": "Email should be  strings"
                }

            elif not isinstance(is_admin, bool):
                return {
                    "status": 400,
                    "error": "is_admin should be a Boolean"
                }

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {
                "status": 400,
                "error": "Wrong format of the email"
            }

        # check if username doesnot have digits
        if re.search("[0-9]", first_name) and re.search("[0-9]", last_name):
            return {
                "status": 400,
                "error": "Name should not contain digits"
            }

        return {}

    def login_validations(self, contentType, data):
        if contentType != "application/json":
            return {
                "status": 400,
                "error": "The application content should be json"
            }

        if "email" not in data and "password" not in data:
            return {
                "status": 400,
                "error": "Wrong body Fomat for login user"
            }

        data = request.get_json()
        email = data.get("email", None)
        password = data.get("password", None)

        if not email or not password:
            return {
                "status": 400,
                "error": "Please fields must not be empty"
            }

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {
                "status": 400,
                "error": "Wrong format of the email"
            }

        if not isinstance(email, str) and len(password) == 6:
            return {
                "status": 400,
                "error": "Please your email should be a string and Password must be equal to 6 characters"
            }
        return {}

    def create_message_validate(self, contentType, data):
        if contentType != "application/json":
            return {
                "status": 400,
                "message": "The application content type must be json"
            }

        if "subject" not in data or "message" not in data or "sender_id" not in data or "receiver_id" not in data:
            return {
                "status": 400,
                "message": "Wrong body format for creating message fields"
            }

        data = request.get_json()
        created_on = datetime.datetime.now()
        subject = data.get("subject")
        message = data.get("message")
        status = data.get("status")
        sender_id = data.get("sender_id")
        receiver_id = data.get("receiver_id")

        if not isinstance(subject, str) and not isinstance(message, str) and not isinstance(status, str):
            return {
                "status": 400,
                "message": "Fields must be Strings"
            }
        if not isinstance(sender_id, int) and not isinstance(receiver_id, int):
            return{
                "status": 400,
                "message": "The receiver ID and sender ID should be integer"
            }

        if not subject and not message and not subject and not receiver_id and not sender_id:
            return {
                "status": 400,
                "message": "Felids must not be empty"
            }
        return {}
