from fastapi import WebSocket
from typing import Dict, List

class ChatConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        self.active_connections[user_id].remove(websocket)

    async def send_to_user(self, user_id: int, message: dict):
        for ws in self.active_connections.get(user_id, []):
            await ws.send_json(message)

    async def broadcast_admin(self, message: dict):
        # 管理画面用（user_id=0 とかでもOK）
        for sockets in self.active_connections.values():
            for ws in sockets:
                await ws.send_json(message)

manager = ChatConnectionManager()
