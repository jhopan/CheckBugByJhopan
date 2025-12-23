#!/usr/bin/env python3
import subprocess
import time
import platform
import psutil
from colorama import Fore, Style

def kill_xray_processes():
    """Kill xray processes on any platform (Linux, Windows, macOS)"""
    system = platform.system()
    
    if system == "Windows":
        # Windows - using taskkill
        try:
            subprocess.run(["taskkill", "/F", "/IM", "xray.exe"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass
        # Alternative method using psutil
        try:
            for proc in psutil.process_iter(['name']):
                if 'xray' in proc.info['name'].lower():
                    proc.kill()
        except:
            pass
    else:
        # Linux/Unix/macOS - using pkill
        subprocess.run(["pkill", "-9", "-f", "xray"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-9", "xray"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(1)

def show_banner():
    banner = f"""
     _ _                           
    | | |__   ___  _ __   __ _ _ __  
 _  | | '_ \ / _ \| '_ \ / _` | '_ \ 
| |_| | | | | (_) | |_) | (_| | | | |
 \___/|_| |_|\___/| .__/ \__,_|_| |_|
                  |_|                
{Fore.YELLOW}Xray v25.12.8{Style.RESET_ALL}  {Fore.GREEN}v.3.2 Cross-Platform{Style.RESET_ALL}

Github : github.com/jhopan
Developed by Jhopan

{Fore.YELLOW}> Pastikan Akun VPN Stabil!
> Gunakan SSH dan Xray agar hasil lebih pasti!{Style.RESET_ALL}                         
"""
    return banner

def show_menu():
    print("\t")
    print(f"{Fore.YELLOW}[*] Pilih metode:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[1] (Xray) Address{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[2] (Xray) Wildcard{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[3] (Xray) SNI{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[4] (Xray) Onering{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[5] SSH WEBSOCKET{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[6] Subdomain Scanner (Perlu Internet){Style.RESET_ALL}")
    print(f"{Fore.CYAN}[7] Reverse IP Address (Perlu Internet){Style.RESET_ALL}")
    print(f"{Fore.CYAN}[8] (Xray) SNI v2 (SNI + Host){Style.RESET_ALL}")