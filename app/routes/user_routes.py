from app.views.user_views import CreateUser
from app.views.user_views import LoginUser


class UserUrl:
  @staticmethod
  def get_user_routes(app):
    register_user_view = CreateUser.as_view("register")
    login_user_view = LoginUser.as_view("log_in_user")
    app.add_url_rule("/auth/signup", view_func= register_user_view, methods=["POST",])
    app.add_url_rule("/auth/login", view_func=login_user_view, methods=["POST",])
  