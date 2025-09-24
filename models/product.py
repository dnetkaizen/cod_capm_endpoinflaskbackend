from .database import db
from decimal import Decimal

class Product(db.Model):
    """Product model representing a product in the system."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self) -> dict:
        """Convert product to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'stock': self.stock,
            'category': self.category,
            'image_url': self.image_url,
            'is_active': self.is_active
        }

    @staticmethod
    def from_dict(data: dict) -> 'Product':
        """Create Product instance from dictionary."""
        return Product(
            name=data['name'],
            description=data['description'],
            price=Decimal(str(data['price'])),
            stock=data['stock'],
            category=data['category'],
            image_url=data.get('image_url'),
            is_active=data.get('is_active', True)
        )