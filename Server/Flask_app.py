from flask import Flask
from flask_cors import CORS
from stores import db
from routes.Items import items_bp
from routes.Users import users_bp
from routes.Events import events_bp
from routes.Pledges import pledges_bp
from routes.Notification import notification_bp
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] =f'mysql://root:{os.getenv("DB_PASSWORD")}@localhost:3306/theapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY")
db.init_app(app)

app.register_blueprint(users_bp, url_prefix='/users_bp')
app.register_blueprint(items_bp, url_prefix='/item')
app.register_blueprint(events_bp, url_prefix='/event')
app.register_blueprint(pledges_bp, url_prefix='/pledge')
app.register_blueprint(notification_bp, url_prefix='/notification')

@app.route("/")
def home():
    return "Home"

if __name__ == '__main__':
    app.run(debug=True)