import os
from flask import Flask, jsonify
import psycopg2
from flask_bcrypt import Bcrypt

# Initialize application
app = Flask(__name__)

# Initialize Bcrypt
app.config['SECRET_KEY'] = '12345678'
bcrypt = Bcrypt(app)


conn = psycopg2.connect(os.environ.get('DATABASE_URL'))

from app.routes.user_routes import UserUrl
from app.routes.mail_route import MessageUrls
from app.routes.group_route import GroupUrl
UserUrl.get_user_routes(app)
MessageUrls.get_mail_routes(app)
GroupUrl.get_group_routes(app)
