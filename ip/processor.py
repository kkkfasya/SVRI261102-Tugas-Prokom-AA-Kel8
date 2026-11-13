import socket
import sys
from datetime import datetime
import os

from pretty_print import print_banner, print_section_header
from .const import TOTAL_PORTS


def connect_to_ip(target, timeout_sec=3):
    try:
        s = socket.create_connection((target, 80), timeout=timeout_sec)
        s.close()

    except OSError as err:
        raise err


def check_open_ports(target_ip, port_count):
    open_ports = {target_ip: []}

    for port in range(1, port_count + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Set a timeout of 1 second for the connection attempt

        # Attempt to connect to the port on the target IP address
        result = s.connect_ex((target_ip, port))
        # If the connection attempt is successful (result is 0), mark the port as open
        if result == 0:
            open_ports[target_ip].append(
                port
            )  # Add the open port to the list for the corresponding IP address
            print(f"[+] Port {port} is open")
        s.close()

    return open_ports


# return boolean, false berarti tidak ada port
def save_port_to_file(target_ip, ports, output_dir=""):
    if len(ports[target_ip]) < 1:
        return False
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    ip_address = target_ip.replace(".", "-")
    if output_dir:
        file_path = os.path.join(output_dir, f"open_ports_{ip_address}_{date_time}.txt")
    else:
        file_path = f"open_ports_{ip_address}_{date_time}.txt"
    try:
        # Try to save the output file
        with open(file_path, "w") as file:
            for port in ports[target_ip]:
                file.write(str(port) + "\n")
        print_banner(
            f"[v] Open ports list for {target_ip} saved to file '{file_path}'",
        )
    except PermissionError as err:
        raise err


def scan_target_ips(targets, output_dir=""):
    open_ports = {}  # Dictionary to store open ports for each IP address
    try:
        # Iterate over each target IP address
        for idx, ip in enumerate(targets, 1):
            ip = ip.strip()  # Remove any leading or trailing spaces from the IP address
            open_ports[
                ip
            ] = []  # Initialize an empty list to store open ports for the IP address
            print_section_header(
                f"Scanning Target ({idx}/{len(targets)}): {ip}", char="*"
            )

            try:
                connect_to_ip(ip)
            except (socket.timeout, ConnectionRefusedError, socket.gaierror):
                print_section_header(
                    f"[x] Failed to connect to {ip}. Please check the IP address and try again.",
                    char="-",
                )
                continue

            # Iterate over each port (from 1 to 65535) and attempt to connect
            open_ports = check_open_ports(ip, TOTAL_PORTS)
            if len(open_ports) < 1:
                # If no open ports are found for the target, display a message
                print_section_header(
                    f"[x] No open ports found for {ip}. The castle remains unbreachable!",
                    char="-",
                )

            # If open ports are found for the target, save the list to a file
            try:
                save_port_to_file(ip, open_ports, output_dir)

            except PermissionError:
                print_banner(
                    f"[x] Permission denied. Unable to save open ports list for {ip}. Printing to screen instead:"
                )
                for port in open_ports[ip]:
                    print(port)

    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C)
        print("\n[x] Exiting Program!!")
        sys.exit()
    except socket.error:
        # Handle socket error
        print("\n[x] Server not responding!!")
        sys.exit()
