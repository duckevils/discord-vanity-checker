import os
import threading
import json
import random
import requests
from rich import print
from time import sleep
from concurrent.futures import ThreadPoolExecutor

duck = {
    "webhook": "webhook",  
    "importListFrom": "urls.txt",  
    "rotating": True,  
    "threads": 1000, # 500 ustune cıkma
    "showTaken": True,  
    "showAvailable": True 
}

def chunks(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def webhook(invite_code):
    embed_data = {
        "title": "Vanity URL Available!",
        "description": f"• **Vanity URL** : `{invite_code} :>`\n [Join the Discord Server](https://discord.gg/israil)",
        "color": 65280,
        "footer": {
            "text": "developed by duckevils [>.<]",
            "icon_url": "https://cdn.discordapp.com/attachments/1138418027294109757/1316061055587323965/54e898f565e5b0637e921475726b841f.png?ex=6759acde&is=67585b5e&hm=e6e5e9aa90f1eb8df0a4638ec205df9ec5ab36f27a5d72140008e971e4c9172c&"
        }
    }
    data = {"content": None, "embeds": [embed_data], "attachments": []}
    headers = {"Content-Type": "application/json"}
    requests.post(duck['webhook'], data=json.dumps(data), headers=headers)

def checker(invite_code, session, proxy):
    try:
        url = f"https://discord.com/api/v9/invites/{invite_code}"
        headers = {"content-type": "application/json"}
        if proxy:
            proxies = {"https": f"http://{proxy}"}
        else:
            proxies = {}

        response = session.get(url, headers=headers, proxies=proxies)

        if response.status_code == 429:
            print('[red]Rate-Limit')
            return

        if response.status_code == 200:
            print(f'Vanity URL Not Available: [ [red]{invite_code}[/red] ]') if duck.get('showTaken', False) else None
        elif response.status_code == 404:
            print(f'Vanity URL is Available: [ [green]{invite_code}[/green] ]') if duck.get('showAvailable', False) else None
            webhook(invite_code)
        else:
            print(f'Error with URL [ [yellow]{invite_code}[/yellow] ], check your proxies.')

    except requests.exceptions.RequestException as duckevils:
        print(f"ERR! {duckevils}")

def handler():
    session = requests.Session()

    urls = []
    try:
        with open(duck['importListFrom'], 'r') as f:
            urls = f.read().splitlines()
    except FileNotFoundError:
        print("The file containing the URL list was not found.")
        return
    
    if not urls:
        print("No URLs to check.")
        return

    if duck.get('rotating', True):
        proxy_list = open("proxies.txt", 'r').readlines()

    if not proxy_list:
        proxy = None
    else:
        proxy = random.choice(proxy_list).strip()

    with ThreadPoolExecutor(max_workers=duck.get('threads', 10)) as executor:
        for invite_code in urls:
            executor.submit(checker, invite_code, session, proxy)

if __name__ == "__main__":
    handler()
