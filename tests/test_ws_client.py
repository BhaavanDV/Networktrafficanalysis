import asyncio
import json
import websockets

async def send_packets():
    uri = "ws://127.0.0.1:8000/ws_packets"  # Your FastAPI WS endpoint
    async with websockets.connect(uri) as websocket:
        # Example packet data
        packets = [
            {
                "timestamp": "2026-02-27 09:00:00",
                "src_ip": "192.168.0.1",
                "dst_ip": "10.0.0.1",
                "bytes_sent": 1500,
                "bytes_received": 300,
                "packet_size": 1500,
                "protocol": "TCP",
                "inter_arrival": 0.05
            },
            {
                "timestamp": "2026-02-27 09:01:00",
                "src_ip": "192.168.0.2",
                "dst_ip": "10.0.0.2",
                "bytes_sent": 1200,
                "bytes_received": 400,
                "packet_size": 1200,
                "protocol": "UDP",
                "inter_arrival": 0.02
            }
        ]

        await websocket.send(json.dumps(packets))
        print("Sent packets to WebSocket")

        # Receive predictions
        response = await websocket.recv()
        print("Received from server:", response)

# Run the client
if __name__ == "__main__":
    asyncio.run(send_packets())