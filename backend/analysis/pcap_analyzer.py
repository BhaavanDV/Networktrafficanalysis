import pyshark

def analyze_pcap(file):

    capture = pyshark.FileCapture(file)

    packets = []

    for packet in capture:

        try:
            packets.append({
                "src_ip": packet.ip.src,
                "dst_ip": packet.ip.dst,
                "protocol": packet.transport_layer
            })

        except:
            continue

    return packets