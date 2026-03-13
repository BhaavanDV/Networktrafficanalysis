import pyshark
import asyncio

def start_live_capture(callback):
    # 🔹 Create an event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    capture = pyshark.LiveCapture(interface='Wi-Fi')

    prev_time = None

    for packet in capture.sniff_continuously():
        try:
            timestamp = float(packet.sniff_timestamp)
            size = int(packet.length)
            protocol = packet.transport_layer

            if prev_time is None:
                inter_arrival = 0
            else:
                inter_arrival = timestamp - prev_time

            prev_time = timestamp

            features = {
                "packet_size": size,
                "protocol": protocol,
                "inter_arrival": inter_arrival,
                "src_ip": packet.ip.src if hasattr(packet, "ip") else "unknown",
                "dst_ip": packet.ip.dst if hasattr(packet, "ip") else "unknown"
            }

            callback(features)

        except Exception as e:
            print("Packet processing error:", e)