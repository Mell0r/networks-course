import socket
import netifaces

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print(f"IP-address: {ip_address}")

def get_subnet_mask():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for address in addresses[netifaces.AF_INET]:
                if 'netmask' in address:
                    return address['netmask']
    return None

print(f"Subnet mask: {get_subnet_mask()}")