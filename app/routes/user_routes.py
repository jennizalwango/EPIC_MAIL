from app.views.user_veiws import RegisterUser

class UserUrl:
  @staticmethod
  def get_user_routes(app):
     # Register classes as views
    registration_view = RegisterUser.as_view('register')

    # Add rules for the api Endpoints
    app.add_url_rule('/api/v2/auth/signup', view_func=registration_view, methods=['POST', ])