from stores import db

class Response(db.Model):
    __tablename__ = 'response'
    
    response_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.request_id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class ResponseItem(db.Model):
    __tablename__ = 'responseitem'
    
    response_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    response_id = db.Column(db.Integer, db.ForeignKey('response.response_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.ItemID'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)