import requests
import constant
from sqlighter import SQLighter
from bs4 import BeautifulSoup as bs
import lxml

# получаем адрес расположение мероприятия
def data_event(url):
    html = get_html(url)
    text_html =  html.text
    soup = bs(text_html, 'lxml')

    # производим поиск меток в html начала и окончания мероприятия
    info_data = soup.find_all('p', class_='info__text')
    data_start = info_data[0].get_text()
    data_stop = info_data[1].get_text()

    return data_start, data_stop

# получаем json ответ с сайта 
def get_html(url):
    r = requests.get(url)
    return r

# получаем данные по каждому мероприятию
def get_data(html):
    # подключаемся к БД
    db = SQLighter('event_parse.db')
    
    # получаем id последнего проверенного мероприятия
    id_last_post = db.get_last_post('biglion')
    
    json_html = html.json()

    # список словарей всех мероприятий 
    ads = json_html['data']['dealOffers']
    
    # сохраняем id первого мероприятия в полученном списке
    new_last_post = ads[0]['id']

    # создаем пустой список для дальшейшего добавления в него мероприятий
    events= []

    for ad in ads:
        # производим сравнение id каждого мероприятия с последним обработанным (записанным)
        if ad['id'] == id_last_post:
            break
        # производим получение данных из json для БД
        # отсеиваем залетные мероприятия не в СПб
        if ad['locations'][0]['parsedAddress']['city'] != 'Санкт-Петербург':
            continue
        id_parse  = ad['id']
        type_event = ad['categoryTitle']
        img = ad['image']
        title = ad['title']
        cost = ad['price']
        discounted = ad['priceDiscounted']
        metro = ad['locations'][0]['metro'] 
        # если в названии метро есть скобки в которых указывается цвек линнии - убираем
        try:
            # если поикст возращает ошибку, то метро нет - онлайн или по питеру
            scobka = metro.find("(")
            if scobka != -1:
                metro = metro[0:scobka-1]
        except:
            metro = None

        address = ad['locations'][0]['friendlyAddress']
        if address == '':
            address = 'По городу'
        #if ad['locations'][0]['аddress'] == 'РФ':
         #   address = 'Онлайн'

        link = ad['url']  
        full_link = 'https://speterburg.biglion.ru/deals/' + link 

        data_start, data_stop = data_event(full_link)
        
        # добавляем мероприятие в список
        events.append((id_parse, type_event, img, title, data_start, data_stop, cost, discounted, address, metro, full_link))
        
    # если список мероприятий не пустой
    if len(events) != 0:
        # записываем id последнего мероприятия
        db.update_last_post(new_last_post, 'biglion')

        # записываем мероприятия в БД
        db.write_events(events)
    db.close()

def main():
    # в url возможно необходимо добавить фильтр
    url = 'https://speterburg.biglion.ru/api/v4/search/getSearchResults/?show_free=1&city=c_18&category=131&page=1&per_page=60&sort_type=start_date&sort_direction=desc'
    html = get_html(url)
    get_data(html) 

if __name__ == '__main__':
    main()