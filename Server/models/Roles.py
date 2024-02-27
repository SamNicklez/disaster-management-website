from stores import db

class Role(db.Model):
    __tablename__ = 'roles'
    RoleID: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name: str = db.Column(db.String(45), nullable=False)
    