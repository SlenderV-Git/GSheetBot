from .get_session import Session
from .models import ChatID

def check_id(chat_id):
    session = Session()
    chat = session.query(ChatID).filter_by(chat_id=chat_id).first()
    session.close()
    return chat

def add_id(chat_id):
    new_chat = ChatID(chat_id=chat_id)
    session = Session()
    session.add(new_chat)
    session.commit()
    session.close()
    
def delete_id(chat_id : ChatID):
    session = Session()
    session.delete(chat_id)
    session.commit()
    session.close()
    
def get_all():
    session = Session()
    chats = session.query(ChatID).all()
    session.close()
    return chats