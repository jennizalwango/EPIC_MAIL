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
        status = "sent"
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

    def get(self, data):  
       # data is either status or message-id 
        # get all received mails
        if data is None:
            received_mails = [mail.to_dict() for mail in message_list if mail.to_dict()['status'] == 'received']
            if not received_mails:
                return jsonify({
                    "status": 404,
                    "error": "No received mails found"
                })
            return jsonify({
                        "status":200,
                        "data": received_mails 
                    })
        # get all sent or unread or received mails
        if data in ['sent','unread','received','draft']:
            mails = [mail.to_dict() for mail in message_list if mail.to_dict()['status'] == data]
            if not mails:
                return jsonify({
                    "status": 400,
                    "error": "Not mail found"
                })
            return jsonify({
                        "status":200,
                        "data": mails
                    })
        # fetch a specific mail
        try:
            message_id = int(data)
        except:
            return jsonify({
                    "status": 400,
                    "error": "Invalid status or message_id"
                })

        get_mail = [mail.to_dict() for mail in message_list if mail.to_dict()['message_id'] == int(data)]
        if not get_mail:
            return jsonify({
                "status": 404,
                "error": "Mail not found"
            })
        return jsonify({
                    "status": 200,
                    "data": get_mail
                })
         
    def delete(self, data):
        try:
            message_id = int(data)
        except:
            return jsonify({
                        "status": 400,
                        "error": "Invalid message_id"
                    })
        get_mail = [mail for mail in message_list if mail.to_dict['message_id'] == int(data)]
        if not get_mail:
            return jsonify({
                "status": 404,
                "error": "Mail not found"
            })
        message_list.remove(get_mail[0])
        return jsonify({
                    "status": 200,
                    "data": [{'message': 'Message successfully deleted'}]
                })
        