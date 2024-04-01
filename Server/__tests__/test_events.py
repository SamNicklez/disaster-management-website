from flask import Flask
import unittest
from unittest.mock import patch
from models.DisasterEvent import DisasterEvent, EventItem
from models.DonationRequest import DonationRequest
from models.Items import Item
from Flask_app import events_bp

class TestItemsRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.register_blueprint(events_bp)
        self.client = self.app.test_client()

    def test_create_event(self):
        with patch('routes.admin_auth.login_required') as mock_login:
            with patch('jwt.decode') as mock_jwt:
                with patch('stores.db.session') as mock_db_response:
                    with patch('models.Items.Item.query') as mock_item_response:
                        mock_login.return_value = lambda f: f
                        mock_jwt.return_value = {'RoleID': 1}
                        mock_db_response.add.return_value = None
                        mock_db_response.commit.return_value = None
                        mock_item_response.filter_by.return_value.first.return_value = None
                        response = self.client.post('/CreateEvent',
                                                    json={
                                                            'event_name': 'test_event',
                                                            'location': 'test_location',
                                                            'latitude': 'test_latitude',
                                                            'longitude': 'test_longitude',
                                                            'description': 'test',
                                                            'item_names': ['test_item']
                                                        },
                                                    headers={'Authorization': 'Bearer ' + 'mock_token'}
                                                    )
                        self.assertEqual(response.status_code, 201)

    def test_create_event_item(self):
        with patch('routes.admin_auth.login_required') as mock_login:
            with patch('jwt.decode') as mock_jwt:
                with patch('models.DisasterEvent.DisasterEvent.query') as mock_disaster_event_response:
                    with patch('models.Items.Item.query') as mock_item_response:
                        with patch('stores.db.session') as mock_db_response:
                            mock_login.return_value = lambda f: f
                            mock_jwt.return_value = {'RoleID': 1}
                            mock_disaster_event_response.get.return_value = DisasterEvent(event_id=1)
                            mock_item_response.filter_by.return_value.first.return_value = Item(ItemID=1)
                            mock_db_response.add.return_value = None
                            mock_db_response.commit.return_value = None
                            response = self.client.post('/CreateEventItem',
                                                        json={
                                                                'event_id': 1,
                                                                'item_names': ['test_item1', 'test_item2']
                                                            },
                                                        headers={'Authorization': 'Bearer ' + 'mock_token'}
                                                        )
                            self.assertEqual(response.status_code, 201)