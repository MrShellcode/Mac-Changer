import subprocess
import re
import os
import sys
import random
import netifaces

def check_root_privileges():
    if os.geteuid() != 0:
        print("\nError: Only root can run this script.\n")
        sys.exit(1)  # Exit with a non-zero status code

def generate_random_mac():
    # Generate a random MAC address
    random_mac = ":".join(f"{random.randint(0, 255):02X}" for _ in range(6))
    return random_mac
    
def validate_mac(mac):
    # Regular expression to validate MAC address format
    pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    return re.match(pattern, mac)



def change_mac(interface, new_mac):
    try:
        if new_mac.lower() == "random":
            new_mac = generate_random_mac()
            print(f"Generated random MAC address: {new_mac}")

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
    
    interface_list = netifaces.interfaces()
    print("Your System Interface is : ",interface_list)
    interface = input("Enter the network interface name (e.g., eth0): ")
    new_mac = input("Enter the new MAC address (format: XX:XX:XX:XX:XX:XX or 'random'): ")
    if new_mac.lower() == "random":
        print("Generating a random MAC address...")
        new_mac = generate_random_mac()
    print("Your New Mac Adress is ", new_mac)
    change_mac(interface, new_mac)
