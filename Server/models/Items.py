from stores import db

class Category(db.Model):
    __tablename__ = 'category'
    CategoryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CategoryName = db.Column(db.String(255), nullable=False)
    isActive = db.Column(db.Integer, nullable=False, default=1)
    

class Item(db.Model):
    __tablename__ = 'items'
    ItemID = db.Column(db.Integer, primary_key=True)
    ItemName = db.Column(db.String(255), nullable=False)
    ItemDescription = db.Column(db.String(255))
    isActive = db.Column(db.Integer, nullable=False, default=1)
    CategoryId = db.Column(db.Integer, db.ForeignKey('category.CategoryId') ,nullable=False)
    category = db.relationship('Category', backref=db.backref('items', lazy=True))

    def to_dict(self):
        return {
            'ItemID': self.ItemID,
            'ItemName': self.ItemName,
            'ItemDescription': self.ItemDescription,
            'isActive': self.isActive,
            'CategoryId': self.CategoryId
        }
    
    def to_dict_match(self):
        return {
            'ItemID': self.ItemID,
            'ItemName': self.ItemName,
            'ItemDescription': self.ItemDescription,
            'isActive': self.isActive,
        }

    