import os
import platform
from colorama import Fore, Style

def check_core():
    """Check for xray binaries on any platform"""
    system = platform.system()
    
    # Termux/Android paths
    onering_arm = "/data/data/com.termux/files/usr/bin/xray.linux.arm64.64bit"
    onering_amd = "/data/data/com.termux/files/usr/bin/xray.linux.amd64.64bit"
    xray_termux = "/data/data/com.termux/files/usr/bin/xray"
    
    # Standard Linux paths
    xray_linux = "/usr/bin/xray"
    xray_local = "/usr/local/bin/xray"
    
    # Windows paths
    xray_windows = "C:\\Program Files\\xray\\xray.exe"
    xray_current = os.path.join(os.getcwd(), "xray.exe")
    
    # Check ONERING
    if os.path.exists(onering_arm) or os.path.exists(onering_amd):
        print(f"{Fore.GREEN}> ONERING✅{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}> ONERING🟥{Style.RESET_ALL}")
    
    # Check XRAY based on platform
    xray_found = False
    if system == "Windows":
        if os.path.exists(xray_windows) or os.path.exists(xray_current):
            xray_found = True
    else:
        if (os.path.exists(xray_termux) or os.path.exists(xray_linux) or 
            os.path.exists(xray_local)):
            xray_found = True
    
    if xray_found:
        print(f"{Fore.GREEN}> XRAY✅{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}> XRAY🟥{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}> Platform: {system}{Style.RESET_ALL}")