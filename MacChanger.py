#! /usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac Address")
    (options, arguments) = parser.parse_args()
    if not options.interface or not options.new_mac:
    parser.error("[-] Please specify both the interface and the new MAC address; use --help for more info")
    elif not options.interface:
        parser.error("[-] Please specify the interface; use --help for more info")
    elif not options.new_mac:
        parser.error("[-] Please specify the new MAC address; use --help for more info")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address of " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("Error: Could not Read MAC address.")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC is " + str(current_mac))
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] The Mac Address Successfully Changed to " + current_mac)
else:
    print("[-] The Mac Address didn't get changed ")