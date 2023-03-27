import requests
from bs4 import BeautifulSoup
url = "https://www.goldenmp3.ru/search.html"
querystring = {"text": "loveless my bloody valentine"}
payload = ""
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
}
response = requests.request(
    "GET", url, data=payload, headers=headers, params=querystring)
path = response.text.split('<dt><a href="/')[1].split('"')[0]
url = 'https://www.goldenmp3.ru/' + path
print(url)
response = requests.request("GET", url, data=payload, headers=headers)
soup = BeautifulSoup(response.text)
for i in soup.find_all('tr', {'itemprop': 'tracks'}):
    name = i.find('span', {'itemprop': 'name'}).text
    if name.upper() == "when you sleep".upper():
        print(i.find('a', {'class': 'play'})['rel'])
        stream_code = (i.find('a', {'class': 'play'})['rel'])
        print(stream_code)
        stream_url = f'https://listen.musicmp3.ru/{stream_code[0]}'
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Range': 'bytes=0-',
    'Connection': 'keep-alive',
    'Referer': 'https://www.goldenmp3.ru/',
    'Sec-Fetch-Dest': 'audio',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'Accept-Encoding': 'identity'
}
response = session.get(
    stream_url, headers=headers, stream=True)
i = 0
with open('2.mpeg', 'wb') as f:
    for chunk in response.iter_content(chunk_size=1024):
        f.write(chunk)
        print(i)
        i +=1
        if i == 500:
            break
response.close()
session.close()
