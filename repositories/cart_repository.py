from typing import Optional
import uuid
from models.cart import Cart, CartItem
from models.database import db

class CartRepository:
    """Repository for managing cart data access."""
    
    def create_cart(self, user_id: Optional[str] = None) -> Cart:
        """Create a new cart."""
        cart_id = str(uuid.uuid4())
        cart = Cart(id=cart_id, user_id=user_id)
        db.session.add(cart)
        db.session.commit()
        return cart
    
    def get_cart_by_id(self, cart_id: str) -> Optional[Cart]:
        """Get a cart by its ID."""
        return Cart.query.get(cart_id)
    
    def get_cart_by_user_id(self, user_id: str) -> Optional[Cart]:
        """Get a cart by user ID."""
        return Cart.query.filter_by(user_id=user_id).first()
    
    def delete_cart(self, cart_id: str) -> bool:
        """Delete a cart."""
        cart = self.get_cart_by_id(cart_id)
        if cart:
            db.session.delete(cart)
            db.session.commit()
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
            for item in cart.items:
                db.session.delete(item)
            db.session.commit()
            return True
        return False

    def add_item_to_cart(self, cart_id: str, product_id: int, quantity: int) -> Optional[Cart]:
        """Add an item to a cart or update its quantity."""
        cart = self.get_cart_by_id(cart_id)
        if not cart:
            return None

        item = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()
        if item:
            item.quantity += quantity
        else:
            item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
            db.session.add(item)
        
        db.session.commit()
        return cart

    def remove_item_from_cart(self, cart_id: str, product_id: int) -> bool:
        """Remove an item from a cart."""
        item = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return True
        return False

    def update_item_quantity(self, cart_id: str, product_id: int, quantity: int) -> bool:
        """Update the quantity of an item in a cart."""
        item = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()
        if item:
            if quantity <= 0:
                return self.remove_item_from_cart(cart_id, product_id)
            item.quantity = quantity
            db.session.commit()
            return True
        return False