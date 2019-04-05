from app.views.user_veiws import RegisterUser, LoginUser

class UserUrl:
  @staticmethod
  def get_user_routes(app):
    # Register classes as views
    registration_view = RegisterUser.as_view('register')
    login_view = LoginUser.as_view('login')

    # Add rules for the api Endpoints
    app.add_url_rule('/api/v2/auth/signup', view_func=registration_view, 
    methods=['POST', ])
    app.add_url_rule('/api/v2/auth/login', view_func=login_view, 
    methods=['POST', ])
    app.add_url_rule('/api/v2/users', view_func=login_view, 
    methods=['GET', ])