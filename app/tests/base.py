from unittest import TestCase
# from app.views.user_views import *
from app.config import configuration
from app import app, conn
from app import app
from app.models.user_model import User
from flask import json, Response

cur = conn.cursor()

def create_app(environment):
    app.config.from_object(configuration.get(environment))
    client = app.test_client()


class BaseTestCase(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = app.test_client()
        User.drop_tables()
        User.create_user_table()
        
        self.create_user = {
            "firstname":"segbo",
            "lastname":"chrhgistine",
            "email":"sbbo@gmail.com",
            "password":"123456",
            "isAdmin":"false"
            }
        self.login_credentials = {
                "email": "sbbo@gmail.com",
                "password": "123456"
            }
        self.create_message = {
            "receiverEmail": 1,
            "subject": "tech",
            "message": "levelup"  
        }

        
        self.client.post(
        "/api/v2/auth/signup", 
        data=json.dumps(self.create_user), 
        content_type='application/json')
        response_user = self.client.post(
            "/api/v2/auth/login", data=json.dumps(self.login_credentials), 
            content_type='application/json')
            
        # self.assertEqual(response_user.status_code, 200)

    # def tearDown(self):
    #     User.drop_tables()


    def generate_token(self):
        return User.encode_auth_token(1)


