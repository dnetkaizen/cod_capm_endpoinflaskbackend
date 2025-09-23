# Flask E-commerce API

This project implements a Flask-based REST API for an e-commerce system with a layered architecture. The API provides endpoints for product management and shopping cart functionality.

## Architecture

The project follows a **layered architecture** pattern with clear separation of concerns:

```
├── models/          # Data models and entities
├── repositories/    # Data access layer
├── services/        # Business logic layer
├── controllers/     # API controllers and routes
└── app.py          # Main Flask application
```

### Layers Description:

1. **Models Layer**: Defines data structures (Product, Cart, CartItem)
2. **Repository Layer**: Handles data access and storage operations
3. **Service Layer**: Contains business logic and validation
4. **Controller Layer**: Manages HTTP requests/responses and API endpoints

## Features

### Product Management
- Get all products with filtering and pagination
- Get detailed product information
- Check product availability
- Search products by name/description
- Get product categories

### Shopping Cart
- Create and manage shopping carts
- Add products to cart
- Update item quantities
- Remove items from cart
- Clear entire cart
- Validate cart for checkout

## API Endpoints

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | Get all products |
| GET | `/api/products/<id>` | Get product details |
| GET | `/api/products/<id>/availability` | Check product availability |
| GET | `/api/products/categories` | Get all categories |
| GET | `/api/products/search` | Search products |

### Cart

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/cart` | Create or get cart |
| GET | `/api/cart/<cart_id>` | Get cart details |
| POST | `/api/cart/<cart_id>/items` | Add product to cart |
| PUT | `/api/cart/<cart_id>/items/<product_id>` | Update item quantity |
| DELETE | `/api/cart/<cart_id>/items/<product_id>` | Remove item from cart |
| POST | `/api/cart/<cart_id>/clear` | Clear cart |
| GET | `/api/cart/<cart_id>/validate` | Validate cart |

## Installation and Setup

1. **Clone the repository**
   ```bash
   cd Endpoint_flask
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## Usage Examples

### Get All Products
```bash
curl -X GET "http://localhost:5000/api/products"
```

### Get Product Details
```bash
curl -X GET "http://localhost:5000/api/products/1"
```

### Create Cart and Add Product
```bash
# Create cart
curl -X POST "http://localhost:5000/api/cart" \
  -H "Content-Type: application/json"

# Add product to cart (use cart_id from previous response)
curl -X POST "http://localhost:5000/api/cart/{cart_id}/items" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

### Search Products
```bash
curl -X GET "http://localhost:5000/api/products/search?q=laptop"
```

## Sample Data

The application comes with sample products including:
- Laptop Gaming ($1,299.99)
- Wireless Headphones ($199.99)
- Coffee Maker ($89.99)
- Running Shoes ($129.99)
- Smartphone ($799.99)

## Response Format

All API responses follow a consistent format:

```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully"
}
```

For errors:
```json
{
  "success": false,
  "message": "Error description"
}
```

## Development

### Project Structure
```
Endpoint_flask/
├── models/
│   ├── __init__.py
│   ├── product.py
│   └── cart.py
├── repositories/
│   ├── __init__.py
│   ├── product_repository.py
│   └── cart_repository.py
├── services/
│   ├── __init__.py
│   ├── product_service.py
│   └── cart_service.py
├── controllers/
│   ├── __init__.py
│   ├── product_controller.py
│   └── cart_controller.py
├── app.py
├── requirements.txt
└── README.md
```

### Adding New Features

1. **Add new models** in the `models/` directory
2. **Create repositories** for data access in `repositories/`
3. **Implement business logic** in `services/`
4. **Create API endpoints** in `controllers/`
5. **Register blueprints** in `app.py`

## Testing

You can test the API using:
- **curl** commands (examples above)
- **Postman** or similar API testing tools
- **Python requests** library
- **Browser** for GET endpoints

## Notes

- This implementation uses in-memory storage for demonstration purposes
- In production, replace repositories with actual database connections
- Add authentication and authorization as needed
- Implement proper logging and monitoring
- Add input validation and sanitization
- Consider adding rate limiting and caching
