
""""""
from flask import request, jsonify
import datetime
from app.models.mail_model import Messages
from flask.views import MethodView
from app.views.validations import Validations
from app.models.mail_model import message_list


class CreateMail(MethodView):
    def post(self):
        data = request.get_json(force=True)
        contentType = request.content_type

        validates = Validations()
        val_results = validates.create_message_validate(contentType, data)
        if val_results:
            return jsonify(val_results), 400
        
        subject = data.get("subject", None)
        message = data.get("message", None)
        status = data.get("status", None)
        sender_id = data.get("sender_id",None)
        receiver_id = data.get("receiver_id",None)
        
        message = Messages(subject, message, status, sender_id, receiver_id)
        message_list.append(message)
        response = {
            "status": 201,
            "message": "Message  created successfully",
            "data": [message.to_dict()]
        }
        return jsonify(response), 201

        