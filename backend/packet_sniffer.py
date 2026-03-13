from scapy.all import sniff, IP, TCP, UDP
import datetime

from server import add_packet

def process_packet(packet):

    if IP in packet:

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        size = len(packet)

        protocol = "OTHER"

        if TCP in packet:
            protocol = "TCP"
        elif UDP in packet:
            protocol = "UDP"

        packet_data = {
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "protocol": protocol,
            "packet_size": size,
            "prediction": 0
        }

        add_packet(packet_data)

def start_sniffing():
    sniff(prn=process_packet, store=False)