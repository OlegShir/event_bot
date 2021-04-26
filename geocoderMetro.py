''' Модуль принимает адрес события и возращеет ближайшее метро.
    Используются API Google для получения координат адреса события
    и API Yandex для получения ближайшего метро. Разделение сделано
    для того, чтобы уложится в бесплатные лимиты запросов (Яндекс -1000/день,
    Гугл - 200$/месяц)'''

import requests, json, constant
from DashboardYandex import DashboardYandex as dash_yandex
'''
def control_class_geocoderMetro(func):
    def wrapper(self, address):
        try:
            metro = func(self, address)
        except:
            print('Ошибка при определении ближайшего метро')
            metro = None

        return metro
    
    return wrapper
'''
def get_json(url):
    r = requests.get(url)
    return r.json()

class geocoderMetro:

    def __init__(self):
        self.base_google = f'https://maps.googleapis.com/maps/api/geocode/json?language=ru&key={constant.API_GOOGLE}&address=Санкт-Петербург,'
        self.base_yandex = f'https://geocode-maps.yandex.ru/1.x/?kind=metro&results=1&format=json&apikey={constant.API_YANDEX}&geocode='

    def get_metro(self, address):
        metro = None
        # контролим лимит Яндекса
        geo = dash_yandex()
        limit = geo.get_limit_apimaps()
        if address and limit <= 1000:
            # форматируем адрес под Гугл
            google_address = address.replace(' ', '%20')
            # создаем строку запроса для Гугл
            request_url_google = f'{self.base_google}{google_address}'
            respon_google = get_json(request_url_google)

            if respon_google['status'] != 'OK': 
                return
            
            latitude = respon_google['results'][0]['geometry']['location']['lat']
            longitude = respon_google['results'][0]['geometry']['location']['lng']

            # создаем строку запроса для Яндекса
            request_url_yandex = f'{self.base_yandex}{longitude},{latitude}'
            respon_yandex = get_json(request_url_yandex)
            
            try:            
                metro_full = respon_yandex['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']
                metro = metro_full.replace('метро ', '')
            except:
                print(f'Ближайшее метро не найдено для адреса:\n{address}')        
        else: 
            print('Ошибка: кончился лимит запросов на Яндексе или нет адреса')
         
        return metro 


# ТЕСТ
'''
address = 'Санкт-Петербург, Великие Луки, ул.Зверева, д.29'
bs = geocoderMetro()
merto = bs.get_metro(address)
print((merto))
'''