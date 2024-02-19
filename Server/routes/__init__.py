from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


allowed_users = {
    "admin": generate_password_hash("password")
}
allowed_tokens = {
    "token-admin": "admin"
}


@basic_auth.verify_password
def verify_password(username, password):
    if username not in allowed_users:
        return None
    
    if check_password_hash(allowed_users[username], password):
        return username
    
    
@token_auth.verify_token
def verify_token(token):
    try:
        decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
        print(decoded_token)
    except Exception as e:
        return None
    
    # if decoded_token["username"] in allowed_users:
    #     return decoded_token["username"]
    return decoded_token
        
        

        