from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

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