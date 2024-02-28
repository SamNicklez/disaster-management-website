from flask import Blueprint, jsonify, request
from stores import db
from models.Items import Item
from models.Items import Category
from routes import admin_auth

items_bp = Blueprint('Items', __name__)

@items_bp.route('/CreateCategory', methods=['POST'])
def create_category():

    """
    Creates a new category with the name provided in the request JSON.
    Requires a JSON body with 'CategoryName'.
    
    Returns:
        - Success message with status code 201 if the category is created successfully.
        - Error message with status code 500 if there is an internal server error.
    """
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

    """
    Retrieves items filtered by the 'CategoryId' parameter from the query string.
    
    Parameters:
        - CategoryId (query parameter): The ID of the category to filter items by.
    
    Returns:
        - A JSON list of items belonging to the specified category, with status code 200.
        - Error message with status code 400 if 'CategoryId' parameter is missing.
        - Error message with status code 500 if there is an internal server error.
    """

    CategoryName = request.args.get('CategoryName', None)

    if CategoryName is None:
        return jsonify({"error": "CategoryName parameter is required"}), 400
    
    try:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        cursor.callproc('GetItemsByCategory', [CategoryName])
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


@items_bp.route('/DeleteCategory', methods=['POST'])
def delete_category():
    
    """
    Deletes a category specified by 'CategoryName' in the request JSON. Marks category as inactive.
    Requires a JSON body with 'CategoryName'.
    
    Returns
        - Success message if the category is deleted successfully.
        - Error message with status code 400 if 'CategoryName' is missing.
        - Error message with status code 404 if the category is not found.
        - Error message with status code 500 if there is a database error.
    """

    data = request.json

    if 'CategoryName' not in data:
        return jsonify({'error': 'CategoryName is required'}), 400
    
    CategoryName = data['CategoryName']
    try:
        category = Category.query.filter_by(CategoryName=CategoryName).first()
    
        if not category:
            return jsonify({'error': 'Category not found'}), 404
    
        category.isActive = -1

        items = Item.query.filter_by(CategoryId=category.CategoryId).all()
        for item in items:
            item.isActive = -1

        db.session.commit()

        return jsonify({'message': 'Category deleted successfully'})
    except db.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deleting the category'}), 500

@items_bp.route('/DeleteItem', methods=['POST'])
def delete_item():

    """
    Deletes an item specified by 'ItemName' in the request JSON. Marks the item as inactive.
    Requires a JSON body with 'ItemName'.
    
    Returns:
        - Success message if the item is deleted successfully.
        - Error message with status code 400 if 'ItemName' is missing.
        - Error message with status code 404 if the item is not found.
        - Error message with status code 500 if there is a database error.
    """

    data = request.json

    if 'ItemName' not in data:
        return jsonify({'error': 'ItemName is required'}), 400
    
    ItemName = data['ItemName']

    try:
        item = Item.query.filter_by(ItemName=ItemName).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404
        item.isActive = -1
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    
    except db.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deleting the item'}), 500

@items_bp.route('/EditCategory', methods=['POST'])
def edit_category():

    """
    Edits the name of an existing category. Requires JSON body with 'CategoryName' and 'NewCategoryName'.
    
    Returns:
        - Success message if the category name is updated successfully.
        - Error message with status code 400 if required data is missing.
        - Error message with status code 404 if the category is not found.
        - Error message with status code 500 if there is a database error.
    """

    data = request.json

    if 'CategoryName' not in data or 'NewCategoryName' not in data:
        return jsonify({'error': 'Category Name and new name are required'}), 400

    CategoryName = data['CategoryName']
    NewCategoryName = data['NewCategoryName']

    try:
        category = Category.query.filter_by(CategoryName=CategoryName).first()
        if not category:
            return jsonify({'error': 'Category not found'}), 404

        category.CategoryName = NewCategoryName
        db.session.commit()

        return jsonify({'message': 'Category name updated successfully'})
    
    except db.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while updating the category name'}), 500
    

@items_bp.route('/EditItem', methods=['POST'])
def edit_item():

    """
    Edits details of an existing item. Can update the item's name, description, and category ID.
    Requires JSON body with 'ItemName' and optionally 'NewName', 'NewDescription', 'NewCategoryId'.
    
    Returns:
        - Success message if the item details are updated successfully.
        - Error message with status code 400 if 'ItemName' is missing.
        - Error message with status code 404 if the item is not found.
        - Error message with status code 500 if there is a database error.
    """

    data = request.json

    if 'ItemName' not in data:
        return jsonify({'error': 'ItemName is required'}), 400

    ItemName = data['ItemName']
    category = Category.query.filter_by(CategoryName = data['CategoryName']).first()
    try:
        item = Item.query.filter_by(ItemName=ItemName).first()
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        if 'NewName' in data:
            item.ItemName = data['NewName']
        
        if 'NewDescription' in data:
            item.ItemDescription = data['NewDescription']
        
        if 'CategoryName' in data:
            item.CategoryId = category.CategoryId

        db.session.commit()

        return jsonify({'message': 'Item updated successfully'})
    
    except db.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while updating the item'}), 500