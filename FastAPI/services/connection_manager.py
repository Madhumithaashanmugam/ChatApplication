# from typing import Dict, List
# from fastapi import WebSocket

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: Dict[str, List[WebSocket]] = {}

#     async def connect(self, user_id: str, websocket: WebSocket):
#         await websocket.accept()
#         if user_id not in self.active_connections:
#             self.active_connections[user_id] = []
#         self.active_connections[user_id].append(websocket)

#     def disconnect(self, user_id: str, websocket: WebSocket):
#         self.active_connections[user_id].remove(websocket)
#         if not self.active_connections[user_id]:
#             del self.active_connections[user_id]

#     async def send_personal_message(self, user_id: str, message: str):
#         if user_id in self.active_connections:
#             for connection in self.active_connections[user_id]:
#                 await connection.send_text(message)

#     async def broadcast(self, message: str):
#         for user_id, connections in self.active_connections.items():
#             for connection in connections:
#                 await connection.send_text(message)
from typing import Dict, List
from fastapi import WebSocket
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        self.active_connections[user_id].remove(websocket)
        if not self.active_connections[user_id]:
            del self.active_connections[user_id]

    # async def send_personal_message(self, user_id: str, message: str):
    #     if user_id in self.active_connections:
    #         for connection in self.active_connections[user_id]:
    #             await connection.send_text(message)
    
    async def send_personal_message(self, sender_id: str, user_id: str, message: str, created_datetime: datetime):
      if user_id in self.active_connections:
        formatted_message = f"From: {sender_id}, Time: {created_datetime}, Message: {message}"
        for connection in self.active_connections[user_id]:
            await connection.send_text(formatted_message)

    async def broadcast(self, message: str):
        for user_id, connections in self.active_connections.items():
            for connection in connections:
                await connection.send_text(message)
