#!/usr/bin/env python3
"""
Network utilities for interface detection and selection
"""

import platform

# Try import netifaces (optional dependency)
try:
    import netifaces
    NETIFACES_AVAILABLE = True
except ImportError:
    NETIFACES_AVAILABLE = False

from colorama import Fore, Style


def get_active_interfaces():
    """Get list of active network interfaces with IP addresses"""
    if not NETIFACES_AVAILABLE:
        return []
    
    active = []
    
    try:
        for iface in netifaces.interfaces():
            # Skip loopback
            if iface == 'lo':
                continue
            
            # Check if interface has IPv4 address
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                ip = addrs[netifaces.AF_INET][0]['addr']
                active.append({
                    'name': iface,
                    'ip': ip
                })
    except Exception as e:
        print(f"{Fore.RED}[!] Error detecting interfaces: {e}{Style.RESET_ALL}")
        return []
    
    return active


def should_ask_interface():
    """Check if we should ask user for interface selection"""
    system = platform.system()
    
    # Only Linux supports interface binding
    if system != "Linux":
        return False
    
    # Check if netifaces is available
    if not NETIFACES_AVAILABLE:
        return False
    
    # Check if there are multiple active interfaces
    try:
        interfaces = get_active_interfaces()
        # Need at least 2 interfaces for advanced mode to make sense
        return len(interfaces) >= 2
    except:
        return False


def ask_network_mode():
    """Ask user to choose between auto and advanced network mode"""
    print("\n" + "="*60)
    print(f"{Fore.CYAN}[*] Network Mode Selection{Style.RESET_ALL}")
    print("="*60)
    print(f"{Fore.GREEN}[1] Auto (recommended){Style.RESET_ALL} - Use default routing")
    print(f"{Fore.YELLOW}[2] Advanced{Style.RESET_ALL} - Select specific network interface")
    print("="*60)
    
    choice = input(f"{Fore.CYAN}[?] Choose mode (1/2): {Style.RESET_ALL}").strip()
    return choice == "2"


def select_interface():
    """Let user select which network interface to use for testing"""
    interfaces = get_active_interfaces()
    
    if not interfaces:
        print(f"{Fore.RED}[!] No active interfaces found!{Style.RESET_ALL}")
        return None
    
    print("\n" + "="*60)
    print(f"{Fore.CYAN}[*] Available Network Interfaces{Style.RESET_ALL}")
    print("="*60)
    
    for i, iface in enumerate(interfaces, 1):
        print(f"{Fore.GREEN}[{i}]{Style.RESET_ALL} {iface['name']:10} - {iface['ip']}")
    
    print("="*60)
    
    while True:
        try:
            choice = int(input(f"{Fore.CYAN}[?] Select interface (1-{len(interfaces)}): {Style.RESET_ALL}"))
            if 1 <= choice <= len(interfaces):
                selected = interfaces[choice - 1]
                print(f"{Fore.GREEN}[+] Using interface: {selected['name']} ({selected['ip']}){Style.RESET_ALL}")
                return selected['name']
        except ValueError:
            pass
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Cancelled{Style.RESET_ALL}")
            return None
        
        print(f"{Fore.RED}[!] Invalid choice!{Style.RESET_ALL}")


def get_network_interface():
    """
    Main function to get network interface for testing
    Returns: interface name (str) or None for auto mode
    """
    # Check if we should offer advanced mode
    if not should_ask_interface():
        print(f"{Fore.GREEN}[+] Using auto mode (default routing){Style.RESET_ALL}")
        return None
    
    # Ask user to choose mode
    use_advanced = ask_network_mode()
    
    if not use_advanced:
        print(f"{Fore.GREEN}[+] Using auto mode (default routing){Style.RESET_ALL}")
        return None
    
    # Let user select interface
    return select_interface()
