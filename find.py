import os
import requests
from urllib.parse import urlparse
import colorama
import re

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
colorama.init()
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'

def load_wordlist(wordlist_file):
    with open(wordlist_file, "r") as file:
        wordlist = [line.strip() for line in file.readlines()]
    return wordlist

def replace_macros(url, wordlist):
    parsed_url = urlparse(url)
    subdomain = parsed_url.hostname.split('.')[0].replace('www', '')
    sub = subdomain if subdomain else parsed_url.path.split('.')[0]
    main_domain = '.'.join(parsed_url.hostname.split('.')[-2:])
    extld = parsed_url.hostname.split('.')[-1]
    
    macros = {
        '[Lutfifakee_SUB]': sub, 
        '[Lutfifakee_SUBG]': sub.upper(), 
        '[Lutfifakee_SUBC]': sub.capitalize(), 
    }
    for macro, replacement in macros.items():
        wordlist = [path.replace(macro, replacement) for path in wordlist]
    return wordlist


def admin_finder(url, wordlist):
    modified_wordlist = replace_macros(url, wordlist)
    found_admins = []

    headers = {
        'User-Agent': USER_AGENT
    }

    for path in modified_wordlist:
        admin_url = url + path
        response = requests.get(admin_url, headers=headers)
        print(f" {[response.status_code]} - {response.url}")
        
        if "input type=\"password\"" in response.text and 'method="post"' in response.text:
            found_admins.append(admin_url)
    return found_admins
    
def print_banner(text):
    lines = text.split("\n")
    width = max(len(line) for line in lines)
    print(Colors.HEADER + "╔" + "═" * (width + 2) + "╗" + Colors.ENDC)
    for line in lines:
        print(Colors.HEADER + "║ " + line.ljust(width) + " ║" + Colors.ENDC)
    print(Colors.HEADER + "╚" + "═" * (width + 2) + "╝" + Colors.ENDC)

if __name__ == "__main__":
    clear_screen()
    print_banner( """
            # Admin Finder Tool #
    Author          : Lutfifakee
    Github          : github.com/X-Projetion
    Instagram       : instagram.com/lutfifakee
""")

    
    target_url = input(Colors.WARNING +"\n root@Lutfifakee:~$ URL: "+ Colors.ENDC)
    wordlist_file = input(Colors.WARNING +" root@Lutfifakee:~$ WORDLIST: "+ Colors.ENDC)

    if not os.path.exists(wordlist_file):
        print(Colors.FAIL +"\n Wordlist file not found"+ Colors.ENDC)
        print(Colors.FAIL +" please double check the list of words you called"+ Colors.ENDC)
    else:
        wordlist = load_wordlist(wordlist_file)
        admin_urls = admin_finder(target_url, wordlist)
        if admin_urls:
            for admin_url in admin_urls:
                print(Colors.GREEN +f"Admin Found : "+ Colors.UNDERLINE + f"{admin_url}"+ Colors.ENDC)
        else:
            print(Colors.FAIL +"Admin Page Not Found"+ Colors.ENDC)


         
