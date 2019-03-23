from flask import Flask


app = Flask(__name__)


from app.routes.user_routes import UserUrl
UserUrl.get_user_routes(app)

from app.routes.mail_routes import CreatemessageUrl
CreatemessageUrl.get_messages_route(app)
