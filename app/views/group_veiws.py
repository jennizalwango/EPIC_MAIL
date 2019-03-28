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
        
        if isinstance(grouprole, str) and isinstance(groupname, str):

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
        return jsonify({"status": 400, "error": "groupname or grouprole  should be a string"}), 400
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
    return jsonify({
          "status": 200,
          'data': [{ "id": group_details[0]['group_id'], 'name':group_details[0]['groupname'], 'role':group_details[0]['grouprole']}]
      }),200

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