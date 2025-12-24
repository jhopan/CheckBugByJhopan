#!/usr/bin/env python3
"""
Progress bar and UI utilities
"""

import sys
import time
from colorama import Fore, Style


def show_progress_bar(current, total, success, failed, current_target="", bar_length=40):
    """
    Display live progress bar
    """
    percent = (current / total) * 100 if total > 0 else 0
    filled = int(bar_length * current / total) if total > 0 else 0
    bar = '█' * filled + '░' * (bar_length - filled)
    
    # Color based on success rate
    if current > 0:
        success_rate = (success / current) * 100
        if success_rate >= 50:
            color = Fore.GREEN
        elif success_rate >= 20:
            color = Fore.YELLOW
        else:
            color = Fore.RED
    else:
        color = Fore.CYAN
    
    # Build progress line
    progress_line = f"\r{color}[{bar}]{Style.RESET_ALL} {percent:.0f}% ({current}/{total}) "
    progress_line += f"✅ {success}  ❌ {failed}"
    
    if current_target:
        # Truncate long targets
        if len(current_target) > 30:
            current_target = current_target[:27] + "..."
        progress_line += f"  | {Fore.CYAN}{current_target}{Style.RESET_ALL}"
    
    # Print without newline
    sys.stdout.write(progress_line)
    sys.stdout.flush()


def clear_progress():
    """Clear progress bar line"""
    sys.stdout.write('\r' + ' ' * 120 + '\r')
    sys.stdout.flush()


def show_summary(total, success, failed, duration, top_results=None):
    """Display scan summary"""
    success_rate = (success / total * 100) if total > 0 else 0
    
    print("\n" + "="*60)
    print(f"{Fore.CYAN}[*] Scan Summary{Style.RESET_ALL}")
    print("="*60)
    
    # Stats
    if success_rate >= 50:
        color = Fore.GREEN
        emoji = "🎉"
    elif success_rate >= 20:
        color = Fore.YELLOW
        emoji = "✅"
    else:
        color = Fore.RED
        emoji = "⚠️"
    
    print(f"{emoji} {color}Success Rate: {success_rate:.1f}% ({success}/{total}){Style.RESET_ALL}")
    print(f"❌ Failed: {failed}/{total} ({(failed/total*100):.1f}%)")
    print(f"⏱️  Duration: {duration:.1f}s")
    
    if total > 0:
        print(f"⚡ Avg Speed: {(total/duration):.2f} targets/s")
    
    # Top results
    if top_results and success > 0:
        print(f"\n{Fore.GREEN}Top Results:{Style.RESET_ALL}")
        for i, target in enumerate(top_results[:5], 1):
            print(f"  {i}. {target}")
    
    print("="*60)


def animate_loading(message="Processing", duration=2):
    """Show loading animation"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{Fore.CYAN}{frames[i % len(frames)]} {message}...{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    
    sys.stdout.write('\r' + ' ' * 50 + '\r')
    sys.stdout.flush()


def print_header(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"{Fore.CYAN}[*] {title}{Style.RESET_ALL}")
    print("="*60)


def print_step(step, total, message):
    """Print step indicator"""
    print(f"{Fore.YELLOW}[{step}/{total}]{Style.RESET_ALL} {message}")
