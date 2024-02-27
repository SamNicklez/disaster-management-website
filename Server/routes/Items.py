from flask import Blueprint, jsonify, request
from stores import db
from models.Items import Item
from models.Items import Category
from routes import admin_auth

items_bp = Blueprint('Items', __name__)

@items_bp.route('/CreateItem', methods=['POST'])
@admin_auth.login_required
def create_item():
    """
    Create a new item.

    Inputs:
    - JSON data containing the following fields:
        - 'CategoryName': Name of the category the item belongs to
        - 'ItemName': Name of the item
        - 'ItemDescription': Description of the item

    Outputs:
    - If successful, returns 'success'
    - If the item already exists, returns an error message and status code 400
    - If an internal server error occurs, returns an error message and status code 500
    """
    try:
        data = request.get_json()
        print(data)
        category = Category.query.filter_by(CategoryName=data['CategoryName']).first()
        item = Item.query.filter_by(ItemName=data['ItemName']).first()
        if item:
            return jsonify({"error": "Item already exists"}), 400
        if not category:
                new_category = Category(CategoryName=data['CategoryName'])
                db.session.add(new_category)
                db.session.commit()
                category = Category.query.filter_by(CategoryName=data['CategoryName']).first()

        new_item = Item(ItemName=data['ItemName'], CategoryId=category.CategoryId, ItemDescription=data['ItemDescription'])
        db.session.add(new_item)
        db.session.commit()
        return ('success')
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    
@items_bp.route('/GetCategories', methods=['GET'])
@admin_auth.login_required
def get_categories():
    """
    Get all categories.

    Inputs: None

    Outputs:
    - If successful, returns a JSON list of categories with their IDs and names, and status code 200
    - If an internal server error occurs, returns an error message and status code 500
    """
    try:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.callproc('GetAllCategories')
        categories = cursor.fetchall()
        cursor.close() 
        conn.close()
        categories_list = [{'CategoryId': category[0], 'CategoryName': category[1]} for category in categories]
        return jsonify(categories_list), 200
    
    except Exception as e:
        print("error")
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


@items_bp.route('/GetItems', methods=['GET'])
@admin_auth.login_required
def get_items():
    """
    Get items by category.

    Inputs:
    - Query parameter 'CategoryId': ID of the category to filter items by

    Outputs:
    - If successful, returns a JSON list of items with their IDs, names, category IDs, and descriptions, and status code 200
    - If the 'CategoryId' parameter is missing, returns an error message and status code 400
    - If an internal server error occurs, returns an error message and status code 500
    """
    CategoryId = request.args.get('CategoryId', None)

    if CategoryId is None:
        return jsonify({"error": "CategoryId parameter is required"}), 400
    
    try:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.callproc('GetItemsByCategory', [CategoryId])
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        items_list = [{'ItemId': item[0], 'ItemName': item[1], 'CategoryId': item[2], 'ItemDescription': item[3]} for item in items]
        return jsonify(items_list), 200
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
    
@items_bp.route('/GetAllItems', methods=['GET'])
@admin_auth.login_required
def get_all_items():    
    """
    Get all items with their corresponding category names.

    Inputs: None

    Outputs:
    - If successful, returns a JSON list of items with their names, category names, and descriptions, and status code 200
    - If an internal server error occurs, returns an error message and status code 500
    """
    try:
        items = db.session.query(Item, Category.CategoryName).join(Category, Item.CategoryId == Category.CategoryId).all()
        items_list = [{'name': item.ItemName, 'category': category_name, 'description': item.ItemDescription} for item, category_name in items]
        return jsonify(items_list), 200
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
