import socket

def get_ip_address():
    # Get the hostname
    host_name = socket.gethostname()
    # Get the IP address associated with the hostname
    ip_address = socket.gethostbyname(host_name)
    return ip_address

if __name__ == "__main__":
    ip = get_ip_address()
    print(f"IP Address: {ip}")
