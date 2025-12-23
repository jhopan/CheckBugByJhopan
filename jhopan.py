#!/usr/bin/env python3
#Jhopan v.3.2 use xray core v25.12.8 - by Jhopan
import os
import platform
from colorama import Fore, Style, init
from modules import parse, config, test_xray, ssh, subdomain, onering, revip
from utils import helpers
from core import check

init()

# Cross-platform clear screen
def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

clear_screen()

def main():
    print(helpers.show_banner())
    check.check_core()
    helpers.show_menu()
    choice = input(f"{Fore.YELLOW}[*] Pilih metode (1-8): {Style.RESET_ALL}").strip()
    
    if choice == "5":
        print(f"{Fore.CYAN}[!] Mode : SSH Websocket{Style.RESET_ALL}")
        ssh.ssh_connection()
        return
        
    if choice == "7":
    	print(f"{Fore.CYAN}[!] Mode : Reverse IP Address{Style.RESET_ALL}")
    	revip.reverse_ip()
    	return
    	
    if choice == "6":
        print(f"{Fore.CYAN}[!] Mode : Subdomain Scanner{Style.RESET_ALL}")
        subdomain.Subdomain()
        return
    
    modes = {
        "1": "Address",
        "2": "Wildcard", 
        "3": "SNI",
        "4": "Onering",
        "8": "SNI v2 (SNI + Host)"
    }
    
    if choice not in modes:
        print(f"{Fore.RED}[!] Pilihan tidak valid{Style.RESET_ALL}")
        return
    
    print(f"{Fore.CYAN}[!] Mode: {modes[choice]}{Style.RESET_ALL}")
    
    url = input(f"{Fore.YELLOW}[*] URL akun (vmess/trojan/vless): {Style.RESET_ALL}").strip()
    
    if not url:
        print(f"{Fore.RED}[!] URL diperlukan{Style.RESET_ALL}")
        return
    
    try:
        account = parse.parse_vmess_trojan_url(url)
        print(f"{Fore.GREEN}[+] Account : {account['protocol']} {account['address']}:{account['port']}{Style.RESET_ALL}")
        
        if choice == "4":  
            print(f"{Fore.GREEN}[+] XRAY ONERING READY!{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[+] XRAY READY!{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        return
    
    list_file = input(f"{Fore.YELLOW}[*] List IP/domain (txt): {Style.RESET_ALL}").strip()
    
    if not os.path.exists(list_file):
        print(f"{Fore.RED}[!] File tidak ditemukan{Style.RESET_ALL}")
        return
    
    # Get result file name based on list file name
    # e.g., wa.txt -> wa_result.txt, list.txt -> list_result.txt
    list_basename = os.path.splitext(os.path.basename(list_file))[0]
    result_file = f"{list_basename}_result.txt"
    
    targets = test_xray.load_addresses_from_file(list_file)
    
    if not targets:
        print(f"{Fore.RED}[!] Tidak ada target{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}[!] Starting scan ({len(targets)} targets) :{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Result akan disimpan di: {result_file}{Style.RESET_ALL}\n")
    
    success_count = 0
    for i, target in enumerate(targets, 1):
        print(f"[{i}/{len(targets)}] Testing: {target}")
        
        helpers.kill_xray_processes()
        
        if choice == "4":  # Onering
            result, connected_ip = onering.test_onering(target, account)
            if result:
                print(f"✅ CONNECTED - {Fore.GREEN}{target}{Style.RESET_ALL}")
                success_count += 1
                with open(result_file, "a") as f:
                    f.write(f"{target}\n")
            else:
                print(f"❌ FAILED - {Fore.RED}{target}{Style.RESET_ALL}")
        elif choice == "2":  # Wildcard
            result = test_xray.test_wildcard_address(target, account)
            if result:
                print(f"✅ CONNECTED - {Fore.GREEN}{target}{Style.RESET_ALL}")
                success_count += 1
                with open(result_file, "a") as f:
                    f.write(f"{target}\n")
            else:
                print(f"❌ FAILED - {Fore.RED}{target}{Style.RESET_ALL}")
        elif choice == "3":  # SNI
            result = test_xray.test_address(None, account, target)
            if result:
                print(f"✅ CONNECTED - {Fore.GREEN}{target}{Style.RESET_ALL}")
                success_count += 1
                with open(result_file, "a") as f:
                    f.write(f"{target}\n")
            else:
                print(f"❌ FAILED - {Fore.RED}{target}{Style.RESET_ALL}")
        elif choice == "8":  # SNI v2 (SNI + Host)
            result = test_xray.test_sniv2_address(target, account)
            if result:
                print(f"✅ CONNECTED - {Fore.GREEN}{target}{Style.RESET_ALL}")
                success_count += 1
                with open(result_file, "a") as f:
                    f.write(f"{target}\n")
            else:
                print(f"❌ FAILED - {Fore.RED}{target}{Style.RESET_ALL}")
        else:  # Address (1)
            result = test_xray.test_address(target, account)
            if result:
                print(f"✅ CONNECTED - {Fore.GREEN}{target}{Style.RESET_ALL}")
                success_count += 1
                with open(result_file, "a") as f:
                    f.write(f"{target}\n")
            else:
                print(f"❌ FAILED - {Fore.RED}{target}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}[!] Scan selesai! {success_count}/{len(targets)} berhasil connect{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[!] Result CONNECTED disimpan di: {result_file}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()