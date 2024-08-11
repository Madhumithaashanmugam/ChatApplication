from services.connection_manager import ConnectionManager
from fastapi import WebSocket,WebSocketDisconnect,Depends
from apis.message_api import message_api
from models.chat.models import Chat
from models.users.models import User
from services.message_service import CreateMessage,create_message, get_messages_for_user
from config.db.session import get_db
from sqlalchemy.orm import Session

manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, sender_id: str, db: Session = Depends(get_db)):
    await manager.connect(sender_id, websocket)
    

    messages = get_messages_for_user(db, sender_id)
    for message in messages:
        await websocket.send_text(f"From {message.sender_id if message.sender_id != sender_id else message.receptor_id}: {message.content_text}")
    
    try:
        while True:
            data = await websocket.receive_text()
            chat_id, receptor_id, content_text = data.split('|')
            

            Chat = db.query(Chat).filter(Chat.id == chat_id).first()
            if not Chat:
                await websocket.send_text("Invalid Chat ID.")
                continue
            
            User = db.query(User).filter(User.id == sender_id).first()
            User_1 = db.query(User).filter(User.id == receptor_id).first()
            if not User or not User_1:
                await websocket.send_text("Invalid User ID(s).")
                continue
            

            message = CreateMessage(
                Chat_id=chat_id,
                sender_id=sender_id,
                receptor_id=receptor_id,
                content_text=content_text,
                created_datetime=message.created_datetime
                
            )
            await create_message(db, message)
            

            await manager.send_personal_message(sender_id, receptor_id, f"From {sender_id}: {content_text}")
    except WebSocketDisconnect:
        manager.disconnect(sender_id, websocket)
            