from stores import db
from models.DonationRequest import DonationRequest

class DisasterEvent(db.Model):
    __tablename__ = 'event'

    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.DECIMAL, nullable=True)
    longitude = db.Column(db.DECIMAL, nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True)
    requests = db.relationship('DonationRequest', backref='event', lazy=True)