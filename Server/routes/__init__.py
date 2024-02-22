from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from models.Users import User
from models.Roles import Role


admin_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
    

# Basic auth that tells if a user is signed in or not
@token_auth.verify_token
def verify_token(token):
    try:
        jwt.decode(token, "secret", algorithms=["HS256"])
        return True
    except Exception as e:
        return False

@admin_auth.verify_password
def verify_status(token):
    try:
        decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
        user = User.query(User.UserId, Role.Name).join(Role, User.RoleID == decoded_token['RoleID']).filter(User.UserId == decoded_token['id']).first()
        print(user)
    except Exception as e:
        return False
        

        