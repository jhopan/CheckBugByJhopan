#!/usr/bin/env python3
import random
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

def user_agent():
    try:
        ua = open("user-agents.txt","r").read().splitlines()
        return random.choice(ua)
    except:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def Subdomain():
    target = input("[*] Domain : ")
    try:
        Agents = {'User-Agent': user_agent()}
        api = f'https://rapiddns.io/subdomain/{target}?full=1&down=0'
        r = requests.get(api, headers=Agents).text
        bs = BeautifulSoup(r, 'html.parser')
        tbody = bs.find('tbody')
        if tbody:
            _tr = tbody.find_all('tr')
            rd = set()
            for pilla in _tr:
                results = pilla.find('td').text
                lists = results.split()
                rd.update(lists)
            ls = list(rd)
            print(f"\n{Fore.CYAN}[!] Found {len(ls)} subdomains:{Style.RESET_ALL}")
            for end in ls:
                open('domain.txt', 'a').write(end + '\n')
                print(f"[*] {end}")
            print(f"\n{Fore.CYAN}[!] Hasil tersimpan di: domain.txt{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Tidak ada subdomain ditemukan{Style.RESET_ALL}")
    except Exception as e:
        print(f'[!] Error: {e}')