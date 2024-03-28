from stores import db

class Response(db.Model):
    __tablename__ = 'response'
    response_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.request_id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    is_fullfilled = db.Column(db.Integer, nullable=False)
    quantity_donated = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    shipped_date = db.Column(db.DateTime, nullable=True)