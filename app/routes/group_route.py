from app.views.group_veiws import CreateGroup

class GroupUrl:
  @staticmethod
  def get_group_routes(app):
     # Create classes as views
    create_view = CreateGroup.as_view('create')

    # Add rules for the api Endpoints
    app.add_url_rule('/api/v2/groups', view_func=create_view, methods=['POST',])
    app.add_url_rule("/api/v2/groups", view_func=create_view, defaults={"group_id": None}, methods=["GET",])
    app.add_url_rule("/api/v2/group/<group_id>", view_func=create_view, methods=["GET",])
    app.add_url_rule("/api/v2/groups/<group_id>", view_func=create_view, methods=["DELETE",])

  
