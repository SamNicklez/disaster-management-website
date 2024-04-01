from flask import Flask
import unittest
from unittest.mock import patch, MagicMock
from models.Users import User
from Flask_app import users_bp

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.register_blueprint(users_bp)
        self.client = self.app.test_client()

    def test_login(self):
        with patch('models.Users.User.query') as mock_response:
            mock_response.filter_by.return_value.first.return_value = User(UserId=1,
                                                                           RoleID=1,
                                                                           IsVerified=1,
                                                                           Email='test@example.com',
                                                                           Password='scrypt:32768:8:1$brkU25Xau35F5V9X$24405f1a6836c5db9cdde8de5ef2829cc3980bc2a600858e9118b5068453f101cbfb13e84d85491346275150f6024e1eb6c4e7af80ef0ce7772619abc0152068'
                                                                           )
            response = self.client.post('/signin', json={
                                                            'email': 'test@example.com',
                                                            'password': 'password',
                                                            'roleid': 1
                                                        }
                                        )
            self.assertEqual(response.status_code, 200)

    def test_signin_user_not_verified(self): 
        with patch('models.Users.User.query') as mock_query:
            mock_user = MagicMock()
            mock_user.IsVerified = 0
            mock_query.filter_by.return_value.first.return_value = mock_user

            response = self.client.post('/signin', json={
                'email': 'test@example.com',
                'password': 'password'
            })

            self.assertEqual(response.status_code, 405)

    def test_signin_invalid_credentials(self):
        with patch('models.Users.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = None

            response = self.client.post('/signin', json={
                'email': 'nonexistent@example.com',
                'password': 'password'
            })

            self.assertEqual(response.status_code, 401)

    def test_signup_duplicate_user(self):
        with patch('Flask_app.db.session') as mock_session:
            mock_session.add.side_effect = Exception("Duplicate entry")
            response = self.client.post('/signup', json={
                'email': 'existing@example.com',
                'password': 'password',
                'roleid': 1
            })

            self.assertEqual(response.status_code, 409)

    def test_signup_success(self):
        with patch('Flask_app.db.session') as mock_session, \
             patch('smtplib.SMTP') as mock_smtp:
            response = self.client.post('/signup', json={
                'email': 'newuser@example.com',
                'password': 'password',
                'roleid': 1
            })

            self.assertEqual(response.status_code, 201)
            # Ensure that the email is sent for verification
            mock_smtp.return_value.sendmail.assert_called()

    def test_verify_invalid_code(self):
        with patch('Flask_app.db.session') as mock_session:
            # Assuming the verification code doesn't match
            response = self.client.post('/verify', json={
                'email': 'test@example.com',
                'verification': 123456  # Invalid verification code
            })

            self.assertEqual(response.status_code, 401)
    
    def test_verify_admin(self):
        with patch('routes.admin_auth.login_required') as mock_login:
            with patch('jwt.decode') as mock_jwt:
                mock_login.return_value = lambda f: f
                mock_jwt.return_value = {'RoleID': 1}
                response = self.client.post('/verifyAdmin', headers={'Authorization': 'Bearer ' + 'mock_token'})
                self.assertEqual(response.status_code, 200)


   

if __name__ == '__main__':
    unittest.main()
