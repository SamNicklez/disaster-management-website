import pytest
from flask import Flask, jsonify
from models.Users import User
from models.Roles import Role
from werkzeug.security import generate_password_hash
from routes import users_bp
import jwt
import sys
sys.path.append('/Users/deepikamitta/PycharmProjects/software-engineering-project-team-3')

# Create a test client
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(users_bp)
    app.config['TESTING'] = True
    return app.test_client()

# Test case for successful signup
def test_signup(app):
    data = {"email": "test@example.com", "password": "password", "roleid": 1}
    response = app.post("/signup", json=data)
    assert response.status_code == 201
    assert response.json["message"] == "User created successfully"

# Test case for duplicate signup
def test_duplicate_signup(app):
    # Create a user first
    data = {"email": "test@example.com", "password": "password", "roleid": 1}
    app.post("/signup", json=data)

    # Try to create the same user again
    response = app.post("/signup", json=data)
    assert response.status_code == 409
    assert response.json["error"] == "User already exists"

# Test case for successful signin
def test_signin(app):
    # Create a user first
    data = {"email": "test@example.com", "password": "password", "roleid": 1}
    app.post("/signup", json=data)

    # Verify the user
    user = User.query.filter_by(Email="test@example.com").first()
    user.IsVerified = 1

    # Try to sign in
    data = {"email": "test@example.com", "password": "password"}
    response = app.post("/signin", json=data)
    assert response.status_code == 200
    assert "token" in response.json

# Test case for invalid signin
def test_invalid_signin(app):
    data = {"email": "test@example.com", "password": "wrongpassword"}
    response = app.post("/signin", json=data)
    assert response.status_code == 401
    assert response.json["error"] == "Invalid email or password"

# Test case for successful verification
def test_verify(app):
    # Create a user first
    data = {"email": "test@example.com", "password": "password", "roleid": 1}
    app.post("/signup", json=data)

    # Get the verification code
    user = User.query.filter_by(Email="test@example.com").first()
    verification_code = user.IsVerified

    # Verify the user
    data = {"email": "test@example.com", "verification": verification_code}
    response = app.post("/verify", json=data)
    assert response.status_code == 200
    assert response.json["message"] == "User verified successfully"

def test_invalid_verify(app):
    # Create a user first
    data = {"email": "test@example.com", "password": "password", "roleid": 1}
    app.post("/signup", json=data)

    data = {"email": "test@example.com", "verification": 123456}
    response = app.post("/verify", json=data)
    assert response.status_code == 401
    assert response.json["error"] == "Invalid verification code"

