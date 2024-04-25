from stores import db

class DonationRequest(db.Model):
    __tablename__ = 'request'
    request_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    event_item_id = db.Column(db.Integer, db.ForeignKey('eventitem.event_item_id'), nullable=True)
    is_fulfilled = db.Column(db.Integer, nullable=True)
    quantity_requested = db.Column(db.Integer, nullable=True)
    quantity_remaining = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, nullable=True)
    modified_date = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'request_id': self.request_id,
            'event_id': self.event_id,
            'user_id': self.user_id,
            'event_item_id': self.event_item_id,
            'is_fulfilled': self.is_fulfilled,
            'quantity_requested': self.quantity_requested,
            'quantity_remaining': self.quantity_remaining,
            'created_date': self.created_date,
        }
    shipping_number = db.Column(db.String(255), nullable=True)