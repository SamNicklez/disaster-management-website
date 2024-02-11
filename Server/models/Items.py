from stores import db

class Category(db.Model):
    __tablename__ = 'category'
    CategoryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CategoryName = db.Column(db.String(255), nullable=False)
    

class Item(db.Model):
    __tablename__ = 'items'
    ItemID = db.Column(db.Integer, primary_key=True)
    ItemName = db.Column(db.String(255), nullable=False)
    ItemDescription = db.Column(db.String(255))
    CategoryId = db.Column(db.Integer, db.ForeignKey('category.CategoryId') ,nullable=False)
    category = db.relationship('Category', backref=db.backref('items', lazy=True))

    