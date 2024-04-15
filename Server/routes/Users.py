from flask import Blueprint, jsonify, request, session
from routes import token_auth, admin_auth, donor_auth, recipient_auth
from models.Users import User
from models.Roles import Role
from werkzeug.security import generate_password_hash, check_password_hash
from stores import db
from datetime import datetime
import string,ssl,os,smtplib,random,jwt


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
            encoded_token = jwt.encode({"id": user.UserId, "RoleID": user.RoleID, "DateCreated": datetime.now(
            ).isoformat()}, "secret", algorithm="HS256")
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
        new_user = User(Password=hashed_password,
                        Email=data["email"], RoleID=data["roleid"], IsVerified=verify_token)
        db.session.add(new_user)
        db.session.commit()
        # Send user email for verification
        smtp_server = "smtp.gmail.com"

        port = 587  # For starttls
        sender_email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(
                sender_email, data["email"], f"Subject: Email Verification Code\n\nYour verification code is {verify_token}")
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


@users_bp.route('/verifyDonor', methods=['POST'])
@donor_auth.login_required
def verifyDonor():
    """
    Verify a donor user.

    Outputs:
    - If the donor user is verified successfully, returns a JSON object with a success message.
    - If there is an internal server error, returns a JSON object with an error message.
    """
    try:
        return jsonify({"message": "User verified successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500


@users_bp.route('/verifyRecipient', methods=['POST'])
@recipient_auth.login_required
def verifyRecipient():
    """
    Verify a donor user.

    Outputs:
    - If the donor user is verified successfully, returns a JSON object with a success message.
    - If there is an internal server error, returns a JSON object with an error message.
    """
    try:
        return jsonify({"message": "User verified successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500


@users_bp.route('/editProfile', methods=['POST'])
@token_auth.login_required
def editProfile():
    """
    Edit a user's profile based on the provided fields.
    """
    auth_header = request.headers.get('Authorization')
    token = token = auth_header.split(
        " ")[1] if auth_header and auth_header.startswith('Bearer ') else None

    if token is None:
        return jsonify({"error": "User is not logged in"}), 401
    try:
        decoded = jwt.decode(token, "secret", algorithms=["HS256"])
        data = request.get_json()

        user = User.query.filter_by(UserId=decoded["id"]).first()

        if not user:
            return jsonify({"error": "User not found"}), 404
        if 'address' in data and data['address'] != '':
            address = data.get('address', '')
            addressLine2 = data.get('addressLine2', '')
            user.Address = data['address'] + ' ' + \
                data['addressLine2'] if addressLine2 else address
        if 'city' in data and data['city'] != '':
            user.City = data['city']
        if 'state' in data and data['state'] != '':
            user.State = data['state']
        if 'zipcode' in data and data['zipcode'] != '':
            user.ZipCode = data['zipcode']
        if 'latitude' in data and data['latitude'] != '':
            user.Latitude = data['latitude']
        if 'longitude' in data and data['longitude'] != '':
            user.Longitude = data['longitude']

        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@users_bp.route('/getProfile', methods=['GET'])
@token_auth.login_required
def getProfile():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(
        " ")[1] if auth_header and auth_header.startswith('Bearer ') else None
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

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_data = {
            # "username": user.Username,
            "email": user.Email,
            "role": role_name.Name,
            "phone_number": user.PhoneNumber,
            "address": user.Address,
            "city": user.City,
            "state": user.State,
            "zipcode": user.ZipCode
        }

        return jsonify(user_data), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@users_bp.route('/getRole', methods=['GET'])
@token_auth.login_required
def getRole():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(
        " ")[1] if auth_header and auth_header.startswith('Bearer ') else None
    if token is None:
        return jsonify({"error": "User is not logged in"}), 401

    try:
        decoded = jwt.decode(token, "secret", algorithms=["HS256"])
        role = Role.query.filter_by(RoleID=decoded["RoleID"]).first()
        if not role:
            return jsonify({"error": "Role not found"}), 404

        role_data = {
            "role": role.Name
        }

        return jsonify(role_data), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@users_bp.route('/passwordreset', methods=['POST'])
@token_auth.login_required
def passwordReset():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(
        " ")[1] if auth_header and auth_header.startswith('Bearer ') else None
    if token is None:
        return jsonify({"error": "User is not logged in"}), 401
    try:
        user_id = jwt.decode(token, "secret", algorithms=["HS256"])["id"]
        data = request.get_json()
        current_user = User.query.filter_by(UserId=user_id).first()
        if current_user and check_password_hash(current_user.Password, data["old_password"]):
            hashed_new_password = generate_password_hash(data["new_password"])
            current_user.Password = hashed_new_password
            db.session.commit()
            return jsonify({"message": "Password updated successfully"}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


@users_bp.route('/sendforgotpasswordemail', methods=['POST'])
def forgotPassword():
    try:
        data = request.get_json()
        user = User.query.filter_by(Email=data["email"]).first()
        if not user:
            return jsonify({"message": "If a account with this email exists, a code was sent to your email"}), 201

        verify_token = random.randint(100000, 999999)
        # Send user email for verification
        smtp_server = "smtp.gmail.com"

        port = 587  # For starttls
        sender_email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        context = ssl.create_default_context()
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(
            sender_email, data["email"], f"Subject: Password Reset\n\nYour verification code is {verify_token}")
            user.verify_code = verify_token
            db.session.commit()
        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            server.quit()

        return jsonify({"message": "If a account with this email exists, a code was sent to your email"}), 201

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


@users_bp.route('/verifyforgotpassword', methods=['POST'])
def verifyForgotPassword():
    try:
        data = request.get_json()
        user = User.query.filter_by(Email=data["email"]).first()
        if not user:
            return jsonify({"error": "Code or Email is incorrect, please try again"}), 500
        if user.verify_code == data["code"]:
            password_characters_no_special = string.ascii_letters + string.digits
            password_no_special = ''.join(random.choice(password_characters_no_special) for i in range(10))
            hashed_password = generate_password_hash(password_no_special)
            user.Password = hashed_password
            smtp_server = "smtp.gmail.com"

            port = 587
            sender_email = os.getenv("EMAIL")
            password = os.getenv("PASSWORD")
            context = ssl.create_default_context()
            try:
                server = smtplib.SMTP(smtp_server, port)
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(sender_email, password)
                server.sendmail(
                sender_email, data["email"], f"Subject: Password Reset\n\nWe have issued a new password for your account: {password_no_special}, please login and change it immediately.")
                db.session.commit()
            except Exception as e:
                print(f"Error: {str(e)}")
                return jsonify({"error": "Internal Server Error"}), 500
            finally:
                server.quit()
            return jsonify({"message": "Your password has been upated, please check your email for details"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500