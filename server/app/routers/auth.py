from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Token
from ..models import User
from ..oauth2 import create_access_token
from ..utils import hash, verify
from ..schemas import CreateUser, ResponseUser

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/register', response_model=ResponseUser, status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = User(**user.model_dump()) 
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)

    return new_user

@router.get('/user/{id}', response_model=ResponseUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")

    return user

@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == user_credentials.username).first()

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"user with username: {user_credentials.username} does not exist")

    if not verify(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")

    access_token = create_access_token(data={"user_id": user.id, "username": user.username })

    return {"access_token": access_token, "token_type": "bearer"}

