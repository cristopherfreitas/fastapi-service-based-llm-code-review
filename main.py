from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from typing import List
import csv
import io
import re

# Create tables
User.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to User Management API"}

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    try:
        return user_service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    try:
        return user_service.get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/users/bulk/", response_model=List[UserResponse])
def bulk_create_users(users: List[UserCreate], db: Session = Depends(get_db)):
    """Create multiple users at once"""
    created_users = []
    
    for user in users:
        # Check if email is valid
        if "@" not in user.email:
            continue  # Skip invalid emails silently
        
        # Check if user exists
        existing = db.query(User).filter(User.email == user.email).first()
        if existing:
            # Update existing user instead of creating new
            existing.name = user.name
            db.commit()
            created_users.append(existing)
        else:
            # Create new user
            new_user = User(
                name=user.name,
                email=user.email.lower()
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            created_users.append(new_user)
    
    return created_users

@app.post("/users/import-csv/")
def import_users_from_csv(csv_data: str, db: Session = Depends(get_db)):
    """Import users from CSV string"""
    
    # Parse CSV
    reader = csv.DictReader(io.StringIO(csv_data))
    
    success_count = 0
    failed_emails = []
    
    for row in reader:
        try:
            # Extract data
            name = row.get('name', '').strip()
            email = row.get('email', '').strip()
            
            # Basic validation
            if not name or not email:
                failed_emails.append(email)
                continue
                
            # Check email format
            if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                failed_emails.append(email)
                continue
            
            # Check if user already exists
            user = db.query(User).filter(User.email == email).first()
            
            if not user:
                # Create user directly
                user = User(name=name, email=email)
                db.add(user)
                db.commit()
                success_count += 1
            else:
                # Update existing user
                user.name = name
                db.commit()
                success_count += 1
                
        except Exception as e:
            # Generic error handling
            print(f"Error processing user: {str(e)}")
            failed_emails.append(row.get('email', 'unknown'))
            continue
    
    return {
        "message": f"Imported {success_count} users successfully",
        "failed": failed_emails
    }

@app.delete("/users/cleanup/")
def cleanup_duplicate_users(db: Session = Depends(get_db)):
    """Remove duplicate users keeping only the first one"""
    
    # Get all users
    all_users = db.query(User).all()
    
    seen_emails = {}
    deleted_count = 0
    
    for user in all_users:
        email_lower = user.email.lower()
        
        if email_lower in seen_emails:
            # Delete duplicate
            db.delete(user)
            deleted_count += 1
        else:
            seen_emails[email_lower] = user.id
    
    db.commit()
    
    return {"deleted": deleted_count, "remaining": len(seen_emails)}