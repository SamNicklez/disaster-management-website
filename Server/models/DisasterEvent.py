from stores import db

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

    def to_dict(self):
        return {
            'event_id': self.event_id,
            'event_name': self.event_name,
            'description': self.description,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
    
    def to_dict_match(self):
        return {
            'event_name': self.event_name,
            'location': self.location,
            'start_date': self.start_date,
        }

class EventItem(db.Model):
    __tablename__ = 'eventitem'

    event_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.ItemID'), nullable=False)
    isActive = db.Column(db.Integer, nullable=False, default=1)

    def to_dict(self):
        return {
            'event_item_id': self.event_item_id,
            'event_id': self.event_id,
            'item_id': self.item_id,
            'isActive': self.isActive
        }