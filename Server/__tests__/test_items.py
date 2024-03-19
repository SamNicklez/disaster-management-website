
import pytest
from flask import Flask, jsonify
from routes import items_bp
from models.Items import Item, Category
from stores import db
import os
import sys
sys.path.append('/Users/deepikamitta/PycharmProjects/software-engineering-project-team-3')

# Create a test client
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(items_bp)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{os.getenv("DB_PASSWORD")}@localhost:3306/test_db'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app.test_client()

# Test case for creating a new item
def test_create_item(app):
    data = {"CategoryName": "Category 1", "ItemName": "Item 1", "ItemDescription": "Description 1"}
    response = app.post("/CreateItem", json=data)
    assert response.status_code == 200
    assert response.data == b"success"

# Test case for creating a duplicate item
def test_create_duplicate_item(app):
    data = {"CategoryName": "Category 1", "ItemName": "Item 1", "ItemDescription": "Description 1"}
    app.post("/CreateItem", json=data)
    response = app.post("/CreateItem", json=data)
    assert response.status_code == 400
    assert response.json["error"] == "Item already exists"

# Test case for getting categories
def test_get_categories(app):
    category1 = Category(CategoryName="Category 1")
    category2 = Category(CategoryName="Category 2")
    db.session.add(category1)
    db.session.add(category2)
    db.session.commit()

    response = app.get("/GetCategories")
    assert response.status_code == 200
    assert len(response.json) == 2
    assert {"CategoryId": category1.CategoryId, "CategoryName": "Category 1"} in response.json
    assert {"CategoryId": category2.CategoryId, "CategoryName": "Category 2"} in response.json

# Test case for getting items by category
def test_get_items_by_category(app):
    category1 = Category(CategoryName="Category 1")
    db.session.add(category1)
    db.session.commit()

    item1 = Item(ItemName="Item 1", CategoryId=category1.CategoryId, ItemDescription="Description 1")
    item2 = Item(ItemName="Item 2", CategoryId=category1.CategoryId, ItemDescription="Description 2")
    db.session.add(item1)
    db.session.add(item2)
    db.session.commit()

    response = app.get(f"/GetItems?CategoryId={category1.CategoryId}")
    assert response.status_code == 200
    assert len(response.json) == 2
    assert {"ItemId": item1.ItemId, "ItemName": "Item 1", "CategoryId": category1.CategoryId, "ItemDescription": "Description 1"} in response.json
    assert {"ItemId": item2.ItemId, "ItemName": "Item 2", "CategoryId": category1.CategoryId, "ItemDescription": "Description 2"} in response.json

# Test case for getting all items
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

    response = app.get("/GetAllItems")
    assert response.status_code == 200
    assert len(response.json) == 2
    assert {"name": "Item 1", "category": "Category 1", "description": "Description 1"} in response.json
    assert {"name": "Item 2", "category": "Category 2", "description": "Description 2"} in response.json
