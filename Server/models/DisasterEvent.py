from stores import db
from models.DonationRequest import DonationRequest

class DisasterEvent(db.Model):
    __tablename__ = 'event'

    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.FLOAT, nullable=True)
    longitude = db.Column(db.FLOAT, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True)
    requests = db.relationship('DonationRequest', backref='event', lazy=True)
    items = db.relationship('EventItem', backref='event', lazy=True)

class EventItem(db.Model):
    __tablename__ = 'eventitem'

    event_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.ItemID'), nullable=False)