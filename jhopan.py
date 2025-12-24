#!/usr/bin/env python3
#Jhopan v.3.3 use xray core v25.12.8 - by Jhopan
import os
import platform
import time
from colorama import Fore, Style, init
from modules import parse, config, test_xray, ssh, subdomain, onering, revip
from utils import helpers, accounts, network, settings as settings_mod, history, telegram_bot, progress, scan_engine
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
    
    # Additional options
    print(f"{Fore.YELLOW}[9]{Style.RESET_ALL} Manage Saved Accounts")
    print(f"{Fore.YELLOW}[10]{Style.RESET_ALL} Settings")
    print(f"{Fore.YELLOW}[11]{Style.RESET_ALL} View History")
    print(f"{Fore.YELLOW}[12]{Style.RESET_ALL} Batch Mode (Multiple Lists)")
    
    choice = input(f"{Fore.YELLOW}[*] Pilih metode (1-12): {Style.RESET_ALL}").strip()
    
    # Account management
    if choice == "9":
        accounts.manage_accounts_menu()
        return
    
    # Settings
    if choice == "10":
        settings_mod.settings_menu()
        return
    
    # History
    if choice == "11":
        history.history_menu()
        return
    
    # Batch mode
    if choice == "12":
        batch_mode()
        return
    
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
    
    # URL selection with account management
    url = accounts.select_account()
    
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
    
    # Ask if user wants to save this account
    accounts.ask_save_account(url)
    
    # Get network interface for testing (dual network support)
    selected_interface = network.get_network_interface()
    
    # Set interface for test_xray module
    test_xray.set_interface(selected_interface)
    
    # Load settings
    settings = settings_mod.load_settings()
    
    # Get result file name based on list file name
    list_basename = os.path.splitext(os.path.basename(list_file))[0]
    result_file = f"{list_basename}_result.txt"
    
    targets = test_xray.load_addresses_from_file(list_file)
    
    if not targets:
        print(f"{Fore.RED}[!] Tidak ada target{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.CYAN}[!] Starting scan ({len(targets)} targets){Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Result akan disimpan di: {result_file}{Style.RESET_ALL}")
    
    # Telegram notification - scan start
    if settings.get('telegram_enabled'):
        telegram_bot.send_scan_start(
            settings['telegram_token'],
            settings['telegram_chat_id'],
            modes[choice],
            list_file,
            len(targets)
        )
    
    # Scan with retry support
    start_time = time.time()
    connected, failed, duration = scan_engine.scan_with_retry(targets, choice, account, settings)
    
    # Save results
    with open(result_file, "w") as f:
        for target in connected:
            f.write(f"{target}\n")
    
    # Show summary
    progress.show_summary(len(targets), len(connected), len(failed), duration, connected[:5])
    print(f"{Fore.GREEN}[+] Results saved to: {result_file}{Style.RESET_ALL}")
    
    # Telegram notification - scan complete
    if settings.get('telegram_enabled'):
        telegram_bot.send_scan_complete(
            settings['telegram_token'],
            settings['telegram_chat_id'],
            modes[choice],
            list_file,
            len(targets),
            len(connected),
            len(failed),
            duration,
            connected,
            failed
        )
    
    # Add to history
    history.add_history(
        mode=modes[choice],
        list_file=list_file,
        total=len(targets),
        success=len(connected),
        duration=duration,
        results={'connected': connected, 'failed': failed}
    )


def batch_mode():
    """Batch scanning mode for multiple list files"""
    progress.print_header("Batch Mode - Multiple Lists")
    
    print(f"{Fore.CYAN}[*] Enter list files (comma separated):{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}    Example: wa.txt,ig.txt,tiktok.txt{Style.RESET_ALL}")
    
    lists_input = input(f"{Fore.CYAN}[*] List files: {Style.RESET_ALL}").strip()
    
    if not lists_input:
        print(f"{Fore.RED}[!] No lists provided{Style.RESET_ALL}")
        return
    
    list_files = [f.strip() for f in lists_input.split(',')]
    
    # Validate files
    valid_files = []
    for f in list_files:
        if os.path.exists(f):
            valid_files.append(f)
        else:
            print(f"{Fore.YELLOW}[!] File not found: {f} (skipped){Style.RESET_ALL}")
    
    if not valid_files:
        print(f"{Fore.RED}[!] No valid files{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}[+] Valid files: {len(valid_files)}{Style.RESET_ALL}")
    
    # Select mode
    modes = {
        "1": "Address",
        "2": "Wildcard",
        "3": "SNI",
        "4": "Onering",
        "8": "SNI v2"
    }
    
    helpers.show_menu()
    choice = input(f"{Fore.YELLOW}[*] Pilih metode (1-8): {Style.RESET_ALL}").strip()
    
    if choice not in modes:
        print(f"{Fore.RED}[!] Invalid mode{Style.RESET_ALL}")
        return
    
    # Get account
    url = accounts.select_account()
    if not url:
        print(f"{Fore.RED}[!] URL required{Style.RESET_ALL}")
        return
    
    try:
        account = parse.parse_vmess_trojan_url(url)
        print(f"{Fore.GREEN}[+] Account: {account['protocol']} {account['address']}:{account['port']}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
        return
    
    # Network interface
    selected_interface = network.get_network_interface()
    test_xray.set_interface(selected_interface)
    
    # Load settings
    settings = settings_mod.load_settings()
    
    # Batch scan
    print(f"\n{Fore.CYAN}[*] Starting batch scan...{Style.RESET_ALL}")
    results = scan_engine.batch_scan(valid_files, choice, account, settings)
    
    # Batch summary
    print("\n" + "="*60)
    print(f"{Fore.CYAN}[*] Batch Scan Complete!{Style.RESET_ALL}")
    print("="*60)
    
    total_success = sum(r['success'] for r in results)
    total_targets = sum(r['total'] for r in results)
    total_duration = sum(r['duration'] for r in results)
    
    print(f"📦 Total Lists: {len(results)}")
    print(f"🎯 Total Targets: {total_targets}")
    print(f"✅ Total Connected: {total_success}")
    print(f"⏱️  Total Duration: {total_duration:.1f}s")
    print("="*60)
    
    # Telegram notification - batch complete
    if settings.get('telegram_enabled'):
        telegram_bot.send_batch_complete(
            settings['telegram_token'],
            settings['telegram_chat_id'],
            results
        )


if __name__ == "__main__":
    main()