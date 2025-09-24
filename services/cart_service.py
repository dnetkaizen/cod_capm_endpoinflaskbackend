from typing import Optional, Dict, Any
from models.cart import Cart
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from services.product_service import ProductService


class CartService:
    """Service layer for cart business logic."""
    
    def __init__(self, cart_repository: CartRepository, product_repository: ProductRepository):
        self.cart_repository = cart_repository
        self.product_repository = product_repository
        self.product_service = ProductService(product_repository)
    
    def get_or_create_cart(self, cart_id: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Get existing cart or create a new one."""
        cart = self.cart_repository.get_or_create_cart(cart_id, user_id)
        return {
            'success': True,
            'cart': cart.to_dict(),
            'message': 'Cart retrieved successfully'
        }
    
    def add_product_to_cart(self, cart_id: str, product_id: int, quantity: int = 1) -> Dict[str, Any]:
        """Add a product to the cart."""
        # Validate product availability
        availability = self.product_service.check_product_availability(product_id, quantity)
        if not availability['available']:
            return {
                'success': False,
                'message': availability['reason'],
                'cart': None
            }
        
        # Add item to cart
        cart = self.cart_repository.add_item_to_cart(cart_id, product_id, quantity)
        if not cart:
            return {
                'success': False,
                'message': 'Cart not found',
                'cart': None
            }
        
        return {
            'success': True,
            'message': f'Added {quantity} item(s) to cart',
            'cart': cart.to_dict()
        }
    
    def remove_product_from_cart(self, cart_id: str, product_id: int) -> Dict[str, Any]:
        """Remove a product from the cart."""
        if self.cart_repository.remove_item_from_cart(cart_id, product_id):
            cart = self.cart_repository.get_cart_by_id(cart_id)
            return {
                'success': True,
                'message': 'Product removed from cart',
                'cart': cart.to_dict()
            }
        else:
            return {
                'success': False,
                'message': 'Product not found in cart',
                'cart': None
            }
    
    def update_cart_item_quantity(self, cart_id: str, product_id: int, quantity: int) -> Dict[str, Any]:
        """Update the quantity of a product in the cart."""
        if self.cart_repository.update_item_quantity(cart_id, product_id, quantity):
            cart = self.cart_repository.get_cart_by_id(cart_id)
            action = 'removed from' if quantity == 0 else 'updated in'
            return {
                'success': True,
                'message': f'Product quantity {action} cart',
                'cart': cart.to_dict()
            }
        else:
            return {
                'success': False,
                'message': 'Product not found in cart',
                'cart': None
            }
    
    def get_cart_details(self, cart_id: str) -> Dict[str, Any]:
        """Get detailed cart information."""
        cart = self.cart_repository.get_cart_by_id(cart_id)
        if not cart:
            return {
                'success': False,
                'message': 'Cart not found',
                'cart': None
            }
        
        cart_dict = cart.to_dict()
        
        # Add additional cart statistics
        cart_dict['statistics'] = {
            'total_items': cart.get_item_count(),
            'total_amount': float(cart.get_total()),
            'unique_products': len(cart.items),
            'is_empty': len(cart.items) == 0
        }
        
        return {
            'success': True,
            'message': 'Cart retrieved successfully',
            'cart': cart_dict
        }
    
    def clear_cart(self, cart_id: str) -> Dict[str, Any]:
        """Clear all items from the cart."""
        if self.cart_repository.clear_cart(cart_id):
            cart = self.cart_repository.get_cart_by_id(cart_id)
            return {
                'success': True,
                'message': 'Cart cleared successfully',
                'cart': cart.to_dict()
            }
        else:
            return {
                'success': False,
                'message': 'Cart not found',
                'cart': None
            }
    
    def validate_cart_for_checkout(self, cart_id: str) -> Dict[str, Any]:
        """Validate cart items for checkout (stock availability, active products, etc.)."""
        cart = self.cart_repository.get_cart_by_id(cart_id)
        if not cart:
            return {
                'valid': False,
                'message': 'Cart not found',
                'issues': []
            }
        
        if not cart.items:
            return {
                'valid': False,
                'message': 'Cart is empty',
                'issues': []
            }
        
        issues = []
        for item in cart.items:
            # Check if product is still active
            current_product = self.product_repository.get_product_by_id(item.product.id)
            if not current_product or not current_product.is_active:
                issues.append({
                    'product_id': item.product.id,
                    'product_name': item.product.name,
                    'issue': 'Product is no longer available'
                })
                continue
            
            # Check stock availability
            if not self.product_repository.check_stock_availability(item.product.id, item.quantity):
                available_stock = current_product.stock
                issues.append({
                    'product_id': item.product.id,
                    'product_name': item.product.name,
                    'issue': f'Insufficient stock. Requested: {item.quantity}, Available: {available_stock}'
                })
        
        return {
            'valid': len(issues) == 0,
            'message': 'Cart is valid for checkout' if len(issues) == 0 else 'Cart has validation issues',
            'issues': issues,
            'cart': cart.to_dict()
        }