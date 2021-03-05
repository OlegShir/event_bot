import requests
import csv
import constant
from sqlighter import SQLighter

# получаем адрес расположение мероприятия
def location_adress(id):
    url = 'https://speterburg.biglion.ru/deal-offer/'+ str(id) + '/places/'
    r = requests.get(url).json()
    
    long_adres = r['places'][0]['title']

    # убираем г. Санкт-Петербург из адреса
    if long_adres.find('Санкт'):
        short_adres = long_adres.replace('г. Санкт-Петербург,', '')
    else:
        short_adres = long_adres
            
    return short_adres.lstrip()

# получаем словарь данных с биглиона 
def get_json(url):
    r = requests.get(url)
    return r.json()

# получаем данные по каждому мероприятию
def get_data(json_text):
    # подключаемся к БД
    db = SQLighter('event_parse.db')
    
    # получаем id последнего проверенного мероприятия
    id_last_post = db.get_last_post('bigleon')
    
    # список словарей всех мероприятий 
    ads = json_text['data']['dealOffers']
    
    # сохраняем id первого мероприятия в полученном списке
    new_last_post = ads[0]['id']

    # создаем пустой список для дальшейшего добавления в него мероприятий
    events= []

    for ad in ads:
        # производим сравнение id каждого мероприятия с последним обработанным (записанным)
        if ad['id'] == id_last_post:
            break
        # производим получение данных из json для БД
        id_parse  = ad['id']
        type_event = ad['categoryTitle']
        img = ad['image']
        title = ad['title']
        cost = ad['price']
        discounted = ad['priceDiscounted']
        try:
            # получаем адрес по id мероприятия путем http запроса
            address = location_adress(id_parse)
        except:
            # если адреса нет, то это онлайн-мероприятие или где-то в лесу 
            address = 'None'
        metro = ad['locations'][0]['metro'] 
        try: 
            # проводим поиск станции метро в словаре constant.py
            district = constant.tuple_district[constant.dictonary_metro[metro]]  
        except:
            # метро для онлайн-мероприятий имеет значение РФ
            metro = ad['locations'][0]['address'] 
            if metro == "РФ":
                district = 'Онлаин'
            else:
                # в случае ошибки  
                district = 'None'
        link = ad['url'] 
        
        # добавляем мероприятие в список
        events.append((id_parse, type_event, img, title, cost, discounted, address, metro, district, link))
    
    # если список мероприятий не пустой
    if len(events) != 0:
        # записываем id последнего мероприятия
        db.update_last_post(new_last_post, 'bigleon')

        # записываем мероприятия в БД
        db.write_events(events)
        
    db.close()

def main():
    # в url возможно необходимо добавить фильтр
    url = 'https://speterburg.biglion.ru/api/v4/search/getSearchResults/?show_free=1&city=c_18&category=131&page=1&per_page=60&sort_type=start_date&sort_direction=desc'
    json_text = get_json(url)
    get_data(json_text) 


if __name__ == '__main__':
    main()