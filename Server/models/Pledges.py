from stores import db

class Pledge(db.Model):
    __tablename__ = 'pledges'
    pledge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    quantity_given = db.Column(db.Integer, nullable=False)
    quantity_received = db.Column(db.Integer, nullable=False, default=0)
    is_fulfilled = db.Column(db.Integer, nullable=False, default=0)