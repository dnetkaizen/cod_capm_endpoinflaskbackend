from models.user import User
from models.database import db

class UserRepository:
    """Repository for user data access."""

    def get_user_by_username(self, username: str) -> User:
        """Get a user by username."""
        return User.query.filter_by(username=username).first()

    def create_user(self, user_data: dict) -> User:
        """Create a new user."""
        new_user = User(username=user_data['username'])
        new_user.set_password(user_data['password'])
        db.session.add(new_user)
        db.session.commit()
        return new_user
