import os

def parse_ip_list(ip_list):
    #Parse IP addresses from input list.
    ips = []
    for item in ip_list:
        # Check if the item is a file
        if os.path.isfile(item):
            with open(item, 'r') as file:
                ips.extend([ip.strip() for ip in file.read().splitlines() if ip.strip()])
        else:
            ips.extend(item.split(','))
    return ips
