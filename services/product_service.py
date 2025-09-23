from typing import List, Optional, Dict, Any
from ..models.product import Product
from ..repositories.product_repository import ProductRepository


class ProductService:
    """Service layer for product business logic."""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def get_all_products(self, category: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all products with optional filtering."""
        if search:
            products = self.product_repository.search_products(search)
        elif category:
            products = self.product_repository.get_products_by_category(category)
        else:
            products = self.product_repository.get_all_products()
        
        return [product.to_dict() for product in products]
    
    def get_product_detail(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific product."""
        product = self.product_repository.get_product_by_id(product_id)
        if product:
            product_dict = product.to_dict()
            # Add additional details that might be useful
            product_dict['in_stock'] = product.stock > 0
            product_dict['low_stock'] = product.stock <= 5
            return product_dict
        return None
    
    def check_product_availability(self, product_id: int, quantity: int = 1) -> Dict[str, Any]:
        """Check if a product is available in the requested quantity."""
        product = self.product_repository.get_product_by_id(product_id)
        
        if not product:
            return {
                'available': False,
                'reason': 'Product not found',
                'product': None
            }
        
        if not product.is_active:
            return {
                'available': False,
                'reason': 'Product is not active',
                'product': product.to_dict()
            }
        
        if product.stock < quantity:
            return {
                'available': False,
                'reason': f'Insufficient stock. Available: {product.stock}, Requested: {quantity}',
                'product': product.to_dict(),
                'available_stock': product.stock
            }
        
        return {
            'available': True,
            'reason': 'Product is available',
            'product': product.to_dict(),
            'available_stock': product.stock
        }
    
    def get_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all products in a specific category."""
        products = self.product_repository.get_products_by_category(category)
        return [product.to_dict() for product in products]
    
    def search_products(self, query: str) -> List[Dict[str, Any]]:
        """Search products by name or description."""
        products = self.product_repository.search_products(query)
        return [product.to_dict() for product in products]
    
    def get_product_categories(self) -> List[str]:
        """Get all unique product categories."""
        products = self.product_repository.get_all_products()
        categories = list(set(product.category for product in products))
        return sorted(categories)
    
    def validate_product_data(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate product data before creation or update."""
        errors = []
        
        # Required fields validation
        required_fields = ['name', 'description', 'price', 'stock', 'category']
        for field in required_fields:
            if field not in product_data or not product_data[field]:
                errors.append(f'{field} is required')
        
        # Data type and value validation
        if 'price' in product_data:
            try:
                price = float(product_data['price'])
                if price < 0:
                    errors.append('Price must be non-negative')
            except (ValueError, TypeError):
                errors.append('Price must be a valid number')
        
        if 'stock' in product_data:
            try:
                stock = int(product_data['stock'])
                if stock < 0:
                    errors.append('Stock must be non-negative')
            except (ValueError, TypeError):
                errors.append('Stock must be a valid integer')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
