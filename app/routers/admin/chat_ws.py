from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.ws.chat import manager

router = APIRouter()

@router.websocket("/ws/chat/{user_id}")
async def chat_ws(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()

            # 管理画面・Flutter双方に配信
            await manager.send_to_user(user_id, data)
            await manager.broadcast_admin(data)

    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
