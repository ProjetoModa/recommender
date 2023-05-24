from . import db
from sqlalchemy.sql import func


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    x = db.Column(db.Numeric(20, 8), nullable=False)
    y = db.Column(db.Numeric(20, 8), nullable=False)
    type = db.Column(db.String(255), nullable=True)
    fabric = db.Column(db.String(255), nullable=True)
    pattern = db.Column(db.String(255), nullable=True)
    size = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Product {self.name}>'
