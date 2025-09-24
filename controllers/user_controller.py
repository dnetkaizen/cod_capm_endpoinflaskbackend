from flask import Blueprint, request, jsonify
from services.user_service import UserService
from repositories.user_repository import UserRepository

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Initialize dependencies
user_repository = UserRepository()
user_service = UserService(user_repository)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    User signup.
    Request body:
    - username: Username (required)
    - password: Password (required)
    """
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400

        result = user_service.signup(data)
        status_code = 201 if result['success'] else 400
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error during signup: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login.
    Request body:
    - username: Username (required)
    - password: Password (required)
    """
    try:
        data = request.get_json()
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400

        result = user_service.login(data)
        status_code = 200 if result.get('token') else 401
        return jsonify(result), status_code

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error during login: {str(e)}'}), 500
