from flask_httpauth import HTTPTokenAuth
from utils.FirebaseAPI import FirebaseAPI
from flask import g, Blueprint, render_template

fb_auth = HTTPTokenAuth(scheme="Bearer")
firebase_mock_service = Blueprint('/f', __name__)


@fb_auth.verify_token
def verify_token(token: str) -> bool:

    user_info = FirebaseAPI.verify_google_token(token)

    if user_info:
        g.current_user = user_info  # Setting the current user in Flask's global object
        return True
    else:
        return False


@fb_auth.error_handler
def unauthorized() -> tuple[str, int]:
    return "Unauthorized access", 401


# This is just for testing
@firebase_mock_service.route("/google")
def test_login_with_google() -> str:
    return render_template('google_login.html')
