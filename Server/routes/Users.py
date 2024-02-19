from flask import Blueprint, jsonify, request, session
from routes import basic_auth, verify_token
from models.Users import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
from stores import db
from collections import Mapping


users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()
        if "UserID" not in data or "password" not in data:
            return jsonify({"error": "Missing user ID or password"}), 400
        
        user = User.query.filter_by(UserID=data["UserID"], IsVerified=1).first()
        
        if user and check_password_hash(user.password, data["password"]):
            encoded_token = jwt.encode({"id": user.UserId, "RoleID":user.RoleID}, "secret", algorithm="HS256")
            session["token"]=encoded_token
            return jsonify({"token": encoded_token}), 200
        else:
            return jsonify({"error": "Invalid voter ID or password"}), 401
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500