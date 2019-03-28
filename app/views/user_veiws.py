import re
from flask import request, jsonify, make_response
from flask.views import MethodView
from app import bcrypt, conn
from app.models.user_model import User


class RegisterUser(MethodView):
    """
    View function to register a user 
    """

    def post(self):
        """
        Register a user, generate their token and add them to the database
        :return: Json Response with the user`s token
        """
        if request.content_type == 'application/json':
            if 'firstname' in request.json and 'lastname' in request.json and 'email' in request.json and 'password' in request.json:
                post_data = request.get_json()
                firstname = post_data.get('firstname')
                lastname = post_data.get('lastname')
                email = post_data.get('email')
                password = post_data.get('password')
                isAdmin = post_data.get('isAdmin')

                if isinstance(firstname, str) and isinstance(lastname, str):
                    if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(password) > 5:
                        user = User.get_by_email(email)
                        if not user:
                            User(firstname = firstname, lastname = lastname, email = email, password = password, isAdmin= isAdmin).save()
                            cur = conn.cursor()
                            sql1 = """
                                SELECT row_to_json(users) FROM users WHERE email=%s
                            """
                            cur.execute(sql1,(email,))
                            user = cur.fetchone()
                            return jsonify({
                                            'status': 201,
                                            'data': [{"token": User.encode_auth_token(email).decode('utf-8'), "user": user[0] }]
                                        }), 201
                        return jsonify({"status":400, "error":"Failed, User already exists, Please sign In"}), 400
                    return jsonify({"status":400, "error": "Missing or wrong email format or password is less than five characters"}),400
                return jsonify({"status":400, "error": "Firstname or Lastname should be a string"}),400
            return jsonify({"status":400, "error":"Firstname or Lastname or Email or password is missing"}),400
        return jsonify({"status":400, "error":"Content-type must be json"}),400


class LoginUser(MethodView):
    def post(self):
        """
        Login a user if the supplied credentials are correct.
        :return: Http Json response
        """
        if request.content_type == 'application/json':
            post_data = request.get_json()
            email = post_data.get('email')
            password = post_data.get('password')
        
            if re.match(r"[^@]+@[^@]+\.[^@]+", email) and len(password ) > 5:
                cur = conn.cursor()
                sql1 = """
                    SELECT row_to_json(users) FROM users WHERE email=%s
                """
                cur.execute(sql1,(email,))
                user = cur.fetchone()
                if user and bcrypt.check_password_hash(user[0]['password'], password):
                    return jsonify({
                                            'status': 200,
                                            'data': [{"token": User.encode_auth_token(user[0]['user_id']).decode('utf-8'), "user": user[0] }]
                                        }), 200
                return jsonify({"status":401, "error":"User does not exist or password is incorrect"}), 401
            return jsonify({"status":400, "error":"Missing or wrong email format or password is less than five characters"}), 401
        return jsonify({"status":400, "error":"Content-type must be json"}), 400