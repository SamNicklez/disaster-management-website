from flask import Blueprint, jsonify, request
from stores import db
from models.Items import Item
from models.Items import Category
from routes import admin_auth

items_bp = Blueprint('Items', __name__)

@items_bp.route('/CreateCategory', methods=['POST'])
@admin_auth.login_required
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
@admin_auth.login_required
def create_item():
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
def get_categoriess():
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
def get_itemsNew():
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
    

