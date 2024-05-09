import subprocess
import re
import os
import sys

def check_root_privileges():
    if os.geteuid() != 0:
        print("\nError: Only root can run this script.\n")
        sys.exit(1)  # Exit with a non-zero status code

def validate_mac(mac):
    # Regular expression to validate MAC address format
    pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    return re.match(pattern, mac)

def change_mac(interface, new_mac):
    try:
        # Validate the new MAC address
        if not validate_mac(new_mac):
            print("Invalid MAC address format. Please use XX:XX:XX:XX:XX:XX.")
            return

        # Shut down the interface
        subprocess.run(["ifconfig", interface, "down"])

        # Change the interface's hardware address
        subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])

        # Bring the interface back up
        subprocess.run(["ifconfig", interface, "up"])

        print(f"MAC address changed to {new_mac} for {interface}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_root_privileges()
    interface = input("Enter the network interface name (e.g., eth0): ")
    new_mac = input("Enter the new MAC address (format: XX:XX:XX:XX:XX:XX): ")
    print("You entered:", new_mac)
    change_mac(interface, new_mac)

