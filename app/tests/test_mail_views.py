"""""""
from flask import json
from app.tests.base import BaseTestCase


class APITestCaseMessages(BaseTestCase):
  def test_create_message(self):
    with self.client:
      self.client.post("/auth/signup", data=json.dumps(self.create_user),content_type='application/json')
      response = self.client.post("/messages", data=json.dumps(self.create_message), content_type='application/json')
      self.assertEqual(response.status_code, 201)

  
  def test_get_specific_message(self):
    with self.client:
      self.client.post("/auth/signup", data=json.dumps(self.create_user))
      response = self.client.get("/messages/1", content_type='application/json')
      self.assertEqual(response.status_code, 200)

  def test_delete_a_specific_message(self):
    with self.client:
      self.client.post("/auth/signup", data=json.dumps(self.create_message))
      response = self.client.delete("/messages/1", content_type='application/json')
      self.assertEqual(response.status_code, 200)
      