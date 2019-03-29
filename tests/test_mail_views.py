from tests.base import BaseTestCase
from app.models.user_model import User
from app import conn
import unittest
import json
import time
import string
import random

def email_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class TestAuthBluePrint(BaseTestCase):
    def test_send_mail(self):
        """
        Test a user is successfully created through the api
        :return:
        """
        with self.client:
            response = self.create_mail('INQUIRY','when is the next bootcamp','example@gmail.com' )
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            # self.assertEqual(response.status_code, 201)
        