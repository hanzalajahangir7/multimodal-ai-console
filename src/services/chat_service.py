from sqlalchemy.orm import Session
from src.models.models import ChatSession, ChatMessage
from src.db.vector_store import vector_store
from src.utils.llm import get_aclient
import json

class ChatService:
    @staticmethod
    async def get_response(session_id: int, user_query: str, db: Session):
        # 1. Retrieve Context from Vector DB
        results = vector_store.query_similar(user_query, n_results=3)
        context_docs = results['documents'][0] if results['documents'] else []
        context_str = "\n\n".join(context_docs)
        
        # 2. Retrieve Conversation History (Last 10 messages)
        history_msgs = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.timestamp.desc()).limit(10).all()
        history_msgs.reverse() # Oldest first
        
        # 3. Construct Messages needed for OpenAI
        messages = [
            {"role": "system", "content": f"You are a helpful AI assistant. Use the following context to answer if relevant:\n\n{context_str}"}
        ]
        
        for msg in history_msgs:
            messages.append({"role": msg.role, "content": msg.content})
            
        messages.append({"role": "user", "content": user_query})
        
        # 4. Call LLM
        aclient = get_aclient()
        response = await aclient.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        ai_response = response.choices[0].message.content
        
        # 5. Store in DB
        user_msg_db = ChatMessage(session_id=session_id, role="user", content=user_query)
        ai_msg_db = ChatMessage(session_id=session_id, role="assistant", content=ai_response)
        db.add(user_msg_db)
        db.add(ai_msg_db)
        db.commit()
        
        return ai_response

    @staticmethod
    def create_session(title: str, db: Session):
        session = ChatSession(title=title)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def get_sessions(db: Session):
        return db.query(ChatSession).all()
    
    @staticmethod
    def get_chat_history(session_id: int, db: Session):
        return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.timestamp).all()
