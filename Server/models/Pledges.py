from stores import db

class Pledge(db.Model):
    __tablename__ = 'pledge'
    pledge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    quantity_given = db.Column(db.Integer, nullable=False)
    quantity_remaining = db.Column(db.Integer, nullable=False, default=0)
    is_fulfilled = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            'pledge_id': self.pledge_id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'quantity_given': self.quantity_given,
            'quantity_remaining': self.quantity_remaining,
            'is_fulfilled': self.is_fulfilled
        }