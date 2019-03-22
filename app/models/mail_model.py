
from datetime import datetime

message_list = []

class Messages:
  def __init__(self, subject, message, status, sender_id, receiver_id):
    self.message_id = Messages.generate_id()
    self.parentMessageId = self.generate_parent_message_id()
    self.created_on = datetime.now()
    self.subject = subject
    self.message = message
    self.status = status
    self.sender_id = sender_id
    self.receiver_id = receiver_id

  def to_dict(self):
    return self.__dict__

  def to_str(self):
    return str(self.__dict__)
  
  @staticmethod
  def generate_id():
    message_id = len(message_list) + 1
    for message in message_list:
      if message.message_id == message_id:
        message_id += 1
    return message_id

  @staticmethod
  def generate_parent_message_id():
    parent_msg_id = len(message_list) + 1
    if not message_list:
      parent_msg_id = 1
      return parent_msg_id
    for message in message_list:
      if message.parentMessageId == parent_msg_id:
        parent_msg_id += 1
      return parent_msg_id