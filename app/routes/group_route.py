from app.views.group_veiws import CreateGroup, UserGroup, GroupMails

class GroupUrl:
  @staticmethod
  def get_group_routes(app):
     # Create classes as views
    create_view = CreateGroup.as_view('create')
    group_view = UserGroup.as_view('user_group')
    group_mails_view = GroupMails.as_view('group_mails')

    # Add rules for the api Endpoints
    app.add_url_rule('/api/v2/groups', view_func=create_view, methods=['POST'])
    app.add_url_rule("/api/v2/groups", view_func=create_view, defaults={"group_id": None}, methods=["GET"])
    app.add_url_rule("/api/v2/groupnames", view_func=group_view, methods=["GET"])
    app.add_url_rule("/api/v2/groups/<group_id>/name", view_func=create_view, methods=["GET", "PUT"])
    app.add_url_rule("/api/v2/groups/<group_id>", view_func=create_view, methods=["DELETE"])
    app.add_url_rule("/api/v2/groups/<group_id>/users", view_func=group_view, methods=["POST"])
    app.add_url_rule("/api/v2/groups/<group_id>/messages", view_func=group_mails_view, methods=["POST"])
    app.add_url_rule("/api/v2/groups/<group_id>/users/<user_id>", view_func=group_view, methods=["DELETE"])