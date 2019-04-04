from app.views.mail_veiws import MessageViews

class MessageUrls:
  @staticmethod
  def get_mail_routes(app):
     # Register classes as views
    message_view = MessageViews.as_view('messages')
    
    # Add rules for the api Endpoints
    app.add_url_rule('/api/v2/messages', view_func=message_view, 
    methods=['POST', ])
    app.add_url_rule('/api/v2/messages', view_func=message_view, 
    defaults={'data':None}, methods=['GET', ])
    app.add_url_rule('/api/v2/messages/<data>', view_func=message_view, 
    methods=['DELETE', 'GET' ])
  