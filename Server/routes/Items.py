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
    
@items_bp.route('/DeleteCategory', methods=['POST'])
def delete_category():
    
    data = request.json

    if 'CategoryId' not in data:
        return jsonify({'error': 'CategoryId is required'}), 400
    
    CategoryId = data['CategoryId']
    try:
        category = Category.query.filter_by(CategoryId=CategoryId).first()
    
        if not category:
            return jsonify({'error': 'Category not found'}), 404
    
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'})
    except db.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deleting the category'}), 500

@items_bp.route('/DeleteItem', methods=['POST'])
def delete_item():
    data = request.json

    if 'ItemId' not in data:
        return jsonify({'error': 'ItemId is required'}), 400
    
    ItemId = data['ItemId']

    try:
        item = Item.query.filter_by(ItemID=ItemId).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    
    except db.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deleting the item'}), 500

@items_bp.route('/EditCategory', methods=['POST'])
def edit_category():
    data = request.json

    if 'category_id' not in data or 'new_name' not in data:
        return jsonify({'error': 'Category ID and new name are required'}), 400

    category_id = data['category_id']
    new_name = data['new_name']

    try:
        category = Category.query.filter_by(CategoryId=category_id).first()
        if not category:
            return jsonify({'error': 'Category not found'}), 404

        category.CategoryName = new_name
        db.session.commit()

        return jsonify({'message': 'Category name updated successfully'})
    
    except db.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while updating the category name'}), 500
    

@items_bp.route('/EditItem', methods=['POST'])
def edit_item():
    data = request.json

    if 'item_id' not in data:
        return jsonify({'error': 'Item ID is required'}), 400

    item_id = data['item_id']

    try:
        item = Item.query.filter_by(ItemID=item_id).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        if 'new_name' in data:
            item.ItemName = data['new_name']
        
        if 'new_description' in data:
            item.ItemDescription = data['new_description']
        
        if 'new_category_id' in data:
            item.CategoryId = data['new_category_id']

        db.session.commit()

        return jsonify({'message': 'Item updated successfully'})
    
    except db.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while updating the item'}), 500