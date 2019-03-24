import datetime
from app.config import Config
import jwt

user_list = []
current_user = None


class User:
    def __init__(self, first_name, last_name, email, password, is_admin):
        self.id = self.generate_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.created_on = datetime.datetime.now()
        self.is_admin = is_admin

    def to_dict(self):
        return self.__dict__

    def to_str(self):
        return str(self.__dict__)

    @staticmethod
    def generate_id():
        user_id = len(user_list) + 1
        for user in user_list:
            if user.id == user_id:
                user_id += 1
        return user_id

    @staticmethod
    def encode_auth_token(user_id):
        """
        Encode the Auth token
        :param user_id: User's Id
        :return:
        """
        config_object = Config()
        config_object.SECRET_KEY
        try:
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id
            }
            return jwt.encode(
                payload,
                config_object.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as error:
            print("something wrong happened: {}".format(str(error)))

    @staticmethod
    def decode_auth_token(token):
        try:
           # to decode the token, u need to pass in the token to be decoded, \
           # the key u used to encrypt it, and the method to use to decode it
            payload = jwt.decode(
                token,
                config_object.SECRET_KEY,
                algorithms
            )
        except jwt.ExpiredSignatureError:
            return "Signature expired, Please sign in again"

        except jwt.InvalidTokenError:
            return "Invalid Key.Please sign in again"
