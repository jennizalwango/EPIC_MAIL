import datetime
from flask import jsonify
import jwt
from app import config
from app.conn_database.database import DatabaseConnection


db = DatabaseConnection()
cursor = db.dict_cursor


#  create a table for users
class User:
  def __init__(self, **kwargs):
    self.first_name = kwargs["first_name"]
    self.last_name = kwargs["last_name"]
    self.email = kwargs["email"]
    self.password = kwargs["password"]
    self.is_admin = kwargs["is_admin"]

  # Save is the same as creating user in the data base
  def save(self):
    query = """
              INSERT INTO users(first_name, last_name, email, password, is_admin)
              VALUES('{}', '{}', '{}', '{}', '{}')""".format(self.first_name, 
              self.last_name, self.email, self.password, 
              self.is_admin)
    cursor.execute(query)

  # do a query to check if our user exists in the database \
  # by using the username and the email
  @staticmethod
  def check_user(email):
    # here we use subquries because we dont want to return \
    # some data from the database like the password 
    query = "SELECT row_to_json(users) FROM users WHERE email = '{}';".format(email)
    cursor.execute(query)
    user = cursor.fetchone()
    return user

  # do a query to login the user into the system
#   @staticmethod
#   def login_user(username, password):
#     query = "SELECT row_to_json(users) FROM users WHERE username ='{}';".format(
#         username)
#     cursor.execute(query)
#     # returns the first record from the database that matches the provided username.
#     user_login = cursor.fetchone()
#     print (user_login[0]['user_id'])
#     # check if the user_login list is not empty and also if the provided password matches with the hashed password in our database.

#     if user_login and sha256_crypt.verify(password,user_login[0]['password']):
#     # if user_login and bcrypt.check_password_hash(user_login[0]['password'], password):
#       return jsonify({
#         'status': 200,
#         # we call a class user in our user model and the method that generates the token, we also  decode the bcause we want to be able to see the token
#         'data': [{
#           "token": User.encode_auth_token(user_login[0]['user_id']),
#           "user":user_login[0],
#           "message": "Login sucessful" 
#         }]
#       }), 200
#     return jsonify({
#       "status":401, 
#       "error":"User does not exist or password is incorrect"
#       }), 401


#   # do a method that is going to encode our token so that its generated
#   # the token will cotains the data we want to encrpyt, expiring time
#   # sub refers to the data to be encrypted
#   # secret key is the key we use t encrypt the data     
  
  @staticmethod
  def encode_auth_token(user_id):
    """generate the token"""
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id
        }
        # return the generated encrpyted token.
        return jwt.encode(
            payload,
            config.SECRET_KEY,
            algorithm='HS256'
        ).decode('utf-8')
    except Exception as error:
      print("something wrong happened: {}".format(str(error)))
        

  # """Decoding the token to get the payload and then return \
  # the user Id in 'sub'
  #       :param token: Auth Token
  #       :return:
  #       """
  @staticmethod
  def decode_auth_token(token):
    try:
       # to decode the token, u need to pass in the token to be decoded, \
       # the key u used to encrypt it, and the method to use to decode it
      payload = jwt.decode(
        token, 
        config.SECRET_KEY, 
        algorithms='HS256'
        )
      # All our expired or invaild tokens will be stored in blacklist_token \
      # table so that they are not used again.To do this we use a class and \
      # a method to actually check if the token is valid or not
      is_token_blacklisted = BlacklistToken.check_blacklist(token)
      # check if the token provided is blacklisted or its valid
      if is_token_blacklisted:
        return "Token was blacklisted, Please login "
      return payload["sub"]

    except jwt.ExpiredSignatureError:
      return "Signature expired, Please sign in again"

    except jwt.InvalidTokenError:
      return "Invalid Key.Please sign in again"


# class BlacklistToken:
#   def __init__(self, token):
#     self.token = token
#     self.Blacklisted_on = datetime.datetime.now()

#   def blacklist(self):
#     """Persist Blacklisted token in the database
#     :return:
#     """
#     cursor = db.dict_cursor()
#     query = "INSERT INTO blacklist_token(token, blacklisted_on) VALUES('{}',\
#        '{}')".format(self.token, self.Blacklisted_on)
#     cursor.execute(query, (self.token, self.Blacklisted_on))

#   @staticmethod
#   def check_blacklist(token):
#     """check to find out whether a token has already been blacklisted.
#     :param token: Authorization token
#     :return:
#     """
#     query = """SELECT token FROM blacklist_token WHERE token = '{}'"""
#     cursor.execute(query, (token))
#     response = cursor.fetchone()

#     if response:
#       return True
#     return False
