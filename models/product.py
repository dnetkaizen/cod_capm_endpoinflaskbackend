from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class Product:
    """Product model representing a product in the system."""
    id: int
    name: str
    description: str
    price: Decimal
    stock: int
    category: str
    image_url: Optional[str] = None
    is_active: bool = True
    
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
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Create Product instance from dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            price=Decimal(str(data['price'])),
            stock=data['stock'],
            category=data['category'],
            image_url=data.get('image_url'),
            is_active=data.get('is_active', True)
        )
