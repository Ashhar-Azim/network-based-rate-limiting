import time
import logging
from collections import defaultdict

# Configure logging
logging.basicConfig(filename='rate_limiting.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Define a dictionary to store IP addresses and their request counts for each port
ip_port_request_count = defaultdict(lambda: defaultdict(list))

# Define a set to store whitelisted IP addresses
whitelisted_ips = set()

# User interactions to set rate limiting parameters
time_frame = int(input("Enter the time frame (in seconds): "))
threshold = int(input("Enter the request threshold: "))
while True:
    ip = input("Enter a whitelisted IP address (or type 'done' to finish): ")
    if ip.lower() == 'done':
        break
    whitelisted_ips.add(ip)

def limit_requests(ip, port):
    current_time = int(time.time())

    # Check if the IP address is whitelisted
    if ip in whitelisted_ips:
        return False

    # Add the current request timestamp to the IP's request history for the specific port
    ip_port_request_count[ip][port].append(current_time)

    # Remove timestamps older than the time frame
    ip_port_request_count[ip][port] = [t for t in ip_port_request_count[ip][port] if current_time - t <= time_frame]

    # Check if the request count exceeds the threshold
    if len(ip_port_request_count[ip][port]) > threshold:
        return True

    return False
