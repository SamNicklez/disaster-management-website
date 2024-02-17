from flask import Flask
from stores import db
from routes.Items import items_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:newSQLIowa00@localhost:3306/theapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(items_bp, url_prefix='/item')

@app.route("/")
def home():
    return "Home"

if __name__ == '__main__':
    app.run(debug=True) 