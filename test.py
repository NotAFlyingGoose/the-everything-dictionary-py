import requests, urllib.parse, time, sys
from datetime import datetime

proxy = 'https://www.whateverorigin.org/get?url='

def request():
    response = requests.get(proxy + urllib.parse.quote_plus('https://google.com'), headers={
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate',
                'accept-language': 'en-US,en;q=0.5',
                'host': 'www.whateverorigin.org',
                'referer': 'localhost:5500',
                'origin': 'localhost:5500',
                'connection': 'keep-alive',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0'
            })
    return response.headers.__contains__('access-control-allow-origin')

if __name__ == '__main__':
    a = 0
    for i in range(100):
        if request():
            a += 1
        print(('\033[A' if i>0 else '') + str(i+1) + '% done')
    print('\033[A100% done')
    print('Can access ' + str(a) + '%')