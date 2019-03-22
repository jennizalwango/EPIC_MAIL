from flask import json
from app.tests.base import BaseTestCase


class APITestCaseUser(BaseTestCase):
  def test_register_user(self):
    with self.client:
      response = self.client.post("/auth/signup", data=json.dumps(self.create_user), content_type='application/json')
      self.assertEqual(response.status,'201 CREATED')

  def test_login_user_sucessful(self):
        with self.client:
            self.client.post("/auth/signup", data=json.dumps(self.create_user),content_type='application/json') 

            user = {
                "email":"jenny@gmail.com",
                "password": "password"
            }
            
            response = self.client.post("/auth/login", data=json.dumps(self.create_user), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            results = json.loads(response.data.decode())
            self.assertIn("Login successful", results["message"] )
            