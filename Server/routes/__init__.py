from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


admin_auth = HTTPTokenAuth()
token_auth = HTTPTokenAuth()
    

@token_auth.verify_token
def verify_token(token):
    """
    Verify the authenticity of a token.

    Args:
        token (str): The token to be verified.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    try:
        jwt.decode(token, "secret", algorithms=["HS256"])
        return True
    except Exception:
        return False


@admin_auth.verify_token
def verify_status(token):
    """
    Verify if a user is an admin based on the token.

    Args:
        token (str): The token to be verified.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    try:
        decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
        if(decoded_token["RoleID"] == 1):
            return True
        else:
            return False
    except Exception:
        return False
        

        