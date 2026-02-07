from fastapi import APIRouter
from fastapi import Depends
from db import get_db
from repositories.user_repo import UserRepo
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/signup")
def signup(db:Session = Depends(get_db)):
    user_repo = UserRepo(db)
    user_repo.add_user()
    return {"message": "User signed up successfully"}

@router.post("/login")
def login():
    return {"message": "User logged in successfully"}
