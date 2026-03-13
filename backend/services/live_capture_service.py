# backend/services/live_capture_service.py
# ==========================
import threading
import pyshark
import time

from services.feature_pipeline import build_features  # for feature extraction

# ==========================
# Live capture function
# ==========================
def start_capture_thread(callback, interface="Ethernet"):
    """
    Starts live packet capture on the given interface.
    Each packet is processed into features and sent to the callback.
    """
    def capture_loop():
        print(f"[Live Capture] Starting on interface: {interface}")
        try:
            cap = pyshark.LiveCapture(interface=interface)
            prev_time = None

            for pkt in cap.sniff_continuously():
                try:
                    pkt_len = int(pkt.length)
                    proto = int(pkt.highest_layer == "TCP") * 6 + int(pkt.highest_layer == "UDP") * 17
                    curr_time = float(pkt.sniff_timestamp)
                    iat = curr_time - prev_time if prev_time else 0
                    prev_time = curr_time

                    # Build feature dict
                    packet_features = {
                        "packet_length": pkt_len,
                        "inter_arrival": iat,
                        "protocol_encoded": proto,
                        "src_ip": getattr(pkt.ip, "src", "unknown") if hasattr(pkt, "ip") else "unknown",
                        "dst_ip": getattr(pkt.ip, "dst", "unknown") if hasattr(pkt, "ip") else "unknown"
                    }

                    # Optionally, extract more features using your build_features
                    features = build_features(packet_features)
                    packet_features.update(features)

                    # Call the callback
                    callback(packet_features)

                except Exception as e:
                    print("[Packet processing error]", e)

        except Exception as e:
            print("[Live Capture Error]", e)

    # Start capture in a daemon thread
    thread = threading.Thread(target=capture_loop, daemon=True)
    thread.start()
    print("[Live Capture] Thread started.")