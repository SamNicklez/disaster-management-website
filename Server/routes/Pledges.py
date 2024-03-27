from flask import Blueprint, jsonify, request
from stores import db
from models.Items import Item
from models.Pledges import Pledge
from routes import donor_auth, admin_auth
import jwt

pledges_bp = Blueprint('Pledges', __name__)

@pledges_bp.route('/createPledge', methods=['POST'])
@donor_auth.login_required
def pledge():
    """
    Create a new pledge for a specific item.

    Returns:
        A JSON response with a success message if the pledge is created successfully.
        A JSON response with an error message if there is an exception.
    """
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith('Bearer ') else None
        if token is None:
                return jsonify({"error": "User is not logged in"}), 401
        user_id = (jwt.decode(token, "secret", algorithms=["HS256"]))["id"]
        data = request.get_json()
        item_name = data['item_name']
        quantity = data['quantity']   
        item = Item.query.filter_by(ItemName=item_name).first()
        if item is None:
            return jsonify({'error': 'Item not found'}), 404
        new_pledge = Pledge(user_id=user_id, item_id=item.ItemID, quantity_given=quantity, quantity_remaining=quantity)
        db.session.add(new_pledge)
        db.session.commit()

        return jsonify({'message': 'Pledge created successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    
@pledges_bp.route('/getUserPledges', methods=['GET'])
@donor_auth.login_required
def getPledges():
    """
    Get all pledges made by the logged-in user.

    Returns:
        A JSON response with a list of pledges made by the user.
        A JSON response with an error message if there is an exception.
    """
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith('Bearer ') else None
        if token is None:
                return jsonify({"error": "User is not logged in"}), 401
        id = (jwt.decode(token, "secret", algorithms=["HS256"]))["id"]
        pledges = Pledge.query.filter_by(user_id=id).all()
        pledges = [pledge.to_dict() for pledge in pledges]
        for pledge in pledges:
            item = Item.query.filter_by(ItemID=pledge['item_id']).first()
            pledge['item_name'] = item.ItemName
        return jsonify(pledges), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@pledges_bp.route('/deletePledge', methods=['POST'])
@donor_auth.login_required
def deletePledge():
    """
    Delete a pledge made by the logged-in user.

    Returns:
        A JSON response with a success message if the pledge is deleted successfully.
        A JSON response with an error message if there is an exception.
    """
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith('Bearer ') else None
        if token is None:
                return jsonify({"error": "User is not logged in"}), 401
        id = (jwt.decode(token, "secret", algorithms=["HS256"]))["id"]
        data = request.get_json()
        pledge_id = data['pledge_id']
        pledge = Pledge.query.filter_by(pledge_id=pledge_id, user_id=id).first()
        if pledge is None:
            return jsonify({'error': 'Pledge not found'}), 404
        pledge.is_fulfilled = 1
        db.session.commit()
        return jsonify({'message': 'Pledge deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pledges_bp.route('/getAllPledges', methods=['GET'])
@admin_auth.login_required
def getAllPledges():
    """
    Get all pledges made by all users.

    Returns:
        A JSON response with a list of all pledges made by all users.
        A JSON response with an error message if there is an exception.
    """
    try:
        pledges = Pledge.query.filter_by(is_fulfilled=0).all()
        pledges = [pledge.to_dict() for pledge in pledges]
        for pledge in pledges:
            item = Item.query.filter_by(ItemID=pledge['item_id']).first()
            pledge['item_name'] = item.ItemName
        return jsonify(pledges), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500