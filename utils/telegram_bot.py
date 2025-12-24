#!/usr/bin/env python3
"""
Telegram bot notification module
IMPORTANT: Always use default route (not bound to specific interface)
This ensures Telegram works even when testing interface has no internet
"""

import requests
import platform
from colorama import Fore, Style


def send_telegram_message(token, chat_id, message):
    """
    Send message to Telegram
    Uses default routing (not bound to interface) - works even if testing interface has no internet
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
        # Force use default interface by not binding to specific interface
        # This ensures Telegram works even when xray uses wlan1 (no internet)
        # Telegram will use wlan0 (internet) automatically
        response = requests.post(url, data=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"{Fore.RED}[!] Telegram error: {e}{Style.RESET_ALL}")
        return False


def send_scan_start(token, chat_id, mode, list_file, total_targets):
    """Send notification when scan starts"""
    message = f"""
🚀 <b>Scan Started</b>

📋 Mode: {mode}
📁 List: {list_file}
🎯 Targets: {total_targets}

⏳ Testing in progress...
"""
    return send_telegram_message(token, chat_id, message.strip())


def send_scan_complete(token, chat_id, mode, list_file, total, success, failed, duration, connected_list, failed_list):
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
    
    return send_telegram_message(token, chat_id, message.strip())


def send_batch_complete(token, chat_id, results):
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
    
    return send_telegram_message(token, chat_id, message.strip())


def test_telegram_connection(token, chat_id):
    """Test if Telegram bot is working"""
    message = "🤖 <b>Jhopan Bot Test</b>\n\n✅ Bot configured successfully!"
    
    print(f"{Fore.CYAN}[*] Testing Telegram connection...{Style.RESET_ALL}")
    
    if send_telegram_message(token, chat_id, message):
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
