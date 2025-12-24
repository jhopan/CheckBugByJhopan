#!/usr/bin/env python3
"""
Scanning engine with retry, progress, and batch support
"""

import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style

from modules import test_xray, onering
from utils import progress, telegram_bot, history, settings as settings_mod


def test_single_target(target, mode, account, show_progress_bar=True):
    """Test single target based on mode"""
    try:
        if mode == "4":  # Onering
            result, connected_ip = onering.test_onering(target, account)
            return result, target
        elif mode == "2":  # Wildcard
            result = test_xray.test_wildcard_address(target, account)
            return result, target
        elif mode == "3":  # SNI
            result = test_xray.test_address(None, account, target)
            return result, target
        elif mode == "8":  # SNI v2
            result = test_xray.test_sniv2_address(target, account)
            return result, target
        else:  # Address (1)
            result = test_xray.test_address(target, account)
            return result, target
    except Exception as e:
        if show_progress_bar:
            progress.clear_progress()
        print(f"{Fore.RED}[!] Error testing {target}: {e}{Style.RESET_ALL}")
        return False, target


def scan_with_retry(targets, mode, account, settings):
    """
    Scan targets with optional retry
    Returns: (connected_list, failed_list, duration)
    """
    start_time = time.time()
    
    connected = []
    failed = []
    
    show_prog = settings.get('show_progress', True)
    auto_retry = settings.get('auto_retry', True)
    retry_count = settings.get('retry_count', 2)
    parallel_jobs = settings.get('parallel_jobs', 1)
    
    # First pass
    print(f"{Fore.CYAN}[*] First pass: Testing {len(targets)} targets...{Style.RESET_ALL}")
    connected, failed = scan_targets(targets, mode, account, show_prog, parallel_jobs)
    
    # Retry failed targets if enabled
    if auto_retry and failed and retry_count > 0:
        for retry_num in range(1, retry_count + 1):
            if not failed:
                break
            
            print(f"\n{Fore.YELLOW}[*] Retry {retry_num}/{retry_count}: {len(failed)} failed targets...{Style.RESET_ALL}")
            retry_connected, retry_failed = scan_targets(failed, mode, account, show_prog, parallel_jobs)
            
            # Update lists
            connected.extend(retry_connected)
            failed = retry_failed
            
            if retry_connected:
                print(f"{Fore.GREEN}[+] Retry recovered {len(retry_connected)} targets!{Style.RESET_ALL}")
    
    duration = time.time() - start_time
    
    return connected, failed, duration


def scan_targets(targets, mode, account, show_progress_bar=True, parallel_jobs=1):
    """
    Scan list of targets
    Returns: (connected_list, failed_list)
    """
    from utils import helpers
    
    connected = []
    failed = []
    total = len(targets)
    
    if parallel_jobs > 1:
        # Parallel execution
        with ThreadPoolExecutor(max_workers=parallel_jobs) as executor:
            futures = {executor.submit(test_single_target, target, mode, account, show_progress_bar): target 
                      for target in targets}
            
            for i, future in enumerate(as_completed(futures), 1):
                target = futures[future]
                
                if show_progress_bar:
                    progress.show_progress_bar(i, total, len(connected), len(failed), target)
                
                try:
                    result, tested_target = future.result()
                    
                    helpers.kill_xray_processes()
                    
                    if result:
                        connected.append(tested_target)
                        if not show_progress_bar:
                            print(f"✅ CONNECTED - {Fore.GREEN}{tested_target}{Style.RESET_ALL}")
                    else:
                        failed.append(tested_target)
                        if not show_progress_bar:
                            print(f"❌ FAILED - {Fore.RED}{tested_target}{Style.RESET_ALL}")
                except Exception as e:
                    failed.append(target)
                    if show_progress_bar:
                        progress.clear_progress()
                    print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
    else:
        # Sequential execution
        for i, target in enumerate(targets, 1):
            if show_progress_bar:
                progress.show_progress_bar(i, total, len(connected), len(failed), target)
            else:
                print(f"[{i}/{total}] Testing: {target}")
            
            result, tested_target = test_single_target(target, mode, account, show_progress_bar)
            
            helpers.kill_xray_processes()
            
            if result:
                connected.append(tested_target)
                if not show_progress_bar:
                    print(f"✅ CONNECTED - {Fore.GREEN}{tested_target}{Style.RESET_ALL}")
            else:
                failed.append(tested_target)
                if not show_progress_bar:
                    print(f"❌ FAILED - {Fore.RED}{tested_target}{Style.RESET_ALL}")
    
    if show_progress_bar:
        progress.clear_progress()
    
    return connected, failed


def batch_scan(list_files, mode, account, settings):
    """
    Scan multiple list files in batch
    Returns: list of results
    """
    results = []
    total_lists = len(list_files)
    
    for i, list_file in enumerate(list_files, 1):
        progress.print_step(i, total_lists, f"Processing {list_file}")
        
        if not os.path.exists(list_file):
            print(f"{Fore.RED}[!] File not found: {list_file}{Style.RESET_ALL}")
            continue
        
        # Load targets
        targets = test_xray.load_addresses_from_file(list_file)
        if not targets:
            print(f"{Fore.RED}[!] No targets in {list_file}{Style.RESET_ALL}")
            continue
        
        # Result file name
        list_basename = os.path.splitext(os.path.basename(list_file))[0]
        result_file = f"{list_basename}_result.txt"
        
        print(f"{Fore.CYAN}[*] Testing {len(targets)} targets from {list_file}...{Style.RESET_ALL}")
        
        # Scan with retry
        connected, failed, duration = scan_with_retry(targets, mode, account, settings)
        
        # Save results
        with open(result_file, "w") as f:
            for target in connected:
                f.write(f"{target}\n")
        
        # Show summary
        progress.show_summary(len(targets), len(connected), len(failed), duration, connected[:5])
        
        print(f"{Fore.GREEN}[+] Results saved to: {result_file}{Style.RESET_ALL}")
        
        # Store result
        results.append({
            'list_file': list_file,
            'total': len(targets),
            'success': len(connected),
            'failed': len(failed),
            'duration': duration,
            'result_file': result_file,
            'connected': connected,
            'failed_list': failed
        })
    
    return results
