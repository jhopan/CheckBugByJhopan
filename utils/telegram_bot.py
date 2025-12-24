#!/usr/bin/env python3
"""
Telegram bot notification module
Supports interface binding for dual network setups
"""

import requests
import platform
import socket
from colorama import Fore, Style


def get_interface_ip(interface_name):
    """Get IP address of specific interface"""
    if interface_name == "auto" or not interface_name:
        return None
    
    try:
        # Try to get IP from interface using netifaces
        try:
            import netifaces
            addrs = netifaces.ifaddresses(interface_name)
            if netifaces.AF_INET in addrs:
                return addrs[netifaces.AF_INET][0]['addr']
        except ImportError:
            pass
        
        # Fallback: manual detection not reliable cross-platform
        return None
    except:
        return None


def send_telegram_message(token, chat_id, message, interface="auto"):
    """
    Send message to Telegram
    interface: "auto" for default route, or interface name (wlan0, wlan1, etc)
    """
    if not token or not chat_id:
        return False
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        # Default: use default routing
        if interface == "auto" or not interface:
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
        
        # Specific interface: bind to interface IP
        source_ip = get_interface_ip(interface)
        
        if source_ip:
            # Create custom session with source address
            session = requests.Session()
            
            # Monkey-patch socket to bind to specific IP
            original_socket = socket.socket
            
            def bound_socket(*args, **kwargs):
                sock = original_socket(*args, **kwargs)
                try:
                    sock.bind((source_ip, 0))
                except:
                    pass
                return sock
            
            socket.socket = bound_socket
            
            try:
                response = session.post(url, data=data, timeout=10)
                return response.status_code == 200
            finally:
                socket.socket = original_socket
        else:
            # Fallback to default route
            print(f"{Fore.YELLOW}[!] Could not bind to {interface}, using default route{Style.RESET_ALL}")
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
            
    except Exception as e:
        print(f"{Fore.RED}[!] Telegram error: {e}{Style.RESET_ALL}")
        return False


def send_scan_start(token, chat_id, mode, list_file, total_targets, interface="auto"):
    """Send notification when scan starts"""
    message = f"""
🚀 <b>Scan Started</b>

📋 Mode: {mode}
📁 List: {list_file}
🎯 Targets: {total_targets}

⏳ Testing in progress...
"""
    return send_telegram_message(token, chat_id, message.strip(), interface)


def send_scan_complete(token, chat_id, mode, list_file, total, success, failed, duration, connected_list, failed_list, interface="auto"):
    """
    Send detailed scan results to Telegram
    Includes connected and failed targets
    """
    success_rate = round((success / total * 100), 2) if total > 0 else 0
    
    # Emoji based on success rate
    if success_rate >= 50:
        emoji = "🎉"
    elif success_rate >= 20:
        emoji = "✅"
    else:
        emoji = "⚠️"
    
    message = f"""
{emoji} <b>Scan Complete</b>

📋 Mode: {mode}
📁 List: {list_file}
⏱️ Duration: {duration:.1f}s

━━━━━━━━━━━━━━━━━━━━━
📊 Results:
✅ Connected: {success}/{total} ({success_rate}%)
❌ Failed: {failed}/{total}
━━━━━━━━━━━━━━━━━━━━━
"""
    
    # Add connected targets (max 15)
    if connected_list:
        message += f"\n✅ <b>Connected Targets:</b>\n"
        for target in connected_list[:15]:
            message += f"  • {target}\n"
        if len(connected_list) > 15:
            message += f"  ... and {len(connected_list) - 15} more\n"
    
    # Add failed targets (max 10)
    if failed_list and len(failed_list) <= 10:
        message += f"\n❌ <b>Failed Targets:</b>\n"
        for target in failed_list[:10]:
            message += f"  • {target}\n"
    elif failed_list:
        message += f"\n❌ <b>Failed:</b> {len(failed_list)} targets\n"
    
    message += f"\n💾 Result saved to: <code>{list_file.replace('.txt', '_result.txt')}</code>"
    
    return send_telegram_message(token, chat_id, message.strip(), interface)


def send_batch_complete(token, chat_id, results, interface="auto"):
    """Send batch scan summary"""
    total_success = sum(r['success'] for r in results)
    total_targets = sum(r['total'] for r in results)
    total_duration = sum(r['duration'] for r in results)
    
    message = f"""
🎊 <b>Batch Scan Complete</b>

📦 Total Lists: {len(results)}
⏱️ Total Duration: {total_duration:.1f}s
✅ Total Connected: {total_success}/{total_targets}

━━━━━━━━━━━━━━━━━━━━━
"""
    
    for r in results:
        success_rate = round((r['success'] / r['total'] * 100), 2) if r['total'] > 0 else 0
        if success_rate >= 50:
            emoji = "🎉"
        elif success_rate >= 20:
            emoji = "✅"
        else:
            emoji = "⚠️"
        
        message += f"\n{emoji} {r['list_file']}\n"
        message += f"   {r['success']}/{r['total']} ({success_rate}%) - {r['duration']:.1f}s\n"
    
    return send_telegram_message(token, chat_id, message.strip(), interface)


def test_telegram_connection(token, chat_id, interface="auto"):
    """Test if Telegram bot is working"""
    message = "🤖 <b>Jhopan Bot Test</b>\n\n✅ Bot configured successfully!"
    
    if interface != "auto":
        message += f"\n🌐 Using interface: <code>{interface}</code>"
    
    print(f"{Fore.CYAN}[*] Testing Telegram connection...{Style.RESET_ALL}")
    
    if send_telegram_message(token, chat_id, message, interface):
        print(f"{Fore.GREEN}[+] Telegram test successful!{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}[!] Telegram test failed!{Style.RESET_ALL}")
        return False


def format_file_for_telegram(file_path):
    """
    Read result file and format for Telegram
    Returns list of connected targets
    """
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []
