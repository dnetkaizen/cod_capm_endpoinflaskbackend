from typing import Dict, Optional
import uuid
from ..models.cart import Cart


class CartRepository:
    """Repository for managing cart data access."""
    
    def __init__(self):
        # In-memory storage for demo purposes
        # In a real application, this would connect to a database
        self._carts: Dict[str, Cart] = {}
    
    def create_cart(self, user_id: Optional[str] = None) -> Cart:
        """Create a new cart."""
        cart_id = str(uuid.uuid4())
        cart = Cart(id=cart_id, user_id=user_id)
        self._carts[cart_id] = cart
        return cart
    
    def get_cart_by_id(self, cart_id: str) -> Optional[Cart]:
        """Get a cart by its ID."""
        return self._carts.get(cart_id)
    
    def get_cart_by_user_id(self, user_id: str) -> Optional[Cart]:
        """Get a cart by user ID."""
        for cart in self._carts.values():
            if cart.user_id == user_id:
                return cart
        return None
    
    def update_cart(self, cart: Cart) -> Cart:
        """Update an existing cart."""
        self._carts[cart.id] = cart
        return cart
    
    def delete_cart(self, cart_id: str) -> bool:
        """Delete a cart."""
        if cart_id in self._carts:
            del self._carts[cart_id]
            return True
        return False
    
    def get_or_create_cart(self, cart_id: Optional[str] = None, user_id: Optional[str] = None) -> Cart:
        """Get existing cart or create a new one."""
        if cart_id:
            cart = self.get_cart_by_id(cart_id)
            if cart:
                return cart
        
        if user_id:
            cart = self.get_cart_by_user_id(user_id)
            if cart:
                return cart
        
        return self.create_cart(user_id)
    
    def clear_cart(self, cart_id: str) -> bool:
        """Clear all items from a cart."""
        cart = self.get_cart_by_id(cart_id)
        if cart:
            cart.clear()
            return True
        return False
