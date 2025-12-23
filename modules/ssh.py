#!/usr/bin/env python3
import socket
import time
from colorama import Fore, Style

def ssh_connection():
    SSH_HOST = input(f"[*] Host SSH : ")
    SSH_PORT = int(input(f"[*] SSH Port : "))
    USERNAME = input(f"[*] Username : ")
    PASSWORD = input(f"[*] Password : ")
    
    proxy_file = input(f"{Fore.YELLOW}[*] List web/ip (txt) : {Style.RESET_ALL}")
    
    try:
        with open(proxy_file, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] File {proxy_file} tidak ditemukan!{Style.RESET_ALL}")
        return
        
    print(f"{Fore.CYAN}[1] Proxy HTTP (No SNI)")
    print(f"[2] TLS/SSL Proxy (SNI){Style.RESET_ALL}")
    ask_sni = input(f"{Fore.YELLOW}[*] Pilih metode (1/2) : {Style.RESET_ALL}")
    if ask_sni == "1":
        SNI_HOST = SSH_HOST
    elif ask_sni == "2":
        SNI_HOST = input(f"{Fore.YELLOW}[*] SNI : {Style.RESET_ALL}")
        
    for proxy_host in proxies:
        try:
            sock = socket.socket()
            sock.settimeout(8)
            sock.connect((proxy_host, 80))
            payload = f"GET /ws HTTP/1.1\r\nHost: {SNI_HOST}\r\nConnection: Keep-Alive\r\nUpgrade: websocket\r\n\r\n"
            sock.send(payload.encode())
            time.sleep(1)
            auth = f"CONNECT {USERNAME}:{PASSWORD}@{SSH_HOST}:{SSH_PORT}\r\n\r\n"
            sock.send(auth.encode())
            time.sleep(2)
            response = sock.recv(2048)
            if b"SSH-2.0" in response:
                print(f"✅ CONNECTED - {Fore.GREEN}{proxy_host}{Style.RESET_ALL}")
                with open("Result.txt","a") as f:
                    f.write(proxy_host+"\n")
                sock.close()
            else:
                print(f"❌ FAILED - {Fore.RED}{proxy_host}{Style.RESET_ALL}")
                sock.close()
        except Exception as e:
            print(f"❌ {proxy_host} - {Fore.RED}FAILED ({str(e)[:30]}...){Style.RESET_ALL}")
    print(f"{Fore.CYAN}[!] Hasil tersimpan di : Result.txt {Style.RESET_ALL}")