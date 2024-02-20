from flask import Blueprint, jsonify, request, session
from routes import basic_auth, verify_token
from models.Users import User
from models.Roles import Role
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
from stores import db
from collections.abc import Mapping
import random
import smtplib, ssl
import os


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
        data = request.get_json()
        verify_token = random.randint(100000, 999999)
        hashed_password = generate_password_hash(data["password"])
        new_user = User(Password=hashed_password, Email=data["email"],RoleID=data["roleid"], IsVerified=verify_token)
        db.session.add(new_user)
        db.session.commit()
        ## Send user email for verification
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        sender_email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP(smtp_server,port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email,data["email"], f"Subject: Email Verification Code\n\nYour verification code is {verify_token}")
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            server.quit()
        
        return jsonify({"message": "User created successfully"}), 201
    
    except Exception as e:
        print(str(e))
        if "1062" in str(e):
            return jsonify({"error": "User already exists"}), 409
        else:
            return jsonify({"error": "Internal Server Error"}), 500
        
@users_bp.route('/verify', methods=['POST'])
def verify():
    try:
        data = request.get_json()
        user = User.query.filter_by(Email=data["email"], IsVerified=data["verification"]).first()
        if user:
            user.IsVerified = 1
            db.session.commit()
            return jsonify({"message": "User verified successfully"}), 200
        else:
            return jsonify({"error": "Invalid verification code"}), 401
    except Exception as e:
        print(str(e))
        return jsonify({"error": "Internal Server Error"}), 500