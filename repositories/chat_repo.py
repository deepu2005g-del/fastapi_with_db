from sqlalchemy.orm import Session
from models import Chat, Message

class ChatRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_chat(self, user_id: int, title: str):
        db_chat = Chat(user_id=user_id, title=title)
        self.db.add(db_chat)
        self.db.commit()
        self.db.refresh(db_chat)
        return db_chat

    def get_chats(self, user_id: int):
        return self.db.query(Chat).filter(Chat.user_id == user_id).order_by(Chat.updated_at.desc()).all()

    def get_chat(self, chat_id: int, user_id: int):
        return self.db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user_id).first()

    def delete_chat(self, chat_id: int, user_id: int):
        chat = self.get_chat(chat_id, user_id)
        if chat:
            self.db.delete(chat)
            self.db.commit()
            return True
        return False

    def add_message(self, chat_id: int, role: str, content: str):
        db_message = Message(chat_id=chat_id, role=role, content=content)
        self.db.add(db_message)
        
        # Update chat updated_at
        chat = self.db.query(Chat).filter(Chat.id == chat_id).first()
        if chat:
            from datetime import datetime
            chat.updated_at = datetime.utcnow()
            
        self.db.commit()
        self.db.refresh(db_message)
        return db_message
