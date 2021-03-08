import requests
import constant
from sqlighter import SQLighter

# получаем json ответ с сайта  
def get_html(url):
    r = requests.get(url)
    return r

# получаем данные по каждому мероприятию
def get_data(html):

    # подключаемся к БД
    db = SQLighter('event_parse.db')

    # получаем id последнего проверенного мероприятия
    id_last_post = db.get_last_post('kudago')

    json_html = html.json()
    
    # список словарей всех мероприятий 
    ads = json_html['results']

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

        type_event_kudago = ad['categories'][0]
        type_event = constant.dictonary_event_kudago[type_event_kudago]

        img = ad['images'][0]['thumbnails']['640x384']
        title = ad['title']
        cost = ad['price']
        discounted = 0
        try:
            address = metro = ad['place']['address'] 
        except:
            address = None
        try:
            metro_list = ad['place']['subway'] 
            metro = metro_list.split(', ')[0]
        except:
            metro = None
        
        link = ad['site_url'] 
        try:
            date_start = ad['dates'][0]['start_date']
            data_start = constant.re_format_kudago(date_start)
        except:
            data_start = None
        try:
            data_stop = len(ad['dates'])
        except:
            data_stop = None
        
        # добавляем мероприятие в список
        events.append((id_parse, type_event, img, title, data_start, data_stop, cost, discounted, address, metro, link))

    # если список мероприятий не пустой
    if len(events) != 0:
        # записываем id последнего мероприятия
        db.update_last_post(new_last_post, 'kudago')

        # записываем мероприятия в БД
        db.write_events(events)
    db.close()



def main():
    # в url
    url = 'https://kudago.com/public-api/v1.4/events/?page_size=100&order_by=-publication_date&location=spb&expand=price,place,images,categories,dates,site_url&fields=id,title,price,place,images,dates,categories,site_url'
    html = get_html(url)
    get_data(html) 


if __name__ == '__main__':
    main()