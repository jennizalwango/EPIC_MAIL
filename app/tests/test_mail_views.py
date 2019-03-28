# import unittest
# from flask import json
# from app.tests.base import BaseTestCase

# class APITestCaseMessages(BaseTestCase):
#   def test_create_message(self):
#     response = self.client.post(
#       "/api/v2/messages",
#       data=json.dumps(self.create_message),
#       headers=dict(Authorization="Bearer" +self.generate_token()),
#       content_type='application/json')
#     print(response.data)
#     self.assertEqual(json.loads(response.data)['data'][0], 201)