import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from models.Items import Item, Category
from Flask_app import items_bp

class TestItems(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.register_blueprint(items_bp)
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_create_category_success(self):
        with patch('Flask_app.db.session') as mock_session:
            mock_session.add.return_value = None
            response = self.client.post('/CreateCategory', json={'CategoryName': 'TestCategory'})
            self.assertEqual(response.status_code, 201)

    def test_create_category_exists_inactive(self):
        with patch('Flask_app.db.session') as mock_session:
            mock_session.add.return_value = None
            mock_category = MagicMock()
            mock_category.isActive = 0
            mock_session.query(Category).filter_by.return_value.first.return_value = mock_category
            response = self.client.post('/CreateCategory', json={'CategoryName': 'TestCategory'})
            self.assertEqual(response.status_code, 201)

    def test_create_category_already_exists(self):
        with patch('Flask_app.db.session') as mock_session:
            mock_session.query(Category).filter_by.return_value.first.return_value = MagicMock()
            response = self.client.post('/CreateCategory', json={'CategoryName': 'Test2'})
            self.assertEqual(response.status_code, 201)

    # def test_create_item_success(self):
    #     with patch('Flask_app.db.session') as mock_session:
    #         mock_session.query(Category).filter_by.return_value.first.return_value = MagicMock()
    #         mock_session.query(Item).filter_by.return_value.first.return_value = None
    #         response = self.client.post('/CreateItem', json={'CategoryName': 'TestCategory', 'ItemName': 'TestItem', 'ItemDescription': 'Description'})
    #         self.assertEqual(response.status_code, 201)

    def test_create_item_already_exists(self):
        with patch('Flask_app.db.session') as mock_session:
            mock_session.query(Category).filter_by.return_value.first.return_value = MagicMock()
            mock_session.query(Item).filter_by.return_value.first.return_value = MagicMock()
            response = self.client.post('/CreateItem', json={'CategoryName': 'TestCategory', 'ItemName': 'TestItem', 'ItemDescription': 'Description'})
            self.assertEqual(response.status_code, 401)

    # def test_get_categories_success(self):
    #     with patch('Flask_app.db.session') as mock_session:
    #         mock_category_1 = MagicMock()
    #         mock_category_1.CategoryId = 1
    #         mock_category_1.CategoryName = 'TestCategory1'

    #         mock_category_2 = MagicMock()
    #         mock_category_2.CategoryId = 2
    #         mock_category_2.CategoryName = 'TestCategory2'

    #         mock_session.query(Category).all.return_value = [mock_category_1, mock_category_2]
    #         response = self.client.get('/GetCategories')
    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(response.json, [{'CategoryId': 1, 'CategoryName': 'TestCategory1'}, {'CategoryId': 2, 'CategoryName': 'TestCategory2'}])
            
    # def test_get_all_items_success(self):
    #     with patch('Flask_app.db.session') as mock_session:
    #         mock_item_1 = MagicMock()
    #         mock_item_1.ItemName = 'TestItem1'
    #         mock_item_1.ItemDescription = 'Description1'
    #         mock_item_1.Category = MagicMock()
    #         mock_item_1.Category.CategoryName = 'TestCategory1'

    #         mock_item_2 = MagicMock()
    #         mock_item_2.ItemName = 'TestItem2'
    #         mock_item_2.ItemDescription = 'Description2'
    #         mock_item_2.Category = MagicMock()
    #         mock_item_2.Category.CategoryName = 'TestCategory2'

    #         mock_session.query(Item, Category.CategoryName).join.return_value.filter.return_value.all.return_value = [(mock_item_1, 'TestCategory1'), (mock_item_2, 'TestCategory2')]
    #         response = self.client.get('/GetAllItems')
    #         self.assertEqual(response.status_code, 200)
    #         self.assertEqual(response.json, [{'name': 'TestItem1', 'category': 'TestCategory1', 'description': 'Description1'}, {'name': 'TestItem2', 'category': 'TestCategory2', 'description': 'Description2'}])



   

if __name__ == '__main__':
    unittest.main()
