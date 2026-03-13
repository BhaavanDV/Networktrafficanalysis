# backend/api/socket_routes.py
from fastapi import APIRouter, WebSocket
from services.websocket_service import WebSocketManager

router = APIRouter()
ws_manager = WebSocketManager()

@router.websocket("/ws/predictions")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.send_message(f"Echo: {data}")
    except Exception:
        ws_manager.disconnect(websocket)