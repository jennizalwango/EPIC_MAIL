import datetime
import jwt
from app import app, conn
cur = conn.cursor()


class Group:
    """
    Table schema
    """
    # lets create a group table if it doesnt exist
    cur.execute('''CREATE TABLE IF NOT EXISTS groups
            ( Group_id SERIAL PRIMARY KEY    NOT NULL,
            groupname         VARCHAR(25)     NOT NULL,
            grouprole          VARCHAR(25)     NOT NULL,
            groupowner         INTEGER     NOT NULL,          
            registered_on     DATE     NOT NULL );''')

    # lets create a users_group table if it doesnt exist
    cur.execute('''CREATE TABLE IF NOT EXISTS group_users
            ( id SERIAL PRIMARY KEY    NOT NULL,
              group_id     INTEGER     NOT NULL,
              userId        INTEGER     NOT NULL,
              userRole          VARCHAR(25)     NOT NULL,         
              registered_on     DATE     NOT NULL );''')

    cur.execute('''CREATE TABLE IF NOT EXISTS group_messages
            ( id SERIAL PRIMARY KEY    NOT NULL,
            senderId       INTEGER     NOT NULL,
            groupId     INTEGER     NOT NULL,
            subject        VARCHAR(25)     NOT NULL,
            message        VARCHAR(25)     NOT NULL,
            parentMessageId     INTEGER     NOT NULL,   
            status VARCHAR(100)  DEFAULT 'sent',        
            createdOn     DATE     NOT NULL );''')

    # this constructor is called each time we create a new user

    def __init__(self, group_name, group_role, group_owner):
        self. group_name = group_name
        self. group_role = group_role
        self. group_owner = group_owner
        self.registered_on = str(datetime.datetime.now())

    def save_group(self):
        """
        Persist the group in the database
        :param group:
        :return:
        """
        cur = conn.cursor()
        sql = """
            INSERT INTO groups (groupname, grouprole, \
                groupowner, registered_on) 
                    VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (self.group_name, self.group_role,
                          self.group_owner, self.registered_on))
        conn.commit()

    @staticmethod
    def get_group_by_groupname(group_name):
        """
        Filter a group by group_name.
        :param group_name:
        :return: group or None
        """
        cur = conn.cursor()
        sql1 = """
             SELECT * FROM groups WHERE groupname=%s
        """
        cur.execute(sql1, (group_name,))
        group = cur.fetchone()
        return group

    @staticmethod
    def get_all_groups(user_id):
        cur = conn.cursor()
        query = "SELECT row_to_json(groups) FROM groups WHERE\
             group_owner = %s"
        cur.execute(query, (user_id,))
        all_groups = cur.fetchall()
        return all_groups

    @staticmethod
    def get_group_names():
        cur = conn.cursor()
        query = "SELECT row_to_json(groups) FROM groups"
        cur.execute(query)
        all_groups = cur.fetchall()
        return all_groups

    @staticmethod
    def get_group_type(group_id):
        cur = conn.cursor()
        query = "SELECT group_owner FROM groups WHERE\
             group_id = '{}'".format(
            group_id)
        cur.execute(query)
        get_the_group = cur.fetchone()
        return get_the_group

    @staticmethod
    def check_group_id(group_id):
        cur = conn.cursor()
        query = "SELECT row_to_json(groups) FROM groups WHERE\
            group_id = '{}';".format(
            group_id)
        cur.execute(query)
        checking_group_id = cur.fetchone()
        return checking_group_id

    @staticmethod
    def get_a_specific_group(group_id):
        cur = conn.cursor()
        query = "SELECT row_to_json(groups) FROM groups WHERE\
             group_id = '{}';".format(
            group_id)
        cur.execute(query)
        specific_group = cur.fetchone()
        return specific_group

    @staticmethod
    def update_groupname(user_id, group_id, group_name):
        cur = conn.cursor()
        query = "UPDATE groups SET group_name = '{}' WHERE\
             group_id = '{}';".format(
            group_name, group_id)
        cur.execute(query)