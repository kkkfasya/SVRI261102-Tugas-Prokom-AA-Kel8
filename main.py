import argparse
import sys
import ip
from pretty_print import print_section_header
import pyfiglet
from datetime import datetime


def main():
    argparser = argparse.ArgumentParser(
        description="Port Scanner - Scan for open ports on specified IP addresses."
    )
    argparser.add_argument(
        "-i",
        "--ip",
        metavar="IP",
        type=str,
        nargs="+",
        help="Target IP addresses separated by comma or space.",
    )
    argparser.add_argument(
        "-f",
        "--file",
        metavar="FILE",
        type=str,
        help="Read target IP addresses from a file.",
    )
    argparser.add_argument(
        "-o",
        "--output-dir",
        metavar="DIRECTORY",
        type=str,
        help="Directory to save output files (if not defined will be the current path).",
    )
    args = argparser.parse_args()

    if not (args.ip or args.file):
        # Print help message and request to provide IP addresses
        print(
            "Please provide IP addresses as arguments or use the -help flag for more information."
        )
        print(
            "\nExamples: python3 scan.py -i 127.0.0.1\n\t  python3 scan.py -i 127.0.0.1, 172.17.0.2\n\t  python3 scan.py -f list_ip.txt -o /home/kali/Documents"
        )
        sys.exit()

    if args.file:
        with open(args.file, "r") as file:
            targets = [line.strip() for line in file.readlines() if line.strip()]
    else:
        targets = ip.parser.parse_ip_list(args.ip)

    # Remove empty IP addresses
    targets = [ip for ip in targets if ip]

    # Generate ASCII art banner for the port scanner
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER", font="slant")
    print(ascii_banner)

    # Print scanning information
    print_section_header(f"Scanning Targets: {', '.join(targets)}")
    print_section_header(f"Scanning started at: {str(datetime.now())}")
    ip.processor.scan_target_ips(targets, args.output_dir)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[x] Exiting Program!!")
        sys.exit()
