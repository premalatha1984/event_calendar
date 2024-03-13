from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.user import models



user_router = APIRouter()


@user_router.post('/create_user')
# Function to create a new user
def create_user(user_data: dict, db: Session= Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user_data['email']).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email must be unique")
    user_data['created_by_id']=1
    user = models.User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Function to retrieve all users
@user_router.get('/list_all_user')
def get_all_users(db: Session= Depends(get_db)):
    return db.query(models.User).all()

# Function to retrieve a user by ID
def get_user_by_id(user_id: int, db: Session= Depends(get_db)):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Function to retrieve a user by username
def get_user_by_username(username: str, db: Session= Depends(get_db)):
    return db.query(models.User).filter(models.User.username == username).first()

# Function to update a user
def update_user(user_id: int, user_data: dict, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        db.commit()
    return user

# Function to delete a user
def delete_user(user_id: int, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user