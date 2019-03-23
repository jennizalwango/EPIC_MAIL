from unittest import TestCase
from app.views import mail_views
from app.views import user_views
from app.config import configuration
from app import app


def create_app(environment):
  app.config.from_object(configuration.get(environment))
  client = app.test_client()

class BaseTestCase(TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.client = app.test_client()
    self.create_user = {
      "first_name": "zawal",
      "last_name": "jenni", 
      "email": "jenny@gmail.com", 
      "password": "password",
      "is_admin": False
    }

    self.create_message = {
      "subject": "tech",
      "message": "levelup",
      "status": "sent",
      "receiver_id":1,
	    "sender_id":2
    }


  def tearDown(self):
    user_views.user_list = []
    mail_views.message_list = []
