
from resources.user_view_list import UserViewList
from resources.user_view_new import UserViewNew

def init_app(app):
    """Init app."""
    
    """Route for endpoint users."""
    user_view_list = UserViewList.as_view('user_view_list')
    app.add_url_rule(
        rule='/users',
        view_func=user_view_list,
        methods=['GET']
    )

    """Route for endpoint users."""
    user_view_new = UserViewNew.as_view('user_view_new')
    app.add_url_rule(
        rule='/user',
        view_func=user_view_new,
        methods=['POST']
    )