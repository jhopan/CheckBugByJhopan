#!/usr/bin/env python3
import subprocess
import time
import os
import json
from colorama import Fore, Style

XRAY_PATH = "/data/data/com.termux/files/usr/bin/xray"

def get_xray_command():
    if os.path.exists(XRAY_PATH):
        return XRAY_PATH
    else:
        return "xray"

def test_xray_connection(config_file):
    try:
        xray_cmd = get_xray_command()
        
        xray_proc = subprocess.Popen(
            [xray_cmd, "run", "-config", config_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(3)
        
        if xray_proc.poll() is None:
            xray_proc.terminate()
            xray_proc.wait()
            return True
        else:
            stdout, stderr = xray_proc.communicate()
            print(f"{Fore.RED}[!] Xray Error: {stderr}{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}[!] Error menjalankan Xray: {e}{Style.RESET_ALL}")
        return False

def test_address(target_address, server_config, sni_address=None, config_func=None):
    try:
        if config_func:
            xray_config = config_func(server_config, target_address)
        elif sni_address:
            from modules.config import create_xray_config
            xray_config = create_xray_config(server_config, None, sni_address)
        else:
            from modules.config import create_xray_config
            xray_config = create_xray_config(server_config, target_address)
        
        if target_address:
            config_name = target_address.replace('.', '-').replace('/', '-')
        elif sni_address:
            config_name = sni_address.replace('.', '-').replace('/', '-')
        else:
            config_name = "test"
            
        config_file = f"test-{config_name}.json"
        with open(config_file, "w") as f:
            json.dump(xray_config, f, indent=2)
        
        xray_cmd = get_xray_command()
        
        xray_proc = subprocess.Popen(
            [xray_cmd, "run", "-config", config_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        time.sleep(3)
        
        try:
            result = subprocess.run(
                ["curl", "-s", "--socks5", "127.0.0.1:10808", 
                 "-o", "/dev/null", "-w", "%{http_code}", 
                 "--max-time", "5",
                 "http://httpbin.org/ip"],
                capture_output=True, text=True, timeout=8
            )
            
            success = result.stdout == "200"
            
        except:
            success = False
        
        try:
            xray_proc.terminate()
            xray_proc.wait(timeout=2)
        except:
            try:
                xray_proc.kill()
                xray_proc.wait(timeout=1)
            except:
                pass
        
        try:
            os.remove(config_file)
        except:
            pass
        
        return success
        
    except Exception as e:
        print(f"{Fore.RED}[!] Error testing {target_address or sni_address or 'unknown'}: {e}{Style.RESET_ALL}")
        return False

def test_wildcard_address(target_address, server_config):
    from modules.config import create_xray_config_wildcard
    return test_address(target_address, server_config, config_func=create_xray_config_wildcard)

def load_addresses_from_file(filename):
    addresses = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    addresses.append(line)
        return addresses
    except FileNotFoundError:
        print(f"{Fore.RED}[!] File {filename} tidak ditemukan!{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"{Fore.RED}[!] Error membaca file: {e}{Style.RESET_ALL}")
        return []

def test_sniv2_address(target_sni, server_config):
    """Test SNI v2: Target digunakan sebagai SNI dan Host header"""
    from modules.config import create_xray_config_sniv2
    return test_address(target_sni, server_config, config_func=lambda cfg, tgt: create_xray_config_sniv2(cfg, tgt))
