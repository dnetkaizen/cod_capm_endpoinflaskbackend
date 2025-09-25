from repositories.user_repository import UserRepository
import jwt
import datetime
from flask import current_app

class UserService:
    """Service layer for user business logic."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def signup(self, user_data: dict):
        """User signup."""
        if self.user_repository.get_user_by_username(user_data['username']):
            return {'success': False, 'message': 'User already exists'}

        self.user_repository.create_user(user_data)
        return {'success': True, 'message': 'User created successfully'}

    def login(self, user_data: dict):
        """User login."""
        user = self.user_repository.get_user_by_username(user_data['username'])
        if user and user.check_password(user_data['password']):
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, current_app.config['SECRET_KEY'])
            return {'success': True, 'token': token, 'user': {"id": user.id, "name": user.username,"email": user.username}}
        return {'success': False, 'message': 'Invalid credentials'}
