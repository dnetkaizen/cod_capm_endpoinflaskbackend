from typing import List, Optional
from decimal import Decimal
from models.product import Product


class ProductRepository:
    """Repository for managing product data access."""
    
    def __init__(self):
        # In-memory storage for demo purposes
        # In a real application, this would connect to a database
        self._products = self._initialize_sample_data()
        self._next_id = len(self._products) + 1
    
    def _initialize_sample_data(self) -> List[Product]:
        """Initialize with sample product data."""
        return [
            Product(
                id=1,
                name="Laptop Gaming",
                description="High-performance gaming laptop with RTX graphics",
                price=Decimal("1299.99"),
                stock=10,
                category="Electronics",
                image_url="https://example.com/laptop.jpg"
            ),
            Product(
                id=2,
                name="Wireless Headphones",
                description="Premium noise-cancelling wireless headphones",
                price=Decimal("199.99"),
                stock=25,
                category="Electronics",
                image_url="https://example.com/headphones.jpg"
            ),
            Product(
                id=3,
                name="Coffee Maker",
                description="Automatic drip coffee maker with programmable timer",
                price=Decimal("89.99"),
                stock=15,
                category="Home & Kitchen",
                image_url="https://example.com/coffee-maker.jpg"
            ),
            Product(
                id=4,
                name="Running Shoes",
                description="Comfortable running shoes with advanced cushioning",
                price=Decimal("129.99"),
                stock=30,
                category="Sports",
                image_url="https://example.com/shoes.jpg"
            ),
            Product(
                id=5,
                name="Smartphone",
                description="Latest smartphone with advanced camera system",
                price=Decimal("799.99"),
                stock=20,
                category="Electronics",
                image_url="https://example.com/smartphone.jpg"
            )
        ]
    
    def get_all_products(self) -> List[Product]:
        """Get all active products."""
        return [product for product in self._products if product.is_active]
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get a product by its ID."""
        for product in self._products:
            if product.id == product_id and product.is_active:
                return product
        return None
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get all products in a specific category."""
        return [
            product for product in self._products 
            if product.category.lower() == category.lower() and product.is_active
        ]
    
    def search_products(self, query: str) -> List[Product]:
        """Search products by name or description."""
        query_lower = query.lower()
        return [
            product for product in self._products
            if (query_lower in product.name.lower() or 
                query_lower in product.description.lower()) and product.is_active
        ]
    
    def create_product(self, product_data: dict) -> Product:
        """Create a new product."""
        product_data['id'] = self._next_id
        self._next_id += 1
        
        new_product = Product.from_dict(product_data)
        self._products.append(new_product)
        return new_product
    
    def update_product(self, product_id: int, product_data: dict) -> Optional[Product]:
        """Update an existing product."""
        for i, product in enumerate(self._products):
            if product.id == product_id:
                product_data['id'] = product_id
                updated_product = Product.from_dict(product_data)
                self._products[i] = updated_product
                return updated_product
        return None
    
    def delete_product(self, product_id: int) -> bool:
        """Soft delete a product by setting is_active to False."""
        for product in self._products:
            if product.id == product_id:
                product.is_active = False
                return True
        return False
    
    def update_stock(self, product_id: int, quantity_change: int) -> bool:
        """Update product stock (positive to add, negative to subtract)."""
        product = self.get_product_by_id(product_id)
        if product and product.stock + quantity_change >= 0:
            product.stock += quantity_change
            return True
        return False
    
    def check_stock_availability(self, product_id: int, required_quantity: int) -> bool:
        """Check if enough stock is available for a product."""
        product = self.get_product_by_id(product_id)
        return product is not None and product.stock >= required_quantity
