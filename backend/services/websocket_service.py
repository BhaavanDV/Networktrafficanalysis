import socketio

# Async Socket.IO server
sio = socketio.AsyncServer(async_mode='asgi')
# ASGI app to integrate with FastAPI
from fastapi import FastAPI
app = FastAPI()
socket_app = socketio.ASGIApp(sio, app)

# Event example
@sio.event
async def connect(sid, environ):
    print(f"[Socket.IO] Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"[Socket.IO] Client disconnected: {sid}")