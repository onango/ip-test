import os
import socket
from undetected_chromedriver import Chrome, ChromeOptions
from stem import Signal
from stem.control import Controller

def get_ip_address():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return ip_address

def renew_tor_ip():
    tor_password = os.environ.get("TOR_CONTROL_PASSWORD", "")
    if tor_password:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=tor_password)
            controller.signal(Signal.NEWNYM)

if __name__ == "__main__":
    ip = get_ip_address()
    print(f"IP Address: {ip}")

    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--proxy-server=socks5://127.0.0.1:9050')

    with Chrome(options=options) as driver:
        driver.get("https://example.com")

    renew_tor_ip()
