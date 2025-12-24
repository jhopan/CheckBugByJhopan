#!/usr/bin/env python3
"""
History/logging module for tracking scans
"""

import json
import os
from datetime import datetime
from colorama import Fore, Style

HISTORY_FILE = "jhopan_history.json"


def add_history(mode, list_file, total, success, duration, results):
    """Add scan result to history"""
    history = load_history()
    
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": mode,
        "list_file": list_file,
        "total": total,
        "success": success,
        "duration": duration,
        "success_rate": round((success / total * 100), 2) if total > 0 else 0,
        "results": {
            "connected": results.get("connected", []),
            "failed": results.get("failed", [])
        }
    }
    
    history.insert(0, entry)  # Add to beginning
    
    # Keep only last 50 entries
    history = history[:50]
    
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        return True
    except:
        return False


def load_history():
    """Load history from file"""
    if not os.path.exists(HISTORY_FILE):
        return []
    
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return []


def view_history():
    """Display scan history"""
    history = load_history()
    
    if not history:
        print(f"{Fore.YELLOW}[!] No scan history{Style.RESET_ALL}")
        return None
    
    print("\n" + "="*80)
    print(f"{Fore.CYAN}[*] Scan History{Style.RESET_ALL}")
    print("="*80)
    print(f"{'#':<4} {'Date/Time':<20} {'List':<15} {'Mode':<12} {'Result':<12} {'Time':<8}")
    print("-"*80)
    
    for i, entry in enumerate(history[:20], 1):  # Show last 20
        result_str = f"{entry['success']}/{entry['total']} ({entry['success_rate']}%)"
        duration_str = f"{entry['duration']:.1f}s"
        
        # Color based on success rate
        if entry['success_rate'] >= 50:
            color = Fore.GREEN
        elif entry['success_rate'] >= 20:
            color = Fore.YELLOW
        else:
            color = Fore.RED
        
        print(f"{color}[{i:<2}]{Style.RESET_ALL} {entry['timestamp']:<20} {entry['list_file']:<15} {entry['mode']:<12} {result_str:<12} {duration_str:<8}")
    
    print("="*80)
    
    return history


def get_history_entry(index):
    """Get specific history entry"""
    history = load_history()
    if 0 <= index < len(history):
        return history[index]
    return None


def clear_history():
    """Clear all history"""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        return True
    except:
        return False


def history_menu():
    """Interactive history menu"""
    while True:
        history = view_history()
        
        if not history:
            return
        
        print(f"\n{Fore.YELLOW}Options:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[1-20]{Style.RESET_ALL} View details")
        print(f"{Fore.RED}[D]{Style.RESET_ALL} Delete all history")
        print(f"{Fore.YELLOW}[0]{Style.RESET_ALL} Back to main menu")
        
        choice = input(f"\n{Fore.CYAN}[?] Select option: {Style.RESET_ALL}").strip().lower()
        
        if choice == '0':
            break
        
        elif choice == 'd':
            confirm = input(f"{Fore.YELLOW}[!] Delete all history? (y/n): {Style.RESET_ALL}").strip().lower()
            if confirm == 'y':
                if clear_history():
                    print(f"{Fore.GREEN}[+] History cleared{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[!] Failed to clear history{Style.RESET_ALL}")
        
        else:
            try:
                index = int(choice) - 1
                entry = get_history_entry(index)
                
                if entry:
                    print("\n" + "="*80)
                    print(f"{Fore.CYAN}[*] Scan Details{Style.RESET_ALL}")
                    print("="*80)
                    print(f"Date/Time: {entry['timestamp']}")
                    print(f"Mode: {entry['mode']}")
                    print(f"List File: {entry['list_file']}")
                    print(f"Duration: {entry['duration']:.1f}s")
                    print(f"Success Rate: {entry['success_rate']}% ({entry['success']}/{entry['total']})")
                    
                    print(f"\n{Fore.GREEN}Connected ({len(entry['results']['connected'])}):{Style.RESET_ALL}")
                    for target in entry['results']['connected'][:10]:  # Show first 10
                        print(f"  ✅ {target}")
                    if len(entry['results']['connected']) > 10:
                        print(f"  ... and {len(entry['results']['connected']) - 10} more")
                    
                    print(f"\n{Fore.RED}Failed ({len(entry['results']['failed'])}):{Style.RESET_ALL}")
                    for target in entry['results']['failed'][:10]:  # Show first 10
                        print(f"  ❌ {target}")
                    if len(entry['results']['failed']) > 10:
                        print(f"  ... and {len(entry['results']['failed']) - 10} more")
                    
                    print("="*80)
                    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[!] Invalid selection{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}[!] Invalid input{Style.RESET_ALL}")
