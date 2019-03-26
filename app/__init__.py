from app.routes.mail_routes import CreatemessageUrl
from app.routes.user_routes import UserUrl
from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


UserUrl.get_user_routes(app)

CreatemessageUrl.get_messages_route(app)
