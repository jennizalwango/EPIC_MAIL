import re
import datetime
from flask import request, jsonify, make_response
from flask.views import MethodView
from app import bcrypt, conn
from app.models.group_model import Group
from app.models.user_model import User
from app.views.helper import token_required



class CreateGroup(MethodView):

  """
  View function to register a group 
  """
  @token_required
  def post(current_user, self):
    """
    Register a user, generate their token and add them to the database
    :return: Json Response with the user`s token
    """
    # check if user is an admin
    status = User.check_if_admin(current_user)
    if not status == "true":
      return jsonify({"status":401, "message":"You don't have admin rights to execute this resource"})
    
    if request.content_type == 'application/json':
      if 'name' in request.json and 'role' in request.json:
        data = request.get_json()
        groupname = data.get('name')
        grouprole = data.get('role')
        groupowner = current_user
        
        if isinstance(grouprole, str) and isinstance(grouprole, str):

          group = Group.get_group_by_groupname(groupname)
          if not group:
            Group(groupname=groupname, grouprole=grouprole,
                  groupowner=groupowner).save_group()
            cur = conn.cursor()
            sql1 = """
                SELECT row_to_json(groups) FROM groups WHERE groupname=%s
            """
            cur.execute(sql1, (groupname,))
            group_details = cur.fetchone()
            return jsonify({
                          'status': 201,
                          'data': [{ "id": group_details[0]['group_id'], 'name':group_details[0]['groupname'], 'role':group_details[0]['grouprole']}]
                        }), 201
          return jsonify({"status": 400, "error": "Failed, Groupname already exists"}), 400
        return jsonify({"status": 400, "error": "groupname or grouprole or groupowner should be a string"}), 400
      return jsonify({"status": 400, "error": "groupname or grouprole is missing"}), 400
    return jsonify({"status": 400, "error": "Content type must json"}), 400

  @token_required
  def get(current_user, self, group_id):
    if group_id is None:
        groups = Group.get_all_groups(current_user)
        if not groups:
          return jsonify({'status':200, 'message':'No group found'})
        return jsonify({
          "status": 200,
          "data": groups
        }), 200

    try:
      groupId = int(group_id)
    except:
      return jsonify({'status':400, 'error':'Invalid group id'})

    group_details = Group.get_a_specific_group(groupId)
    if group_details:
      return jsonify({
            "status": 200,
            'data': [{ "id": group_details[0]['group_id'], 'name':group_details[0]['groupname'], 'role':group_details[0]['grouprole']}]
        }),200
    return jsonify({'status':400, 'error':'No group found'})

  @token_required
  def delete(current_user, self, group_id):
     # check if user is an admin
    status = User.check_if_admin(current_user)
    if not status == "true":
      return jsonify({"status":401, "message":"You don't have admin rights to execute this resource"})
    
    try:
        groupId = int(group_id)
    except:
        return jsonify({'status':404, 'error':'Invalid group_id'})

    sql = """
            SELECT * FROM groups WHERE group_id=%s
          """
    cur = conn.cursor()
    cur.execute(sql,(groupId,))
    groups = cur.fetchone()
    if groups:
        sql = """
                DELETE FROM groups WHERE group_id=%s
              """
        cur = conn.cursor()
        cur.execute(sql,(groupId,))
        return jsonify({'status':200, 'data':[{'message':'Group deleted successfully'}]})
    return jsonify({'status':200, 'error':'No group found'})

  @token_required
  def put(current_user, self, group_id):
     # check if user is an admin
    status = User.check_if_admin(current_user)
    if not status == "true":
      return jsonify({"status":401, "message":"You don't have admin rights to execute this resource"})
    
    try:
        groupId = int(group_id)
    except:
        return jsonify({'status':404, 'error':'Invalid group_id'})

    if 'name' not in request.json:
       return jsonify({'status':400, 'message':'Missing group name'})

    posted_data = request.get_json()
    new_group_name = posted_data['name']
    if not isinstance(new_group_name, str) or not new_group_name:
      return jsonify({'status':400, 'message':'The group name must a string and cannot be empty'})


    sql = """
            SELECT grouprole FROM groups WHERE group_id=%s
          """
    cur = conn.cursor()
    cur.execute(sql,(groupId,))
    groups = cur.fetchone()
    if groups:
        sql2 = """
          UPDATE groups set groupname=%s WHERE group_id=%s
        """
        cur = conn.cursor()
        cur.execute(sql2,(new_group_name, groupId,))
        return jsonify({'status':200, 'data':[{'id':groupId, 'name':new_group_name, 'role':groups[0]}]})
    return jsonify({'status':200, 'error':'No group found'})

class UserGroup(MethodView):
  @token_required
  def post(current_user,self, group_id):
    # check if user is an admin
    status = User.check_if_admin(current_user)
    if not status == "true":
      return jsonify({"status":401, "message":"You don't have admin rights to execute this resource"})
    
    if 'userId' not in request.json or 'userRole' not in request.json:
      return jsonify({"status":400, "message":"Missing UserId or userRole"})
    
    posted_data = request.get_json()
    if not isinstance(posted_data['userId'], int) or not isinstance(posted_data['userRole'], str):
      return jsonify({"status":400, "message":"Incorrect userId or userRole format"})
    
    try:
      groupId = int(group_id)
    except:
      return jsonify({"status":400, "message":"Invalid group_id"})

    sql = """
            SELECT grouprole FROM groups WHERE group_id=%s
          """
    cur = conn.cursor()
    cur.execute(sql,(groupId,))
    groups = cur.fetchone()
    if groups:
        sql = """
            INSERT INTO group_users(group_id, userId, userRole, registered_on) VALUES(%s,%s,%s,%s)
        """
        cur = conn.cursor()
        cur.execute(sql,(groupId, posted_data['userId'], posted_data['userRole'],str(datetime.datetime.now()),))

        get_group_users = """
                                SELECT row_to_json(group_users) FROM group_users WHERE group_id=%s
                            """
        cur = conn.cursor()
        cur.execute(get_group_users ,(groupId,))
        group_users = cur.fetchall()
        return jsonify({'status':200, 'data':group_users})
    return jsonify({'status':200, 'error':'No group found'})

  @token_required
  def delete(current_user, self, group_id, user_id):
     # check if user is an admin
    status = User.check_if_admin(current_user)
    if not status == "true":
      return jsonify({"status":401, "message":"You don't have admin rights to execute this resource"})
    
    try:
        groupId = int(group_id)
        userId = int(user_id)
    except:
        return jsonify({'status':404, 'error':'Invalid group_id or user_id'})

    sql1 = """
            SELECT * FROM groups WHERE group_id=%s
          """
    cur = conn.cursor()
    cur.execute(sql1,(groupId,))
    groups = cur.fetchone()

    sql2 = """
            SELECT * FROM users WHERE user_id=%s
          """
    cur = conn.cursor()
    cur.execute(sql2,(userId,))
    users= cur.fetchone()
    if groups and users:
        sql = """
                DELETE FROM group_users WHERE group_id=%s  AND userId=%s
              """
        cur = conn.cursor()
        cur.execute(sql,(groupId,userId))
        return jsonify({'status':200, 'data':[{'message':'User deleted from the successfully'}]})
    return jsonify({'status':200, 'error':'No group or user found'})

class GroupMails(MethodView):
  @token_required
  def post(current_user, self, group_id):
    if request.content_type == 'application/json':
        if 'subject' in request.json and 'message' in request.json:
            post_data = request.get_json()
            subject = post_data.get('subject')
            message = post_data.get('message')
            
            if isinstance(subject, str) and isinstance(message, str):
              try:
                groupId = int(group_id)
              except:
                return jsonify({'status':400, 'message':'Invalid group_id'})
              
              
              cur = conn.cursor()
              sql = """
                  INSERT INTO group_messages (senderId, groupId, subject, message, parentMessageId, createdOn) 
                          VALUES (%s, %s, %s, %s, %s, %s)
              """
              createdOn = str(datetime.datetime.now())
              cur.execute(sql,(current_user, groupId, subject, message, current_user, createdOn))
              conn.commit()
              f = """SELECT currval(pg_get_serial_sequence(%s,%s))"""
              cur.execute(f,('group_messages', 'id'))
              latest_id = cur.fetchone()
              
              return jsonify({'status':'success','data':[{'id':latest_id[0], 'createdOn':createdOn,'subject':subject,'message':message,'parentMessageId':current_user,'status':'sent'}]})
                
            return jsonify({'status':400, 'message':'subject or message must be strings'})
        return jsonify({'status':400, 'message':'wrong message format'})
    return jsonify({"status":400, "error":"Content-type must be json"}),400
      


      


      


