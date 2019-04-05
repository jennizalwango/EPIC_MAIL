import os
from flask import Flask, jsonify
import psycopg2
from flask_bcrypt import Bcrypt
from flask_cors import CORS
# Initialize application
app = Flask(__name__)
cors = CORS(app)

# Initialize Bcrypt
app.config['SECRET_KEY'] = '12345678'
bcrypt = Bcrypt(app)

# conn = psycopg2.connect(os.environ.get('DATABASE_URL'))

# conn = psycopg2.connect(database="epicmail", user="postgres", password="postgres", host="localhost", port=5432)

conn = psycopg2.connect(
  database="d7oe093sstb9l5", 
  user="jplzedaofwqxjg", password="da09959fb59f00f876743b021b00872a9a38fbd87346a712356e520ee438f1bc", host="ec2-54-221-243-211.compute-1.amazonaws.com", 
  port=5432)


from app.routes.user_routes import UserUrl
from app.routes.mail_route import MessageUrls
from app.routes.group_route import GroupUrl
UserUrl.get_user_routes(app)
MessageUrls.get_mail_routes(app)
GroupUrl.get_group_routes(app)
