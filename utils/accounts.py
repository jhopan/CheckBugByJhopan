#!/usr/bin/env python3
"""
Account URL management for easy testing
"""

import json
import os
from colorama import Fore, Style


ACCOUNTS_FILE = "accounts.json"


def load_accounts():
    """Load saved accounts from file"""
    if not os.path.exists(ACCOUNTS_FILE):
        return []
    
    try:
        with open(ACCOUNTS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []


def save_accounts(accounts):
    """Save accounts to file"""
    try:
        with open(ACCOUNTS_FILE, 'w') as f:
            json.dump(accounts, f, indent=2)
        return True
    except:
        return False


def add_account(name, url):
    """Add new account to saved list"""
    accounts = load_accounts()
    
    # Check if name already exists
    for acc in accounts:
        if acc['name'] == name:
            # Update existing
            acc['url'] = url
            save_accounts(accounts)
            return True
    
    # Add new account
    accounts.append({
        'name': name,
        'url': url
    })
    
    return save_accounts(accounts)


def delete_account(name):
    """Delete account by name"""
    accounts = load_accounts()
    accounts = [acc for acc in accounts if acc['name'] != name]
    return save_accounts(accounts)


def list_accounts():
    """Display saved accounts"""
    accounts = load_accounts()
    
    if not accounts:
        print(f"{Fore.YELLOW}[!] No saved accounts{Style.RESET_ALL}")
        return None
    
    print("\n" + "="*60)
    print(f"{Fore.CYAN}[*] Saved Accounts{Style.RESET_ALL}")
    print("="*60)
    
    for i, acc in enumerate(accounts, 1):
        protocol = acc['url'].split('://')[0] if '://' in acc['url'] else 'unknown'
        print(f"{Fore.GREEN}[{i}]{Style.RESET_ALL} {acc['name']:15} - {protocol}")
    
    print(f"{Fore.YELLOW}[0]{Style.RESET_ALL} Enter new URL")
    print("="*60)
    
    return accounts


def select_account():
    """Let user select from saved accounts or enter new URL"""
    accounts = list_accounts()
    
    if not accounts:
        # No saved accounts, ask for new URL
        return input(f"{Fore.CYAN}[*] Masukkan URL akun: {Style.RESET_ALL}").strip()
    
    while True:
        try:
            choice = int(input(f"{Fore.CYAN}[?] Select account (0-{len(accounts)}): {Style.RESET_ALL}"))
            
            if choice == 0:
                # Enter new URL
                return input(f"{Fore.CYAN}[*] Masukkan URL akun: {Style.RESET_ALL}").strip()
            
            if 1 <= choice <= len(accounts):
                selected = accounts[choice - 1]
                print(f"{Fore.GREEN}[+] Using account: {selected['name']}{Style.RESET_ALL}")
                return selected['url']
        
        except ValueError:
            pass
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Cancelled{Style.RESET_ALL}")
            return None
        
        print(f"{Fore.RED}[!] Invalid choice!{Style.RESET_ALL}")


def ask_save_account(url):
    """Ask user if they want to save the URL"""
    save = input(f"{Fore.CYAN}[?] Save this URL for quick access? (y/n): {Style.RESET_ALL}").strip().lower()
    
    if save == 'y':
        name = input(f"{Fore.CYAN}[*] Account name (e.g., 'MyVPN', 'Testing'): {Style.RESET_ALL}").strip()
        
        if name:
            if add_account(name, url):
                print(f"{Fore.GREEN}[+] Account saved as '{name}'{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] Failed to save account{Style.RESET_ALL}")


def manage_accounts_menu():
    """Show account management menu"""
    while True:
        print("\n" + "="*60)
        print(f"{Fore.CYAN}[*] Account Management{Style.RESET_ALL}")
        print("="*60)
        print(f"{Fore.GREEN}[1]{Style.RESET_ALL} List accounts")
        print(f"{Fore.YELLOW}[2]{Style.RESET_ALL} Delete account")
        print(f"{Fore.RED}[0]{Style.RESET_ALL} Back to main menu")
        print("="*60)
        
        choice = input(f"{Fore.CYAN}[?] Choose option: {Style.RESET_ALL}").strip()
        
        if choice == '0':
            break
        
        elif choice == '1':
            list_accounts()
        
        elif choice == '2':
            accounts = load_accounts()
            if not accounts:
                print(f"{Fore.YELLOW}[!] No saved accounts{Style.RESET_ALL}")
                continue
            
            print("\n" + "="*60)
            print(f"{Fore.CYAN}[*] Delete Account{Style.RESET_ALL}")
            print("="*60)
            
            for i, acc in enumerate(accounts, 1):
                print(f"{Fore.GREEN}[{i}]{Style.RESET_ALL} {acc['name']}")
            
            print("="*60)
            
            try:
                del_choice = int(input(f"{Fore.CYAN}[?] Select account to delete (1-{len(accounts)}): {Style.RESET_ALL}"))
                
                if 1 <= del_choice <= len(accounts):
                    account = accounts[del_choice - 1]
                    confirm = input(f"{Fore.YELLOW}[!] Delete '{account['name']}'? (y/n): {Style.RESET_ALL}").strip().lower()
                    
                    if confirm == 'y':
                        if delete_account(account['name']):
                            print(f"{Fore.GREEN}[+] Account deleted{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}[!] Failed to delete account{Style.RESET_ALL}")
            
            except (ValueError, KeyboardInterrupt):
                print(f"{Fore.YELLOW}[!] Cancelled{Style.RESET_ALL}")
