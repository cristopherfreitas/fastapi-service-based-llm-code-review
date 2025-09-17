from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
import re

# Create tables
User.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to User Management API"}

# GOOD PATTERN: Clean endpoint with service layer
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    try:
        return user_service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ANTI-PATTERN: Business logic embedded directly in endpoint
@app.post("/users/antipattern/", response_model=UserResponse)
def create_user_antipattern(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    ANTI-PATTERN EXAMPLE: This endpoint demonstrates what NOT to do.
    All business logic is embedded directly in the endpoint instead of being in a service layer.
    """
    
    # Email validation logic that should be in a service
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user_data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Domain blacklist check that should be in a service
    blacklisted_domains = ["tempmail.com", "throwaway.email", "10minutemail.com"]
    email_domain = user_data.email.split("@")[1].lower()
    if email_domain in blacklisted_domains:
        raise HTTPException(status_code=400, detail=f"Email domain {email_domain} is not allowed")
    
    # Direct database query that should be in a repository
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Name validation that should be in a service
    if len(user_data.name) < 2:
        raise HTTPException(status_code=400, detail="Name must be at least 2 characters long")
    
    if len(user_data.name) > 100:
        raise HTTPException(status_code=400, detail="Name must not exceed 100 characters")
    
    # Direct database manipulation that should be in a repository
    new_user = User(
        name=user_data.name.strip(),  # Business logic: trimming
        email=user_data.email.lower()  # Business logic: normalizing email
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Post-creation logic that should be in a service
    print(f"TODO: Send welcome email to {new_user.email}")
    print(f"TODO: Create audit log entry for user {new_user.id}")
    
    return new_user

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    try:
        return user_service.get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))