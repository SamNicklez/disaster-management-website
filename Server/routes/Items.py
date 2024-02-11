from flask import Blueprint, jsonify, request
from stores import db
from models.Items import Item
from models.Items import Category

items_bp = Blueprint('Items', __name__)

@items_bp.route('/CreateCategory', methods=['POST'])
def create_category():
    try:
        data = request.get_json() 
        new_category = Category(CategoryName=data['CategoryName'])
        db.session.add(new_category)
        db.session.commit()
        return jsonify('success'), 201

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
    

@items_bp.route('/CreateItem', methods=['POST'])
def create_item():
    try:
        data = request.get_json()
        new_item = Item(ItemName=data['ItemName'], CategoryId=data['CategoryId'], ItemDescription = data['ItemDescription'])
        db.session.add(new_item)
        db.session.commit()
        return ('success')
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    
@items_bp.route('/GetCategories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        categories_list = [{'CategoryId': category.CategoryId, 'CategoryName': category.CategoryName} for category in categories]
        return jsonify(categories_list), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


@items_bp.route('/GetItems', methods=['GET'])
def get_items():
    category_id = request.args.get('CategoryId', None)

    if category_id is None:
        return jsonify({"error": "CategoryId parameter is required"}), 400 

    try:
        items = Item.query.filter_by(CategoryId=category_id).all()
        items_list = [{'ItemId': item.ItemID, 'ItemName': item.ItemName, 'ItemDescription': item.ItemDescription, 'CategoryId': item.CategoryId} for item in items]
        return jsonify(items_list), 200
    
    except Exception as e:
        print(f"Error occured ")
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


