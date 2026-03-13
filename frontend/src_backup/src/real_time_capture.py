from scapy.all import sniff
import pandas as pd
from threading import Thread

packets_list = []

def packet_callback(pkt):
    # Example: just store summary
    packets_list.append(str(pkt.summary()))

def start_capture():
    sniff(prn=packet_callback, count=100)  # Capture 100 packets
    print("Packet capture finished.")

def get_recent_packets():
    # Return last 10 packets
    return packets_list[-10:]