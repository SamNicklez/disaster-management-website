from stores import db

class DonationRequest(db.Model):
    __tablename__ = 'request'

    request_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    is_fulfilled = db.Column(db.Boolean, nullable=True)
    created_date = db.Column(db.DateTime, nullable=True)
    modified_date = db.Column(db.DateTime, nullable=True)
    items = db.relationship('ItemRequest', backref='donation_request')

class ItemRequest(db.Model):
    __tablename__ = 'requestitem'

    request_item_id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.request_id'), nullable=True)
    event_item_id = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)