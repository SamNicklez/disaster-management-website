from flask import Blueprint, jsonify, request, session
from routes import basic_auth, verify_token
from models.Users import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
from stores import db
from collections.abc import Mapping


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
    
@users_bp.route('/signup', methods=['POST'])
def signup():
    try:
    # Users table
    # UserId: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Username: str = db.Column(db.String(45), nullable=False)
    # FirstName: str = db.Column(db.String(45), nullable=False)
    # LastName: str = db.Column(db.String(45), nullable=False)
    # email: str = db.Column(db.String(255), nullable=False)
    # PhoneNumber: int = db.Column(db.Integer)
    # Password: str = db.Column(db.String(255), nullable=False)
    # RoleID: int = db.Column(db.Integer, db.ForeignKey('roles.RoleID'))
    # IsVerified: int = db.Column(db.Integer)
    # ZipCode: int = db.Column(db.Integer, nullable=False)
        
    # Example Create 
    # new_item = Item(ItemName=data['ItemName'], CategoryId=data['CategoryId'], ItemDescription = data['ItemDescription'])
    # db.session.add(new_item)
    # db.session.commit()
    # return ('success')
    
    # except Exception as e:
    #     print(f"Error: {str(e)}")
    #     return jsonify({"error": "Internal Server Error"}), 500
        
        data = request.get_json()
        
        hashed_password = generate_password_hash(data["password"], method="sha256")
        new_user = User(UserID=data["UserID"], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": "User created successfully"}), 201
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500