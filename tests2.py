import requests
from bs4 import BeautifulSoup
url = "https://www.goldenmp3.ru/search.html"
querystring = {"text": "shes electric oasis"}
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
for i in soup.find_all('tr',{'itemprop':'tracks'}):
    name = i.find('span',{'itemprop':'name'}).text
    if name.upper() == "she's electric".upper():
        print(i.find('a',{'class':'play'})['rel'])
        break