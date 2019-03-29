from app import app, conn
from flask_testing import TestCase
import json
import string
import random



class BaseTestCase(TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        :return:
        """
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        """
        Create a cursor for your database
        :return:
        """
        cur = conn.cursor()

    def tearDown(self):
        """
        Close connection after running database executions
        :return:
        """
        conn.commit()

    def register_user(self, firstname, lastname, email, password, isAdmin):
        """
        Helper method for registering a user with dummy data
        :return:
        """
        return self.client.post(
            '/api/v2/auth/signup',
            content_type='application/json',
            data=json.dumps(dict(firstname=firstname, lastname=lastname, email=email, password=password, isAdmin=isAdmin)))

    def login_user(self, email, password):
        """
        Helper method for registering a user with dummy data
        :return:
        """
        response = self.register_user('jenny', 'zalwango', 'abc@gmail.com', '123456', True)
        return self.client.post(
            '/api/v2/auth/login',
            content_type='application/json',
            data=json.dumps(dict(email=email, password=password)))

    def login_admin(self, email, password):
        """
        Helper method for registering a user with dummy data
        :return:
        """
        response = self.register_user('jenny', 'zalwango', 'admin@gmail.com', '123456', True)
        return self.client.post(
            '/api/v2/auth/login',
            content_type='application/json',
            data=json.dumps(dict(email=email, password=password)))


 
    def create_mail(self, subject,message,receiverEmail):
        return self.client.post(
            '/api/v2/messages',
            content_type='application/json',
            data=json.dumps(dict(subject=subject, message=message,receiverEmail=receiverEmail)))

    
    def get_user_token(self):
        """
        Get a user token
        :return:
        """
        auth_res = self.login_user('abc@gmail.com', '123456')
        return json.loads(auth_res.data.decode())['data'][0]['token']
    
    def get_admin_token(self):
        """
        Get a user token
        :return:
        """
        auth_res = self.login_admin('admin@gmail.com', '123456')
        return json.loads(auth_res.data.decode())['data'][0]['token']