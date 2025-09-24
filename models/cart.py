from .database import db
from decimal import Decimal

class Cart(db.Model):
    """Cart model representing a shopping cart."""
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), nullable=True)
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        """Convert cart to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items],
            'total': float(self.get_total()),
            'item_count': self.get_item_count()
        }

    def get_total(self) -> Decimal:
        """Calculate total amount of the cart."""
        return sum(item.get_subtotal() for item in self.items)

    def get_item_count(self) -> int:
        """Get total number of items in the cart."""
        return sum(item.quantity for item in self.items)

class CartItem(db.Model):
    """Cart item model representing a product in the cart."""
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.String(36), db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product')

    def get_subtotal(self) -> Decimal:
        """Calculate subtotal for this cart item."""
        return self.product.price * self.quantity

    def to_dict(self) -> dict:
        """Convert cart item to dictionary for JSON serialization."""
        return {
            'product': self.product.to_dict(),
            'quantity': self.quantity,
            'subtotal': float(self.get_subtotal())
        }