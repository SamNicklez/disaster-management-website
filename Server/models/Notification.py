from stores import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notification'

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.UserId'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_dismissed = db.Column(db.Boolean, default=False, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self):
        """
        Converts the Notification instance into a dictionary format for easier JSON serialization.
        """
        return {
            'notification_id': self.notification_id,
            'user_id': self.user_id,
            'message': self.message,
            'is_dismissed': self.is_dismissed,
            'created_date': self.created_date.isoformat()  
        }
