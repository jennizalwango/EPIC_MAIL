import unittest
from flask import json
from app.tests.base import BaseTestCase


class APITestCaseUser(BaseTestCase):
  def test_register_user(self):
    with self.client:

      new_user = {
        "firstname":"jenny",
        "lastname":"babyjenny",
        "email":"baby@gmail.com",
        "password":"1234567",
        "isAdmin":"True"
      }
      response = self.client.post(
        "/api/v2/auth/signup", 
        data=json.dumps(new_user), 
        content_type='application/json')
      self.assertEqual(response.status, '201 CREATED')
  

  def test_register_user_already_exists(self):
    with self.client:
      self.client.post(
        "/api/v2/auth/signup", 
        data=json.dumps(self.create_user), 
        content_type='application/json')
      resp = self.client.post(
        "/api/v2/auth/signup", 
        data=json.dumps(self.create_user), 
        content_type='application/json')
      print(resp.data)
      self.assertEqual(resp.status_code, 400)
      self.assertIn("Failed, User already exists, Please sign In", str(resp.data))

  def test_login_user_sucessful(self):
    with self.client:
      response = self.client.post(
        "/api/v2/auth/login", data=json.dumps(self.login_credentials), 
        content_type='application/json')
      self.assertEqual(response.status_code, 200)

      