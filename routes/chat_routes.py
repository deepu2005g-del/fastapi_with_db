from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from models import User
from schemas.chat_schemas import ChatCreate, ChatResponse, MessageCreate, MessageResponse
from repositories.chat_repo import ChatRepo
from utils.deps import get_current_user
from utils.ai_response import get_completion

router = APIRouter(prefix="/chats", tags=["chats"])

@router.post("/", response_model=ChatResponse)
def create_chat(chat: ChatCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chat_repo = ChatRepo(db)
    return chat_repo.create_chat(user_id=current_user.id, title=chat.title)

@router.get("/", response_model=List[ChatResponse])
def get_chats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chat_repo = ChatRepo(db)
    return chat_repo.get_chats(user_id=current_user.id)

@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(chat_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chat_repo = ChatRepo(db)
    chat = chat_repo.get_chat(chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.delete("/{chat_id}")
def delete_chat(chat_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chat_repo = ChatRepo(db)
    success = chat_repo.delete_chat(chat_id=chat_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"message": "Chat deleted"}

@router.post("/{chat_id}/ask", response_model=MessageResponse)
def ask_ai(chat_id: int, request: MessageCreate, system_prompt: str = "You are a helpful assistant.", current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chat_repo = ChatRepo(db)
    chat = chat_repo.get_chat(chat_id=chat_id, user_id=current_user.id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
        
    # User message
    chat_repo.add_message(chat_id=chat_id, role="user", content=request.content)
    
    # AI response
    try:
        response_text = get_completion(request.content, system_prompt)
        ai_message = chat_repo.add_message(chat_id=chat_id, role="ai", content=response_text)
        return ai_message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
