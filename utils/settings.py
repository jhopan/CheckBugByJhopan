#!/usr/bin/env python3
"""
Settings management with defaults
"""

import json
import os
from colorama import Fore, Style

SETTINGS_FILE = "jhopan_settings.json"

# Default settings
DEFAULT_SETTINGS = {
    "timeout": 5,
    "parallel_jobs": 1,
    "auto_retry": True,
    "retry_count": 2,
    "telegram_enabled": False,
    "telegram_token": "",
    "telegram_chat_id": "",
    "speed_test_enabled": False,
    "show_progress": True
}


def load_settings():
    """Load settings from file, return defaults if not exists"""
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    
    try:
        with open(SETTINGS_FILE, 'r') as f:
            saved = json.load(f)
            # Merge with defaults (in case new settings added)
            settings = DEFAULT_SETTINGS.copy()
            settings.update(saved)
            return settings
    except:
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    """Save settings to file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except:
        return False


def get_setting(key):
    """Get specific setting value"""
    settings = load_settings()
    return settings.get(key, DEFAULT_SETTINGS.get(key))


def set_setting(key, value):
    """Set specific setting value"""
    settings = load_settings()
    settings[key] = value
    return save_settings(settings)


def settings_menu():
    """Interactive settings menu"""
    settings = load_settings()
    
    while True:
        print("\n" + "="*60)
        print(f"{Fore.CYAN}[*] Settings{Style.RESET_ALL}")
        print("="*60)
        
        print(f"{Fore.YELLOW}Performance:{Style.RESET_ALL}")
        print(f"  [1] Timeout: {settings['timeout']}s")
        print(f"  [2] Parallel Jobs: {settings['parallel_jobs']}")
        print(f"  [3] Auto Retry: {'ON' if settings['auto_retry'] else 'OFF'}")
        print(f"  [4] Retry Count: {settings['retry_count']}")
        
        print(f"\n{Fore.YELLOW}Features:{Style.RESET_ALL}")
        print(f"  [5] Show Progress Bar: {'ON' if settings['show_progress'] else 'OFF'}")
        print(f"  [6] Speed Test: {'ON' if settings['speed_test_enabled'] else 'OFF'}")
        
        print(f"\n{Fore.YELLOW}Telegram Notification:{Style.RESET_ALL}")
        print(f"  [7] Telegram: {'ON' if settings['telegram_enabled'] else 'OFF'}")
        if settings['telegram_enabled']:
            print(f"      Bot Token: {settings['telegram_token'][:10]}...{settings['telegram_token'][-5:] if settings['telegram_token'] else 'Not set'}")
            print(f"      Chat ID: {settings['telegram_chat_id']}")
        
        print(f"\n{Fore.GREEN}[8]{Style.RESET_ALL} Reset to Defaults")
        print(f"{Fore.RED}[0]{Style.RESET_ALL} Back to Main Menu")
        print("="*60)
        
        choice = input(f"{Fore.CYAN}[?] Select option: {Style.RESET_ALL}").strip()
        
        if choice == '0':
            break
        
        elif choice == '1':
            try:
                timeout = int(input(f"{Fore.CYAN}[*] Timeout (1-30s) [{settings['timeout']}]: {Style.RESET_ALL}") or settings['timeout'])
                if 1 <= timeout <= 30:
                    settings['timeout'] = timeout
                    print(f"{Fore.GREEN}[+] Timeout updated to {timeout}s{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}[!] Invalid input{Style.RESET_ALL}")
        
        elif choice == '2':
            try:
                jobs = int(input(f"{Fore.CYAN}[*] Parallel Jobs (1-10) [{settings['parallel_jobs']}]: {Style.RESET_ALL}") or settings['parallel_jobs'])
                if 1 <= jobs <= 10:
                    settings['parallel_jobs'] = jobs
                    print(f"{Fore.GREEN}[+] Parallel jobs updated to {jobs}{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}[!] Invalid input{Style.RESET_ALL}")
        
        elif choice == '3':
            settings['auto_retry'] = not settings['auto_retry']
            print(f"{Fore.GREEN}[+] Auto retry: {'ON' if settings['auto_retry'] else 'OFF'}{Style.RESET_ALL}")
        
        elif choice == '4':
            try:
                retry = int(input(f"{Fore.CYAN}[*] Retry Count (1-5) [{settings['retry_count']}]: {Style.RESET_ALL}") or settings['retry_count'])
                if 1 <= retry <= 5:
                    settings['retry_count'] = retry
                    print(f"{Fore.GREEN}[+] Retry count updated to {retry}{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}[!] Invalid input{Style.RESET_ALL}")
        
        elif choice == '5':
            settings['show_progress'] = not settings['show_progress']
            print(f"{Fore.GREEN}[+] Progress bar: {'ON' if settings['show_progress'] else 'OFF'}{Style.RESET_ALL}")
        
        elif choice == '6':
            settings['speed_test_enabled'] = not settings['speed_test_enabled']
            print(f"{Fore.GREEN}[+] Speed test: {'ON' if settings['speed_test_enabled'] else 'OFF'}{Style.RESET_ALL}")
        
        elif choice == '7':
            if not settings['telegram_enabled']:
                # Enable and configure
                print(f"\n{Fore.CYAN}[*] Setup Telegram Bot{Style.RESET_ALL}")
                token = input(f"{Fore.CYAN}[*] Bot Token: {Style.RESET_ALL}").strip()
                chat_id = input(f"{Fore.CYAN}[*] Chat ID: {Style.RESET_ALL}").strip()
                
                if token and chat_id:
                    settings['telegram_token'] = token
                    settings['telegram_chat_id'] = chat_id
                    settings['telegram_enabled'] = True
                    print(f"{Fore.GREEN}[+] Telegram enabled!{Style.RESET_ALL}")
            else:
                # Disable
                settings['telegram_enabled'] = False
                print(f"{Fore.YELLOW}[!] Telegram disabled{Style.RESET_ALL}")
        
        elif choice == '8':
            confirm = input(f"{Fore.YELLOW}[!] Reset to defaults? (y/n): {Style.RESET_ALL}").strip().lower()
            if confirm == 'y':
                settings = DEFAULT_SETTINGS.copy()
                print(f"{Fore.GREEN}[+] Settings reset to defaults{Style.RESET_ALL}")
        
        # Save settings after any change
        save_settings(settings)
    
    return settings
