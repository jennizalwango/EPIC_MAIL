import datetime
import jwt
from app import app, conn
cur = conn.cursor()

class Group:
    """
    Table schema
    """
    #lets create a users table if it doesnt exist
    cur.execute('''CREATE TABLE IF NOT EXISTS groups
            ( Group_id SERIAL PRIMARY KEY    NOT NULL,
            groupname         VARCHAR(255)     NOT NULL,
            grouprole          VARCHAR(255)     NOT NULL,
            groupowner         INTEGER     NOT NULL,          
            registered_on     DATE     NOT NULL );''')

    #this constructor is called each time we create a new user
    def __init__(self, groupname, grouprole, groupowner):
        self. groupname = groupname
        self. grouprole = grouprole
        self. groupowner = groupowner
        self.registered_on = str(datetime.datetime.now())

    def save_group(self):
        """
        Persist the group in the database
        :param group:
        :return:
        """
        cur = conn.cursor()
        sql = """
            INSERT INTO groups (groupname, grouprole, groupowner, registered_on) 
                    VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql,(self.groupname, self.grouprole, self.groupowner, self.registered_on))
        conn.commit()

    @staticmethod
    def get_group_by_groupname(groupname):
        """
        Filter a group by groupname.
        :param group_id:
        :return: group or None
        """
        cur = conn.cursor()
        sql1 = """
             SELECT * FROM groups WHERE groupname=%s
        """
        cur.execute(sql1,(groupname,))
        group = cur.fetchone()
        return group

    @staticmethod
    def get_all_groups(user_id):
        cur = conn.cursor()
        query = "SELECT row_to_json(groups) FROM groups WHERE groupowner = %s"
        cur.execute(query,(user_id,))
        all_groups = cur.fetchall()
        return all_groups   

    @staticmethod
    def get_group_type(group_id):
        cur = conn.cursor()
        query = "SELECT groupowner FROM groups WHERE group_id = '{}'".format(group_id)
        cur.execute(query)
        get_the_group = cur.fetchone()
        return get_the_group 

    @staticmethod
    def check_group_id(group_id):
        cur = conn.cursor()
        query = "SELECT row_to_json(groups) FROM groups WHERE group_id = '{}';".format(group_id)
        cur.execute(query)
        checking_group_id = cur.fetchone()
        return checking_group_id

    @staticmethod
    def get_a_specific_group(group_id):
        cur = conn.cursor()
        query = "SELECT row_to_json(groups) FROM groups WHERE group_id = '{}';".format(group_id)
        cur.execute(query)
        specific_group = cur.fetchone()
        return specific_group

    @staticmethod
    def update_groupname(user_id, group_id, groupname):
        cur = conn.cursor()
        query = "UPDATE groups SET groupname = '{}' WHERE group_id = '{}';".format(groupname, group_id)
        cur.execute(query)
