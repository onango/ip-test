import os
import socket
import time
import requests
from undetected_chromedriver import Chrome, ChromeOptions
from stem import Signal
from stem.control import Controller

def get_ip_address():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return ip_address

def renew_tor_ip():
    tor_password = os.environ.get("TOR_PASSWORD", "")
    if tor_password:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=tor_password)
            controller.signal(Signal.NEWNYM)

            # Give some time for the new circuit to be established
            time.sleep(5)

            # Print the current Tor IP address
            current_ip = get_current_tor_ip()
            print(f"Current Tor IP: {current_ip}")

def get_current_tor_ip():
    # Use a service like check.torproject.org to retrieve the current Tor IP
    ip_check_url = "https://check.torproject.org"
    
    try:
        response = requests.get(ip_check_url, proxies={'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'})
        response.raise_for_status()
        
        # Parse the response to extract the IP address
        current_ip = extract_ip_from_response(response.text)
        return current_ip
    except requests.exceptions.RequestException as e:
        print(f"Error checking Tor IP: {e}")
        return None

def extract_ip_from_response(response_text):
    # Use regular expressions or other parsing methods to extract the IP address from the response
    # This is an example using a simple regex
    import re
    match = re.search(r'Your IP address appears to be: (\d+\.\d+\.\d+\.\d+)', response_text)
    if match:
        return match.group(1)
    else:
        return None

if __name__ == "__main__":
    ip = get_ip_address()
    print(f"IP Address: {ip}")

    # options = ChromeOptions()
    # options.binary_location = "/usr/local/bin/chromedriver"  # Set the Chrome binary path directly

    # options.add_argument('--headless')
    # options.add_argument('--proxy-server=socks5://127.0.0.1:9050')

    # with Chrome(options=options) as driver:
    #     driver.get("https://example.com")

    renew_tor_ip()
