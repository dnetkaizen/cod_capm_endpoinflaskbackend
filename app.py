from flask import Flask, jsonify
from flask_cors import CORS
from controllers.product_controller import product_bp
from controllers.cart_controller import cart_bp


def create_app():
    """Application factory pattern for creating Flask app."""
    app = Flask(__name__)
    
    # Configuration
    app.config['DEBUG'] = True
    app.config['JSON_SORT_KEYS'] = False
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Flask E-commerce API',
            'version': '1.0.0',
            'endpoints': {
                'products': {
                    'get_all': 'GET /api/products',
                    'get_detail': 'GET /api/products/<id>',
                    'check_availability': 'GET /api/products/<id>/availability',
                    'get_categories': 'GET /api/products/categories',
                    'search': 'GET /api/products/search'
                },
                'cart': {
                    'create_or_get': 'POST /api/cart',
                    'get_cart': 'GET /api/cart/<cart_id>',
                    'add_item': 'POST /api/cart/<cart_id>/items',
                    'update_item': 'PUT /api/cart/<cart_id>/items/<product_id>',
                    'remove_item': 'DELETE /api/cart/<cart_id>/items/<product_id>',
                    'clear_cart': 'POST /api/cart/<cart_id>/clear',
                    'validate_cart': 'GET /api/cart/<cart_id>/validate'
                }
            }
        })
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'API is running successfully'
        })
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Resource not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Bad request'
        }), 400
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
