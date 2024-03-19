from flask import Blueprint, jsonify, request, session
from routes import token_auth
from routes import admin_auth
from models.Users import User
from models.Roles import Role
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
from stores import db
from collections.abc import Mapping
from datetime import datetime
import random
import smtplib, ssl
from email.message import EmailMessage
import os


users_bp = Blueprint('users_bp', __name__)


@users_bp.route('/signin', methods=['POST'])
def signin():
    """
    Sign in a user.

    Inputs:
    - data: JSON object containing the user's email and password.

    Outputs:
    - If the user is verified and the password is correct, returns a JSON object containing a token.
    - If the user is not verified, returns a JSON object with an error message.
    - If the email or password is invalid, returns a JSON object with an error message.
    - If there is an internal server error, returns a JSON object with an error message.
    """
    try:
        data = request.get_json()
        
        user = User.query.filter_by(Email=data["email"]).first()

        if user and user.IsVerified != 1:
            return jsonify({"error": "User not verified"}), 405
        elif user and check_password_hash(user.Password, data["password"]) and user.IsVerified == 1:
            encoded_token = jwt.encode({"id": user.UserId, "RoleID":user.RoleID, "DateCreated": datetime.now().isoformat()}, "secret", algorithm="HS256")
            return jsonify({"token": encoded_token}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
    
@users_bp.route('/signup', methods=['POST'])
def signup():
    """
    Sign up a new user.

    Inputs:
    - data: JSON object containing the user's email, password, and role ID.

    Outputs:
    - If the user is created successfully, returns a JSON object with a success message.
    - If the user already exists, returns a JSON object with an error message.
    - If there is an internal server error, returns a JSON object with an error message.
    """
    try:
        data = request.get_json()
        verify_token = random.randint(100000, 999999)
        hashed_password = generate_password_hash(data["password"])
        new_user = User(Password=hashed_password, Email=data["email"],RoleID=data["roleid"], IsVerified=verify_token)
        db.session.add(new_user)
        db.session.commit()
        # Send user email for verification
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
            print(f"Error: {str(e)}")
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            server.quit()
        
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
def verifyUser():
    """
    Verify a user.

    Outputs:
    - If the user is verified successfully, returns a JSON object with a success message.
    - If there is an internal server error, returns a JSON object with an error message.
    """
    
    try:
        return jsonify({"message": "User verified successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    
@users_bp.route('/verifyAdmin', methods=['POST'])
@admin_auth.login_required
def verifyAdmin():
    """
    Verify an admin user.

    Outputs:
    - If the admin user is verified successfully, returns a JSON object with a success message.
    - If there is an internal server error, returns a JSON object with an error message.
    """
    try:
        return jsonify({"message": "User verified successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    
@users_bp.route('/verify', methods=['POST'])
def verify():
    """
    Verify a user using a verification code.

    Inputs:
    - data: JSON object containing the user's email and verification code.

    Outputs:
    - If the verification code is valid, updates the user's verification status and returns a JSON object with a success message.
    - If the verification code is invalid, returns a JSON object with an error message.
    - If there is an internal server error, returns a JSON object with an error message.
    """
    try:
        data = request.get_json()
        user = User.query.filter_by(Email=data["email"]).first()
        if user.IsVerified == data["verification"]:
            user.IsVerified = 1
            db.session.commit()
            return jsonify({"message": "User verified successfully"}), 200
        else:
            return jsonify({"error": "Invalid verification code"}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
@users_bp.route('/editProfile', methods=['POST'])
def editProfile():
    """
    Edit a user's profile based on the provided fields.
    """
    auth_header = request.headers.get('Authorization')
    token = token = auth_header.split(" ")[1] if auth_header and auth_header.startswith('Bearer ') else None

    if token is None:
            return jsonify({"error": "User is not logged in"}), 401    
    try:
        decoded = jwt.decode(token, "secret", algorithms=["HS256"])
        data = request.get_json()
        
        user = User.query.filter_by(UserId = decoded["id"]).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404


        if 'phone_number' in data:
            user.PhoneNumber = data['phone_number']
        if 'address' in data:
            user.Address = data['address'] + ' ' + data['addressLine2']
        if 'city' in data:
            user.City = data['city']
        if 'state' in data:
            user.State = data['state']
        if 'zipcode' in data:
            user.ZipCode = data['zipcode']
        
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
@users_bp.route('/getProfile', methods=['GET'])
def getProfile():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[1] if auth_header and auth_header.startswith('Bearer ') else None
    # role_name = ""
    # if user.role == 1:
    #     role_name = "Admin"
    # elif user.role == 2:
    #     role_name = "Donor"
    # elif user.role == 3:
    #     role_name = "Recipient"
    # else:
    #     return jsonify({"error": f"Invalid Role"}), 500

    if token is None:
        return jsonify({"error": "User is not logged in"}), 401

    try:
        decoded = jwt.decode(token, "secret", algorithms=["HS256"])
        user = User.query.filter_by(UserId=decoded["id"]).first()
        role_name = Role.query.filter_by(RoleID=decoded["RoleID"]).first()
        print(role_name)

        if not user:
            return jsonify({"error": "User not found"}), 404
        


        user_data = {
            # "username": user.Username,
            "email": user.Email,
            "role": role_name,
            "phone_number": user.PhoneNumber,
            "address": user.Address,
            "city": user.City,
            "state": user.State,
            "zipcode": user.ZipCode
        }

        return jsonify(user_data), 200

    except Exception as e:
        print(str(e))
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500
