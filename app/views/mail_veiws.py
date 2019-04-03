import re
import datetime
from flask import request, jsonify, make_response
from flask.views import MethodView
from app.models.mail_model import Message
from app import conn
from app.views.helper import token_required
from app.models.user_model import User


class MessageViews(MethodView):
    """
    View function to send a message 
    """
    @token_required
    def post(current_user, self):
        if request.content_type == 'application/json':
            if 'receiverEmail' in request.json and 'subject' in request.json \
                    and 'message' in request.json:
                post_data = request.get_json()
                receiverEmail = post_data.get('receiverEmail')
                subject = post_data.get('subject')
                message = post_data.get('message')

                if isinstance(subject, str) and isinstance(message, str):
                    if re.match(r"[^@]+@[^@]+\.[^@]+", receiverEmail):
                        verify_email = Message.get_userId(receiverEmail)
                        if not verify_email:
                            return jsonify({
                                "status": 400,
                                "data": "User with this email does not exist"
                            }), 400
                        createdOn = str(datetime.datetime.now())
                        Message(receiverEmail=receiverEmail,
                                subject=subject, message=message, 
                                senderId=current_user,
                                parentMessageId=current_user).save()
                        cur = conn.cursor()
                        f = """SELECT currval(pg_get_serial_sequence(%s,%s))"""
                        cur.execute(f, ('messages', 'id'))
                        latest_id = cur.fetchone()
                        return jsonify({
                            'status': 200,
                            'data': [{
                                'id': latest_id[0],
                                'createdOn':createdOn,
                                'subject':subject,
                                'message':message,
                                'parentMessageId':current_user,
                                'status':'sent'
                            }]})
                        return jsonify({
                            'status': 200,
                            'message': 'Message sent successfully'
                        })
                    return jsonify({
                        'status': 400,
                        'message': 'Invalid email'})
                return jsonify({
                    'status': 400,
                    'message': 'subject or message must be strings'
                })
            return jsonify({
                'status': 400,
                'message': 'wrong message format'
            })
        return jsonify({
            "status": 400,
            "error": "Content-type must be json"
        }), 400

    @token_required
    def get(current_user, self, data):
        if data is None:
            get_received_messages = """
                                SELECT * FROM messages WHERE receiverid=%s
                            """
            cur = conn.cursor()
            cur.execute(get_received_messages, (current_user,))
            messages = cur.fetchall()

            if messages:
                Message_details = []
               
                for mail in messages:
                    sender_email = User.get_user_email(mail[1])
                    receiver_email = User.get_user_email(mail[2])
                    record = {'id': mail[0],
                              'sender_mail':sender_email,
                              'receiver_mail':receiver_email,
                              'createdOn': mail[7],
                              'subject': mail[3],
                              'message': mail[4],
                              'parentMessageId': mail[5],
                              'status': 'received'
                              }
                    Message_details.append(record)
                return jsonify({'status': 200, 'data': Message_details})
            return jsonify({
                'status': 200,
                'data': 'No receieved messages found'
            })

        # get all sent or unread or received mails
        if data in ['sent', 'received', 'unread']:
            if data == 'unread' or data == 'received':
                if data == 'unread':
                    status = 'unread'
                else:
                    status = 'received'

                sql = """
                        SELECT * FROM messages WHERE receiverid=%s
                       """
            else:
                sql = """
                        SELECT * FROM messages WHERE senderid=%s
                      """
                status = 'sent'

            cur = conn.cursor()
            cur.execute(sql, (current_user,))
            messages = cur.fetchall()
            if messages:
                Message_details = []

                for mail in messages:
                    receiver_email = User.get_user_email(mail[2])
                    record = {'id': mail[0],
                              'receiver_mail': receiver_email,
                              'createdOn': mail[7],
                              'subject': mail[3],
                              'message': mail[4],
                              'parentMessageId': mail[5],
                              'status': status
                              }
                    Message_details.append(record)

                return jsonify({'status': 200, 'data': Message_details})
            return jsonify({
                'status': 200,
                'data': 'No '+data+' messages found'})

        try:
            message_id = int(data)
        except:
            return jsonify({
                'status': 404,
                'error': 'Invalid message_id'})

        sql = """
                SELECT row_to_json(messages) FROM messages WHERE id=%s
              """
        cur = conn.cursor()
        cur.execute(sql, (message_id,))
        messages = cur.fetchone()

        if messages:
            return jsonify({
                'status': 200,
                'data': messages})
        return jsonify({
            'status': 200,
            'data': 'No messages found'})

    @token_required
    def delete(current_user, self, data):
        try:
            message_id = int(data)
        except:
            return jsonify({
                'status': 404,
                'error': 'Invalid message_id'})

        sql = """
                SELECT * FROM messages WHERE id=%s
              """
        cur = conn.cursor()
        cur.execute(sql, (message_id,))
        messages = cur.fetchone()
        if messages:
            sql = """
                    DELETE FROM messages WHERE id=%s
                  """
            cur = conn.cursor()
            cur.execute(sql, (message_id,))
            return jsonify({
                'status': 200,
                'data': [{
                    'message': 'Message deleted successfully'
                }]})
        return jsonify({
            'status': 200,
            'data': 'No message found'
        })
