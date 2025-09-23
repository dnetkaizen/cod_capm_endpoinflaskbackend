from dataclasses import dataclass, field
from typing import List, Dict, Optional
from decimal import Decimal
from .product import Product


@dataclass
class CartItem:
    """Cart item model representing a product in the cart."""
    product: Product
    quantity: int
    
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


@dataclass
class Cart:
    """Cart model representing a shopping cart."""
    id: str
    user_id: Optional[str] = None
    items: List[CartItem] = field(default_factory=list)
    
    def add_product(self, product: Product, quantity: int = 1) -> None:
        """Add a product to the cart or update quantity if already exists."""
        for item in self.items:
            if item.product.id == product.id:
                item.quantity += quantity
                return
        
        self.items.append(CartItem(product=product, quantity=quantity))
    
    def remove_product(self, product_id: int) -> bool:
        """Remove a product from the cart."""
        for i, item in enumerate(self.items):
            if item.product.id == product_id:
                del self.items[i]
                return True
        return False
    
    def update_quantity(self, product_id: int, quantity: int) -> bool:
        """Update quantity of a product in the cart."""
        for item in self.items:
            if item.product.id == product_id:
                if quantity <= 0:
                    return self.remove_product(product_id)
                item.quantity = quantity
                return True
        return False
    
    def get_total(self) -> Decimal:
        """Calculate total amount of the cart."""
        return sum(item.get_subtotal() for item in self.items)
    
    def get_item_count(self) -> int:
        """Get total number of items in the cart."""
        return sum(item.quantity for item in self.items)
    
    def clear(self) -> None:
        """Clear all items from the cart."""
        self.items.clear()
    
    def to_dict(self) -> dict:
        """Convert cart to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items],
            'total': float(self.get_total()),
            'item_count': self.get_item_count()
        }
