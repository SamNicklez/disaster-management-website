from stores import db

class User(db.Model):
    __tablename__ = 'users'

    UserId: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName: str = db.Column(db.String(45), nullable=False)
    LastName: str = db.Column(db.String(45), nullable=False)
    Email: str = db.Column(db.String(255), nullable=False)
    PhoneNumber: int = db.Column(db.Integer)
    Password: str = db.Column(db.String(255), nullable=False)
    RoleID: int = db.Column(db.Integer, db.ForeignKey('roles.RoleID'))
    IsVerified: int = db.Column(db.Integer)
    State: str = db.Column(db.String(45), nullable=False)
    City: str = db.Column(db.String(45), nullable=False)
    Address: str = db.Column(db.String(255), nullable=False)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    ZipCode: int = db.Column(db.Integer, nullable=False)
    