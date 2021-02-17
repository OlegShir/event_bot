import requests

url = 'https://speterburg.biglion.ru/deal-offer/4214498/places/'
r = requests.get(url).json()
    
long_adress = r['places'][0]['title']

    # убираем г. Санкт-Петербург из адреса
if long_adress.find('Санкт'):
    short_adress = long_adress.replace('г. Санкт-Петербург,', '')
else:
    short_adress = long_adress
            
print(short_adress.lstrip())