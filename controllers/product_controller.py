from flask import Blueprint, request, jsonify
from typing import Optional
from services.product_service import ProductService
from repositories.product_repository import ProductRepository

# Create blueprint
product_bp = Blueprint('products', __name__, url_prefix='/api/products')

# Initialize dependencies
product_repository = ProductRepository()
product_service = ProductService(product_repository)


@product_bp.route('', methods=['GET'])
def get_products():
    """
    Get all products with optional filtering.
    Query parameters:
    - category: Filter by category
    - search: Search in name and description
    - limit: Limit number of results
    - offset: Offset for pagination
    """
    try:
        category = request.args.get('category')
        search = request.args.get('search')
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int, default=0)
        
        products = product_service.get_all_products(category=category, search=search)
        
        # Apply pagination if limit is specified
        if limit:
            total = len(products)
            products = products[offset:offset + limit]
            
            return jsonify({
                'success': True,
                'data': products,
                'pagination': {
                    'total': total,
                    'limit': limit,
                    'offset': offset,
                    'has_more': offset + limit < total
                }
            }), 200
        
        return jsonify({
            'success': True,
            'data': products,
            'total': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving products: {str(e)}'
        }), 500


@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product_detail(product_id: int):
    """
    Get detailed information about a specific product.
    """
    try:
        product = product_service.get_product_detail(product_id)
        
        if product:
            return jsonify({
                'success': True,
                'data': product
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Product not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving product: {str(e)}'
        }), 500


@product_bp.route('/<int:product_id>/availability', methods=['GET'])
def check_product_availability(product_id: int):
    """
    Check product availability.
    Query parameters:
    - quantity: Quantity to check (default: 1)
    """
    try:
        quantity = request.args.get('quantity', type=int, default=1)
        
        if quantity <= 0:
            return jsonify({
                'success': False,
                'message': 'Quantity must be greater than 0'
            }), 400
        
        availability = product_service.check_product_availability(product_id, quantity)
        
        return jsonify({
            'success': True,
            'data': availability
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error checking availability: {str(e)}'
        }), 500


@product_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Get all product categories.
    """
    try:
        categories = product_service.get_product_categories()
        
        return jsonify({
            'success': True,
            'data': categories
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving categories: {str(e)}'
        }), 500


@product_bp.route('/search', methods=['GET'])
def search_products():
    """
    Search products by query.
    Query parameters:
    - q: Search query (required)
    """
    try:
        query = request.args.get('q')
        
        if not query:
            return jsonify({
                'success': False,
                'message': 'Search query is required'
            }), 400
        
        products = product_service.search_products(query)
        
        return jsonify({
            'success': True,
            'data': products,
            'total': len(products),
            'query': query
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error searching products: {str(e)}'
        }), 500


# Error handlers for the blueprint
@product_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404


@product_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'message': 'Method not allowed'
    }), 405
