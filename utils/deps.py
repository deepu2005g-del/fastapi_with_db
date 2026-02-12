from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db import get_db
from utils.jwt_handler import verify_token
from repositories.user_repo import UserRepo
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token, token_type="access")
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("email")
    if email is None:
        raise credentials_exception
        
    user_repo = UserRepo(db)
    user = user_repo.get_user_by_email(email)
    if user is None:
        raise credentials_exception
        
    return user
