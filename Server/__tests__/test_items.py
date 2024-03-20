import pytest
from flask import Flask, jsonify
from routes.Items import items_bp
from models.Items import Item, Category
from stores import db
from datetime import datetime
import jwt
import os

token = jwt.encode({"id": 1, "RoleID": 1, "DateCreated": datetime.now().isoformat()}, "secret", algorithm="HS256")
headers = {
        'Authorization': f'Bearer {token}'
    }

# Create a test client
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(items_bp)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{os.getenv("DB_PASSWORD")}@localhost:3306/theapp'
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.query(Item).delete()
        db.session.query(Category).delete()
        db.session.commit()
    return app.test_client()

# Test case for creating a new item
def test_create_item(app):
    data = {"CategoryName": "Category 1", "ItemName": "Item 2", "ItemDescription": "Description 1"}
    response = app.post("/CreateItem", json=data, headers=headers)
    assert response.status_code == 200
    assert response.data == b"success"

# Test case for creating a duplicate item
def test_create_duplicate_item(app):
    data = {"CategoryName": "Category 1", "ItemName": "Item 1", "ItemDescription": "Description 1"}
    app.post("/CreateItem", json=data, headers=headers)
    response = app.post("/CreateItem", json=data, headers=headers)
    assert response.status_code == 405
    assert response.json["error"] == "Item already exists"

# Test case for getting categories
def test_get_categories(app):
    category1 = Category(CategoryName="Category 1")
    category2 = Category(CategoryName="Category 2")
    db.session.add(category1)
    db.session.add(category2)
    db.session.commit()

    response = app.get("/GetCategories", headers=headers)
    assert response.status_code == 200
    assert len(response.json) == 2
    assert {"CategoryId": category1.CategoryId, "CategoryName": "Category 1"} in response.json
    assert {"CategoryId": category2.CategoryId, "CategoryName": "Category 2"} in response.json

# # Test case for getting items by category
def test_get_items_by_category(app):
    category1 = Category(CategoryName="Category 1")
    db.session.add(category1)
    db.session.commit()
    item1 = Item(ItemName="Item 1", CategoryId=category1.CategoryId, ItemDescription="Description 1")
    item2 = Item(ItemName="Item 2", CategoryId=category1.CategoryId, ItemDescription="Description 2")
    db.session.add(item1)
    db.session.add(item2)
    db.session.commit()
    response = app.get(f"/GetItems?CategoryName={category1.CategoryId}", headers=headers)
    assert response.status_code == 200
    assert len(response.json) == 2
    print(response.json)

# # Test case for getting all items
def test_get_all_items(app):
    category1 = Category(CategoryName="Category 1")
    category2 = Category(CategoryName="Category 2")
    db.session.add(category1)
    db.session.add(category2)
    db.session.commit()

    item1 = Item(ItemName="Item 1", CategoryId=category1.CategoryId, ItemDescription="Description 1")
    item2 = Item(ItemName="Item 2", CategoryId=category2.CategoryId, ItemDescription="Description 2")
    db.session.add(item1)
    db.session.add(item2)
    db.session.commit()

    response = app.get("/GetAllItems", headers=headers)
    assert response.status_code == 200
    assert len(response.json) == 2
