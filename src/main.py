from curl_cffi.requests import Session
from bs4 import BeautifulSoup

import config

from time import sleep

from re import compile


def valueFromString(s : str) -> str:
    s = s.replace(',', '.').replace('\u2009', '')
    
    
    wasDec = False
    start, end = 0, 0
    for en, i in enumerate(s):
        if not wasDec and i.isdecimal():
            start = en
            wasDec = True
            continue
        elif wasDec and (not i.isdecimal() and not i == '.'):
            end = en
            break
    return s[start:end] if end != 0 else '0'

def sendMsg(session : Session, st : int, priceDelta : int, url : str) -> bool:
    match st:
        case 0:
            params = {'chat_id' : config.YOUR_ID, 'text' : f'🔔 Изменение на {priceDelta} Обычной цены\n{url}'}
        case 1:
            params = {'chat_id' : config.YOUR_ID, 'text' : f'🔔 Изменение на {priceDelta} Ozon-счёта\n{url}'}
        case other:
            print('Didn\'t match any cases, verify that')
            return False
    
    if not config.API_KEYS:
        print('You didn\'t define any API_KEY')
        exit(1)
        
    if not config.YOUR_ID or not config.YOUR_ID[0]:
        print('You didn\'t define YOUR_ID')
        exit(2)

    for API_KEY in config.API_KEYS:
        res = session.get(f'https://api.telegram.org/bot{API_KEY}/sendMessage', params=params)
        if res.status_code == 200:
            return True

    return False
            
def mainP():
    session = Session(headers=config.HEADERS, impersonate = 'chrome110')
    prices : list[list[int]] = []
    
    isPricesFilled = False

    with open('urls.txt', 'r') as file:
        urls = [x.strip('\n') for x in file.readlines()]
    
    while True:
        for enum, url in enumerate(urls):
            
            
            if not url or (not 'ozon.ru' in url):
                continue
            url = url.strip('\n')
            
            res = session.get(url)
            if res.status_code != 200:
                print(f'\n{url}\ngave code: {res.status_code}')
                urls[enum] = ''
                prices.append([])
                continue
            
            soup = BeautifulSoup(res.content, 'html.parser')
            
            try:
                tmp = soup.find_all(string=compile('₽'), limit=3)
                
                price = int(valueFromString(tmp[0])) # type: ignore
                price2 = 0
                if 'Картой' in tmp[2]:
                    price2 = int(valueFromString(tmp[2])) # type: ignore
            except:
                print(f'\n{url}\nThis product is over at line {enum + 1}')
                urls[enum] = ''
                prices.append([])
                continue
            
            if not isPricesFilled:
                prices.append([price, price2])
            elif price != prices[enum][0]:
                if not sendMsg(session, 0, price - prices[enum][0], url):
                    print('Failed all attempts to send message, check what\'s worng')
            elif price2 != prices[enum][1]:
                if not sendMsg(session, 1, price2 - prices[enum][1], url):
                    print('Failed all attempts to send message, check what\'s worng')
                    

        if not isPricesFilled: isPricesFilled = True
        
        sleep(600) # should be "600" ; = 10 min
        
if __name__ == '__main__':
    mainP()
