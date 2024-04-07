from flask import Blueprint, jsonify, request
from stores import db
from models.Notification import Notification
from routes import admin_auth
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
        message = data.get('message')

        # Create and save the new notification
        new_notification = Notification(user_id=user_id, message=message)
        db.session.add(new_notification)
        db.session.commit()

        return jsonify({'message': 'Notification created successfully'}), 201
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
