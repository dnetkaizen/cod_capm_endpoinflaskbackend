from typing import List, Optional
from decimal import Decimal
from models.product import Product
from models.database import db

class ProductRepository:
    """Repository for managing product data access."""    
    def get_all_products(self) -> List[Product]:
        """Get all active products."""
        return Product.query.filter_by(is_active=True).all()
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get a product by its ID."""
        return Product.query.filter_by(id=product_id, is_active=True).first()
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get all products in a specific category."""
        return Product.query.filter_by(category=category, is_active=True).all()
    
    def search_products(self, query: str) -> List[Product]:
        """Search products by name or description."""
        query_lower = query.lower()
        return Product.query.filter(
            (Product.name.ilike(f'%{query_lower}%') | Product.description.ilike(f'%{query_lower}%')) & (Product.is_active == True)
        ).all()
    
    def create_product(self, product_data: dict) -> Product:
        """Create a new product."""
        new_product = Product.from_dict(product_data)
        db.session.add(new_product)
        db.session.commit()
        return new_product
    
    def update_product(self, product_id: int, product_data: dict) -> Optional[Product]:
        """Update an existing product."""
        product = self.get_product_by_id(product_id)
        if product:
            product.name = product_data.get('name', product.name)
            product.description = product_data.get('description', product.description)
            product.price = Decimal(str(product_data.get('price', product.price)))
            product.stock = product_data.get('stock', product.stock)
            product.category = product_data.get('category', product.category)
            product.image_url = product_data.get('image_url', product.image_url)
            db.session.commit()
            return product
        return None
    
    def delete_product(self, product_id: int) -> bool:
        """Soft delete a product by setting is_active to False."""
        product = self.get_product_by_id(product_id)
        if product:
            product.is_active = False
            db.session.commit()
            return True
        return False
    
    def update_stock(self, product_id: int, quantity_change: int) -> bool:
        """Update product stock (positive to add, negative to subtract)."""
        product = self.get_product_by_id(product_id)
        if product and product.stock + quantity_change >= 0:
            product.stock += quantity_change
            db.session.commit()
            return True
        return False
    
    def check_stock_availability(self, product_id: int, required_quantity: int) -> bool:
        """Check if enough stock is available for a product."""
        product = self.get_product_by_id(product_id)
        return product is not None and product.stock >= required_quantity

    def populate_db(self):
        """Populate the database with sample data."""
        if Product.query.count() == 0:
            sample_products = [
                Product(
                    name="Laptop Gaming",
                    description="High-performance gaming laptop with RTX graphics",
                    price=Decimal("1299.99"),
                    stock=10,
                    category="Electronics",
                    image_url="https://images.pexels.com/photos/7974/pexels-photo.jpg"
                ),
                Product(
                    name="Wireless Headphones",
                    description="Premium noise-cancelling wireless headphones",
                    price=Decimal("199.99"),
                    stock=25,
                    category="Electronics",
                    image_url="https://images.pexels.com/photos/205926/pexels-photo-205926.jpeg"
                ),
                Product(
                    name="Coffee Maker",
                    description="Automatic drip coffee maker with programmable timer",
                    price=Decimal("89.99"),
                    stock=15,
                    category="Home & Kitchen",
                    image_url="https://images.pexels.com/photos/593328/pexels-photo-593328.jpeg"
                ),
                Product(
                    name="Running Shoes",
                    description="Comfortable running shoes with advanced cushioning",
                    price=Decimal("129.99"),
                    stock=30,
                    category="Sports",
                    image_url="https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg"
                ),
                Product(
                    name="Smartphone",
                    description="Latest smartphone with advanced camera system",
                    price=Decimal("799.99"),
                    stock=20,
                    category="Electronics",
                    image_url="https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg"
                )
            ]
            db.session.bulk_save_objects(sample_products)
            db.session.commit()