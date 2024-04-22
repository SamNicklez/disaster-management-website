from flask import Blueprint, jsonify, request
from stores import db
from models.Notification import Notification
from routes import admin_auth
import jwt

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/create', methods=['POST'])
@admin_auth.login_required
def create_notification():
    """
    Create a new notification for a specific user. Only accessible by admins.

    Inputs:
    - JWT Token in the Authorization header with admin privileges
    - JSON data containing the following fields:
        - 'user_id': ID of the user to whom the notification is sent
        - 'message': Content of the notification

    Outputs:
    - If successful, returns 'success' message with status code 201
    - If the JWT token does not indicate admin privileges, returns an error message and status code 403
    - If an internal server error occurs, returns an error message and status code 500
    """
    try:
        
        data = request.get_json()
        user_id = data.get('user_id')
        title = data.get('title')
        message = data.get('message')

        # Create and save the new notification
        new_notification = Notification(user_id=user_id, message=message, title=title)
        db.session.add(new_notification)
        db.session.commit()

        return jsonify({'message': 'Notification created successfully'}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@notification_bp.route('/get', methods=['GET'])
def get_notifications():
    """
    Get all notifications for the logged-in user.

    Returns:
        A JSON response with a list of notifications for the user.
        A JSON response with an error message if there is an exception.
    """
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith('Bearer ') else None
        if token is None:
            return jsonify({"error": "User is not logged in"}), 401
        
        user_id = jwt.decode(token, "secret", algorithms=["HS256"])["id"]
        notifications = Notification.query.filter_by(user_id=user_id).all()
        
        
        return jsonify([notification.to_dict() for notification in notifications]), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@notification_bp.route('/viewUnread', methods=['GET'])
def get_unread_notifications():
    """
    Get all unread notifications for the logged-in user.

    Returns:
        A JSON response with a list of unread notifications for the user.
        A JSON response with an error message if there is an exception.
    """
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith('Bearer ') else None
        
        if token is None:
            return jsonify({"error": "Authorization token is missing"}), 401
        
        # Assuming 'your_secret_key' is your actual secret key used for encoding the JWT tokens
        user_id = jwt.decode(token, "secret", algorithms=["HS256"])["id"]
        
        unread_notifications = Notification.query.filter_by(user_id=user_id, is_dismissed=False).all()   
        
        return jsonify([notification.to_dict() for notification in unread_notifications]), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching notifications'}), 500

@notification_bp.route('/markRead/<int:notification_id>', methods=['POST'])
def mark_notification_as_read(notification_id):
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith('Bearer ') else None
       
        if token is None:
            return jsonify({"error": "User is not logged in"}), 401
        
        user_id = jwt.decode(token, "secret", algorithms=["HS256"])["id"]
        # Find and update the notification
        notification = Notification.query.filter_by(user_id=user_id, notification_id=notification_id).first()
        if not notification:
            return jsonify({"error": "Notification not found"}), 404

        notification.is_dismissed = True
        db.session.commit()

        return jsonify({"message": "Notification marked as read"}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred: " + str(e)}), 500
