import datetime
import jwt
from app import app, conn, bcrypt

# establish a connection between our
# apllication and the database
cur = conn.cursor()


# User modal. this will be use as a template
# for creating objects of this class
class Message:
    """
    Table schema
    """

    # lets create a mails table if it doesnt exist
    cur.execute('''CREATE TABLE IF NOT EXISTS messages
            ( id SERIAL PRIMARY KEY    NOT NULL,
            senderId       INTEGER     NOT NULL,
            receiverId     INTEGER     NOT NULL,
            subject        VARCHAR(25)     NOT NULL,
            message        VARCHAR(25)     NOT NULL,
            parentMessageId     INTEGER     NOT NULL,   
            status VARCHAR(100)  DEFAULT 'sent',        
            createdOn     DATE     NOT NULL );''')

    # this constructor is called each time we create a new user

    def __init__(self, senderId, receiverEmail, subject,
                 message, parentMessageId):
        self.senderId = senderId
        self.receiverEmail = receiverEmail
        self.subject = subject
        self.message = message
        self.parentMessageId = parentMessageId
        self.createdOn = str(datetime.datetime.now())

    # this saves users info into the database

    def save(self):
        """
        Persist the message in the database
        """
        cur = conn.cursor()
        sql = """
            INSERT INTO messages (senderId, receiverId, subject, 
            message, parentMessageId, createdOn) 
                    VALUES (%s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql, (self.senderId, Message.get_userId(self.receiverEmail),
                          self.subject, self.message,
                          self.parentMessageId, self.createdOn))
        conn.commit()

    @staticmethod
    def get_userId(user_email):
        """
        Get user_id
        :param email:
        :return: user_id
        """
        cur = conn.cursor()
        sql1 = """
             SELECT user_id FROM users WHERE email=%s
        """
        cur.execute(sql1, (user_email,))
        user = cur.fetchone()
        user_id = user[0]
        return user_id
