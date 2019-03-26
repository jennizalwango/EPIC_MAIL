from app.views.user_veiws import SignupUser

class UserUrl:
  @staticmethod
  def get_user_routes(app):
    register_user_view = SignupUser.as_view("create_user") 
    app.add_url_rule("/api/v2/auth/signup", view_func= register_user_view, methods=["POST"])
