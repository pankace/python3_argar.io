import netifaces # dynamic ip selections
import socket
from server_logger import logger

class NetworkUtils:
    @staticmethod
    def get_network_ip():
        try:
            for interface in netifaces.interfaces():
                # skip loopback
                if interface == "lo0":
                    continue
                addresses = netifaces.ifaddresses(interface)
                # check ipv4
                if netifaces.AF_INET in addresses:
                    ipv4_info = addresses[netifaces.AF_INET][0]
                    ip_address = ipv4_info['addr']
                    if not ip_address.startswith("127."):
                        return ip_address
        except Exception as e:
            print(f"Error occurred while fetching network IP: {e}")
            logger.error(f"Error occurred while fetching network IP: {e}")
        # fallback address
        return socket.gethostbyname(socket.gethostname())
