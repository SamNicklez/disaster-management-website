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
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith('Bearer ') else None
        if token is None:
                return jsonify({"error": "User is not logged in"}), 401
        user_id = (jwt.decode(token, "secret", algorithms=["HS256"]))["user_id"]
        data = request.get_json()
        item_name = data['item_name']
        quantity = data['quantity']   
        item = Item.query.filter_by(item_name=item_name).first()
        if item is None:
            return jsonify({'error': 'Item not found'}), 404
        new_pledge = Pledge(user_id=user_id, item_id=item.item_id, quantity_given=quantity)
        db.session.add(new_pledge)
        db.session.commit()

        return jsonify({'message': 'Pledge created successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@pledges_bp.route('/getPledges', methods=['GET'])
@donor_auth.login_required
def getPledges():
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(" ")[1] if auth_header and auth_header.startswith('Bearer ') else None
        if token is None:
                return jsonify({"error": "User is not logged in"}), 401
        user_id = (jwt.decode(token, "secret", algorithms=["HS256"]))["user_id"]
        pledges = Pledge.query.filter_by(user_id=user_id).all()
        return jsonify([pledge.to_dict() for pledge in pledges]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500