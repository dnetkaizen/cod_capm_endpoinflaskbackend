from flask import Blueprint, request, jsonify
from services.cart_service import CartService
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository

# Create blueprint
cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

# Initialize dependencies
cart_repository = CartRepository()
product_repository = ProductRepository()
cart_service = CartService(cart_repository, product_repository)


@cart_bp.route('', methods=['POST'])
def create_or_get_cart():
    """
    Create a new cart or get existing cart.
    Request body (optional):
    - cart_id: Existing cart ID
    - user_id: User ID for the cart
    """
    try:
        data = request.get_json() or {}
        cart_id = data.get('cart_id')
        user_id = data.get('user_id')
        
        result = cart_service.get_or_create_cart(cart_id=cart_id, user_id=user_id)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating/retrieving cart: {str(e)}'
        }), 500


@cart_bp.route('/<cart_id>', methods=['GET'])
def get_cart(cart_id: str):
    """
    Get cart details by cart ID.
    """
    try:
        result = cart_service.get_cart_details(cart_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving cart: {str(e)}'
        }), 500


@cart_bp.route('/<cart_id>/items', methods=['POST'])
def add_product_to_cart(cart_id: str):
    """
    Add a product to the cart.
    Request body:
    - product_id: ID of the product to add (required)
    - quantity: Quantity to add (default: 1)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request body is required'
            }), 400
        
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not product_id:
            return jsonify({
                'success': False,
                'message': 'product_id is required'
            }), 400
        
        if not isinstance(product_id, int) or product_id <= 0:
            return jsonify({
                'success': False,
                'message': 'product_id must be a positive integer'
            }), 400
        
        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({
                'success': False,
                'message': 'quantity must be a positive integer'
            }), 400
        
        result = cart_service.add_product_to_cart(cart_id, product_id, quantity)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error adding product to cart: {str(e)}'
        }), 500


@cart_bp.route('/<cart_id>/items/<int:product_id>', methods=['PUT'])
def update_cart_item(cart_id: str, product_id: int):
    """
    Update quantity of a product in the cart.
    Request body:
    - quantity: New quantity (0 to remove item)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request body is required'
            }), 400
        
        quantity = data.get('quantity')
        
        if quantity is None:
            return jsonify({
                'success': False,
                'message': 'quantity is required'
            }), 400
        
        if not isinstance(quantity, int) or quantity < 0:
            return jsonify({
                'success': False,
                'message': 'quantity must be a non-negative integer'
            }), 400
        
        result = cart_service.update_cart_item_quantity(cart_id, product_id, quantity)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating cart item: {str(e)}'
        }), 500


@cart_bp.route('/<cart_id>/items/<int:product_id>', methods=['DELETE'])
def remove_product_from_cart(cart_id: str, product_id: int):
    """
    Remove a product from the cart.
    """
    try:
        result = cart_service.remove_product_from_cart(cart_id, product_id)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error removing product from cart: {str(e)}'
        }), 500


@cart_bp.route('/<cart_id>/clear', methods=['POST'])
def clear_cart(cart_id: str):
    """
    Clear all items from the cart.
    """
    try:
        result = cart_service.clear_cart(cart_id)
        
        status_code = 200 if result['success'] else 404
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error clearing cart: {str(e)}'
        }), 500


@cart_bp.route('/<cart_id>/validate', methods=['GET'])
def validate_cart(cart_id: str):
    """
    Validate cart for checkout (check stock availability, active products, etc.).
    """
    try:
        result = cart_service.validate_cart_for_checkout(cart_id)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error validating cart: {str(e)}'
        }), 500


# Error handlers for the blueprint
@cart_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404


@cart_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'message': 'Method not allowed'
    }), 405
