import os
from flask import Flask, jsonify
import psycopg2
from flask_bcrypt import Bcrypt

# Initialize application
app = Flask(__name__)

# Initialize Bcrypt
app.config['SECRET_KEY'] = '12345678'
bcrypt = Bcrypt(app)

conn = psycopg2.connect(database = "epicmail",user="postgres", password="postgres",host="localhost",port=5432)


from app.routes.user_routes import UserUrl
UserUrl.get_user_routes(app)
