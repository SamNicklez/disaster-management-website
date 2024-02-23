from flask import Blueprint, jsonify, request, session
from routes import token_auth
from models.Users import User
from models.Roles import Role
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
from stores import db
from collections.abc import Mapping
import datetime
import random
import smtplib, ssl
from email.message import EmailMessage
import os


users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/signin', methods=['POST'])
def signin():
    try:
        data = request.get_json()
        
        user = User.query.filter_by(Email=data["email"]).first()

        if user and user.IsVerified != 1:
            return jsonify({"error": "User not verified"}), 401
        elif user and check_password_hash(user.Password, data["password"]) and user.IsVerified == 1:
            encoded_token = jwt.encode({"id": user.UserId, "RoleID":user.RoleID, "DateCreated": datetime.today()}, "secret", algorithm="HS256")
            return jsonify({"token": encoded_token}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
    
@users_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        # verify_token = random.randint(100000, 999999)
        hashed_password = generate_password_hash(data["password"])
        new_user = User(Password=hashed_password, Email=data["email"],RoleID=data["roleid"], IsVerified=1)
        db.session.add(new_user)
        db.session.commit()
        ## Send user email for verification
        # smtp_server = "smtp.gmail.com"
        # port = 587  # For starttls
        # sender_email = os.getenv("EMAIL")
        # password = os.getenv("PASSWORD")
        # context = ssl.create_default_context()
        # try:
        #     server = smtplib.SMTP(smtp_server,port)
        #     server.ehlo()
        #     server.starttls(context=context)
        #     server.ehlo()
        #     server.login(sender_email, password)
        #     server.sendmail(sender_email,data["email"], f"Subject: Email Verification Code\n\nYour verification code is {verify_token}")
        # except Exception as e:
        #     print(f"Error: {str(e)}")
        #     return jsonify({"error": "Internal Server Error"}), 500
        # finally:
        #     server.quit()
        
        return jsonify({"message": "User created successfully"}), 201
    
    except Exception as e:
        print(str(e))
        if "Duplicate entry" in str(e):
            return jsonify({"error": "User already exists"}), 409
        else:
            print(f"Error: {str(e)}")
            return jsonify({"error": "Internal Server Error"}), 500


@users_bp.route('/verifyUser', methods=['POST'])
@token_auth.login_required
def verify():
    try:
        return jsonify({"message": "User verified successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500