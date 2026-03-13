ip_ports = {}

def detect_port_scan(src_ip, port):

    if src_ip not in ip_ports:
        ip_ports[src_ip] = set()

    ip_ports[src_ip].add(port)

    if len(ip_ports[src_ip]) > 15:
        return True

    return False