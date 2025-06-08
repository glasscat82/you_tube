import sys, random
import json
from datetime import datetime as dt
import requests
from art import tprint


SUFFIX = '~'

def pc(text: str, *args, color: int = 6):
    """ 1 red, 2 green, 3 yello, 4 blue, 5 purple, 6 blue """
    print(f'\033[3{color}m{text}', *args, sep=' / ', end='\033[0m\n')

def wtf(html, filename):
    with open(filename, "w") as f:
        f.write(html)

def write_json(data, path):
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)  

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    except Exception as e:
        pc(f'[-] 26 → {sys.exc_info()[1]}', color = 1)
        return False

def get_html(url_page: str):
    """ return HTML """
    header = None
    try:        
        page =  requests.get(url_page, headers=header, cookies={'CONSENT': 'YES+cb.20210328-17-p0.en-GB+FX+{}'.format(random.randint(100, 999))})
        return page.text

    except Exception as e:
        pc(sys.exc_info()[1], color = 1)
        return False

def get_cooki(url: str):
    # Создать объект сессии  
    session = requests.Session()
    # Отправить запрос на YouTube
    session.get(url)  
    # Распечатать сохранённые куки  
    pc("[+] Cookies после первого посещения YouTube:", color=2)   
    pc(session.cookies.get_dict(), color=2)

    return session.cookies.get_dict()

def get_json(html: str) -> bool|dict:
    """ return dict """
    try:
        s = '{"responseContext":'
        t0 = html.find(s)
        t1 = html.find(';</script>', t0)
        h = html[t0:t1]
        data = json.loads(h)

    except Exception as e:
        pc(sys.exc_info()[1], color = 1)
        return False

    return data

if __name__ == '__main__':
    """ parsing YouTube """
    
    now = dt.now()
    #---------------start
    tprint('::youtube::', font='cybermedium', sep='\n')

    pc('[+] Enter login YouTube chanel: ', color=3)
    x = input()

    login = x.replace('@', '')
    url = f'https://www.youtube.com/@{login}/videos'
    pc(f'[+] {url}', color=3)
    
    html = get_html(url)
    if html is False:
        pc('[-] error', color=1)

    data = get_json(html)
    if data is False:
        pc('[-] error', color=1)

    wtf(html, f'./html/{login}-{now:%d-%m-%Y_%H}.html')
    write_json(data, f'./json/{login}-{now:%d-%m-%Y_%H}.json')

    if 'metadata' not in data or 'channelMetadataRenderer' not in data['metadata']:
        pc('[-] error', color=1)

    meta = data['metadata']['channelMetadataRenderer']

    pc(f'{SUFFIX * 50}', color=2)    
    pc(f'[+] {meta["title"]}', color=2)
    pc(f'[+] RSS: {meta["rssUrl"]}', color=2)
    pc(f'[+] ID: {meta["externalId"]}', color=2)
    pc(f'{meta["description"]}', color=5)
    pc(f'{SUFFIX * 50}', color=2)
   
    #---------------end
    end = dt.now()
    pc(f'[+] the end → {str(end - now)}', color = 6) 