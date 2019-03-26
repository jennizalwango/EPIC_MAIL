import os
import psycopg2
from flask import Flask
from app.config import configuration

config = configuration.get(os.environ.get("APP_ENV", "development"))
app = Flask(__name__)
app.config.from_object(config)


from app.routes.user_routes import UserUrl
UserUrl.get_user_routes(app)
