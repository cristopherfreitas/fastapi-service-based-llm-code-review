from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User

class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> UserResponse:
        # Check if user already exists
        existing_user = self.user_repository.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError(f"User with email {user_data.email} already exists")
        
        # Create new user
        db_user = self.user_repository.create_user(user_data)
        return UserResponse.model_validate(db_user)

    def get_user_by_id(self, user_id: int) -> UserResponse:
        db_user = self.user_repository.get_user_by_id(user_id)
        if not db_user:
            raise ValueError(f"User with id {user_id} not found")
        return UserResponse.model_validate(db_user)