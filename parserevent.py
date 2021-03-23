import requests
import constant
from sqlighter import SQLighter
from bs4 import BeautifulSoup as bs
import lxml


class ParserEvent:
    #parse_methods = {'kudago': self.parse_kudago, 'biglion': parse_bigleon}

    def __init__(self):
        self.web_sites = {'kudago': 'https://kudago.com/public-api/v1.4/events/?page_size=100&order_by=-publication_date&location=spb&expand=price,place,images,categories,dates,site_url&fields=id,title,price,place,images,dates,categories,site_url', \
                          'biglion': 'https://speterburg.biglion.ru/api/v4/search/getSearchResults/?show_free=1&city=c_18&category=131&page=1&per_page=60&sort_type=start_date&sort_direction=desc'}
        
    def get_html(self, url):
        r = requests.get(url)
        return r
 
    # преодразователь даты kudago 01-12-2021 -> 1 марта 2021
    def re_format_kudago(self, date):
        list_date = date.split('-')
        # удаление нуля в числе 
        number = int(list_date[2])
        re_format_date = str(number) + " " + constant.date_format_kudago[int(list_date[1])-1] + " " + list_date[0]
        return re_format_date
    
    # преобразователь в верхний регистр только первой буквы строки "концект Кота и СОБАКИ" -> "Концерт Кота и СОБАКИ"
    def first_word_upper(self, title):
        title_sep = title.split(' ')


    # получаем адрес расположение мероприятия для биглиона
    def data_event(self, url):
        html = self.get_html(url)
        text_html =  html.text
        soup = bs(text_html, 'lxml')
        # производим поиск меток в html начала и окончания мероприятия
        info_data = soup.find_all('p', class_='info__text')
        data_start = info_data[0].get_text()
        data_stop = info_data[1].get_text()

        return data_start, data_stop

    def parse_kudago(self, last_post, html):
        json_html = html.json()
        # список словарей всех мероприятий 
        ads = json_html['results']
        # сохраняем id первого мероприятия в полученном списке
        new_last_post = ads[0]['id']
        event = []
        for ad in ads:
            # производим сравнение id каждого мероприятия с последним обработанным (записанным)
            if ad['id'] == last_post:
               break
            # производим получение данных из json для БД
            id_parse  = ad['id']
            type_event_kudago = ad['categories'][0]
            try:
                type_event = constant.dictonary_event_kudago[type_event_kudago]
            except:
                type_event = "Разное"
            img = ad['images'][0]['thumbnails']['640x384']
            title = ad['title']
            cost = ad['price']
            discounted = 0
            try:
                address = ad['place']['address'] 
            except:
                address = None
            try:
                metro_list = ad['place']['subway'] 
                metro = metro_list.split(', ')[0]
            except:
                metro = None
            link = ad['site_url'] 
            try:
                date_start_info = ad['dates'][0]['start_date']
                date_start = self.re_format_kudago(date_start_info)
            except:
                date_start = None
            try:
                count_date_length = len(ad['dates'])
                if count_date_length == 1:
                    date_stop_info =  ad['dates'][0]['end_date'] 
                else:
                    date_stop_info =  ad['dates'][count_date_length-1]['start_date']
                date_stop = self.re_format_kudago(date_stop_info)
            except:
                date_stop = None
            if date_start == date_stop:
                date_stop = None
            # добавляем мероприятие в список
            event.insert(0, (id_parse, type_event, img, title, date_start, date_stop, cost, discounted, address, metro, link))
        return event, new_last_post

    def parse_bigleon(self, last_post, html):
        json_html = html.json()
        # список словарей всех мероприятий 
        ads = json_html['data']['dealOffers']
        # сохраняем id первого мероприятия в полученном списке
        new_last_post = ads[0]['id']
        # создаем пустой список для дальшейшего добавления в него мероприятий
        event = []
        for ad in ads:
            # производим сравнение id каждого мероприятия с последним обработанным (записанным)
            if ad['id'] == last_post:
                break
            # производим получение данных из json для БД
            # отсеиваем залетные мероприятия не в СПб
            if ad['locations'][0]['parsedAddress']['city'] != 'Санкт-Петербург':
                continue
            id_parse  = ad['id']
            type_event_biglion = ad['categoryTitle']
            try:
                type_event = constant.dictonary_event_biglion[type_event_biglion]
            except:
                type_event = "Разное"
            img = ad['image']
            title = ad['title']
            cost = str(ad['price']) + ' ' + 'рублей'
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
                address = None
            link = ad['url']  
            full_link = 'https://speterburg.biglion.ru/deals/' + link 
            data_start, data_stop = self.data_event(full_link)
            # добавляем мероприятие в список
            event.append((id_parse, type_event, img, title, data_start, data_stop, cost, discounted, address, metro, full_link))
        return event, new_last_post


    def main_parse(self):
        db = SQLighter('event_parse.db')
        events= []
        # производим перебор названия сайтов и их url-адресов
        for key, value in self.web_sites.items():
            # получаем последнее проверенное мероприятие
            last_post = db.get_last_post(key)
            # получаем данные с очередного сайта
            html = self.get_html(value)
            # определяем метод парсинга сайта
            #func_parse = self.parse_methods.get(key)
            # получаем данные по каждому мероприятию
            if key == 'kudago':
                event, new_last_post = self.parse_kudago(last_post, html)
            elif key == 'biglion':
                event, new_last_post = self.parse_bigleon(last_post, html)
            # если есть новые мероприятия на сайте 
            if len(event) != 0:
                # записываем id последнего мероприятия
                db.update_last_post(new_last_post, key)
                events.extend(event)
        # если список мероприятий не пустой
        if len(events) != 0:
            # записываем мероприятия в БД
            db.write_events(events)
        
        return events

            

       
       




