from flask import json
from app.tests.base import BaseTestCase


class APITestCaseMessages(BaseTestCase):
    def test_create_message(self):
        with self.client:
            self.client.post(
                "/api/v1/auth/signup", 
                data=json.dumps(self.create_user), 
                content_type='application/json')
            response = self.client.post(
                "/api/v1/messages", 
                data=json.dumps(self.create_message), 
                content_type='application/json')
            self.assertEqual(response.status_code, 201)

    def test_get_specific_message(self):
        with self.client:
            self.client.post("/api/v1/auth/signup",
                             data=json.dumps(self.create_user))
            response = self.client.get(
                "/api/v1/messages/1", content_type='application/json')
            self.assertEqual(response.status_code, 404)

    def test_fetch_all_messages(self):
        with self.client:
            self.client.post("/api/v1/auth/signup",
                             data=json.dumps(self.create_user))
            response = self.client.get(
                "/api/v1/messages", content_type='application/json')
            self.assertEqual(response.status_code, 404)

    def test_fetch_all_sent_messages(self):
        with self.client:
            self.client.post("/api/v1/auth/signup",
                             data=json.dumps(self.create_user))
            response = self.client.get(
                "/api/v1/messages/sent", content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_fetch_all_unread_messages(self):
        with self.client:
            self.client.post("/api/v1/auth/signup",
                             data=json.dumps(self.create_user))
            response = self.client.get(
                "/api/v1/messages/unread", content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_delete_a_specific_message(self):
        with self.client:
            self.client.post("/api/v1/auth/signup",
                             data=json.dumps(self.create_message))
            response = self.client.delete(
                "/api/v1/messages/1", content_type='application/json')
            self.assertEqual(response.status_code, 404)
