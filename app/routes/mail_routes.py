from app.views.mail_views import CreateMail


class CreatemessageUrl:
    @staticmethod
    def get_messages_route(app):
        create_meassage_view = CreateMail.as_view("create")
        app.add_url_rule("/api/v1/messages",
                         view_func=create_meassage_view, methods=["POST", ])
        app.add_url_rule("/api/v1/messages", view_func=create_meassage_view,
                         defaults={'data': None}, methods=["GET", ])
        app.add_url_rule("/api/v1/messages/<data>",
                         view_func=create_meassage_view,  methods=["GET", "DELETE"])
