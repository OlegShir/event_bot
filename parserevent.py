import requests
import constant
from sqlighter import SQLighter
from bs4 import BeautifulSoup as bs
import lxml
import json
import re

class ParserEvent:
    #parse_methods = {'kudago': self.parse_kudago, 'biglion': parse_bigleon}

    def __init__(self):
        self.web_sites = {'kudago':          'https://kudago.com/public-api/v1.4/events/?page_size=100&order_by=-publication_date&location=spb&expand=price,place,images,categories,dates,site_url&fields=id,title,price,place,images,dates,categories,site_url', \
                          'biglion':         'https://speterburg.biglion.ru/api/v4/search/getSearchResults/?show_free=1&city=c_18&category=131&page=1&per_page=60&sort_type=start_date&sort_direction=desc', \
                          'kassir_koncert':  'https://spb.kassir.ru/bilety-na-koncert?sort=1', \
                          'kassir_teatr' :   'https://spb.kassir.ru/bilety-v-teatr?sort=1', \
                          'kassir_detyam':   'https://spb.kassir.ru/detskaya-afisha?sort=1',
                          'fiesta':          'https://www.fiesta.ru/spb/novelty/events/'\
                          
        }

    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
        r = requests.get(url, headers = headers)
        return r

    def fiesta_data_format(self, date):
        symbol = [',', '–']
        try:
            symbol_sep = [s for s in symbol if s in date]
            if symbol_sep:
                date_array = date.split(symbol_sep[0])
                date_start = date_array[0].strip()
                date_stop = date_array[-1].strip()
            else:
                date_start = date
                date_stop = None
        except:
            date_start = None
            date_stop = None
        return date_start, date_stop
 
    # преодразователь даты kudago 01-03-2021 -> 1 марта 2021
    def re_format_kudago_and_kassir(self, date):
        # обрезаем длинный формат даты события (кассир)
        if len(date) > 10:
            # '2021-04-28 20:00:00' -> '2021-04-28'
            date =  date[0:10]
        list_date = date.split('-')
        # удаление нуля в числе 
        number = int(list_date[2])
        re_format_date = str(number) + " " + constant.date_format_kudago[int(list_date[1])-1] + " " + list_date[0]
        return re_format_date
    
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
    
    def parse_fiesta(self, last_post, html):
        text_html = html.text
        soup_html = bs(text_html, 'html.parser')
        soup_events = soup_html.find_all('div', class_="grid_i grid_i__desktop-grid-1-3 grid_i__tablet-grid-1-2 grid_i__phone-grid-1-1")
        
        event = []
        for soup_event in soup_events:
            id_parse = soup_event.find('footer').attrs['data-calendar-item']


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
                date_start = self.re_format_kudago_and_kassir(date_start_info)
            except:
                date_start = None
            try:
                count_date_length = len(ad['dates'])
                if count_date_length == 1:
                    date_stop_info =  ad['dates'][0]['end_date'] 
                else:
                    date_stop_info =  ad['dates'][count_date_length-1]['start_date']
                date_stop = self.re_format_kudago_and_kassir(date_stop_info)
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

    def parse_kassir(self, last_post, html):
        
        # парсинг сайта KASSIR.RU осуществляется через библиотеку BeautifulSoup. Парсятся четыре веб-страницы: концерты,
        # театр, спорт и детям. Нужная информация содержится в div с классом "col-xs-2" и 'event', а также в script от  
        # https://schema.org с аттрибутом "application/ld+json"
    
        # оставляем от запроса только текст
        text_html = html.text
        # варим суп текста страницы
        soup_html = bs(text_html, 'html.parser')
        # находим в супе дивы с классом "col-xs-2", содержащие события
        soup_events = soup_html.find_all('div', class_="col-xs-2")
        # сохраняем id первого мероприятия в полученном списке
        # создаем пустой список для дальшейшего добавления в него мероприятий
        new_last_post = last_post
        event = []
        # обрабатываем каждое событие с второго - нулевого нет, первое - реклама
        for number, soup_event in enumerate(soup_events[2:22]):
            # получаем первую часть информации о событии: id, цена, дата, тип 
            json_string = soup_event.find('div', class_='event').attrs['data-ec-item']
            
            # пробуем получить словарь из json_string
            try: 
                first_part_event = json.loads(json_string)
            # в json_string возможно будут исключения типа "" -> удаляем их
            except:
                try:
                    new_json_string = re.sub(r'[^:]""',' ', json_string).replace(' "', ' ').replace('" ', ' ')
                    first_part_event = json.loads(new_json_string)
                except:
                    continue
            print(first_part_event)
            print(number)
            # id события
            id_parse = first_part_event['id']
            # производим сравнение id каждого мероприятия с последним обработанным (записанным)
            if id_parse == last_post:
                break
            # сохраняем id первого мероприятия в полученном списке
            if number == 0:
                new_last_post = id_parse
            # минимальная и максимальная стоимость события
            min_cost = first_part_event['minPrice']
            max_cost = first_part_event['maxPrice']
            # формируем строку стоимости
            if min_cost == max_cost:
                cost = str(max_cost) + ' рублей'
            else:
                cost = 'от ' + str(min_cost) + ' до ' + str(max_cost) + ' рублей'
            # дата события
            date = first_part_event['date']
            # если дата события не один день, то она хранится в виде словаря
            if type(date) == dict:
                date_start = self.re_format_kudago_and_kassir(first_part_event['date']['start_min'])
                date_stop = self.re_format_kudago_and_kassir(first_part_event['date']['start_max'])
            # если один день
            else:
                date_start = self.re_format_kudago_and_kassir(date)
                date_stop = None
            # категория
            type_event = first_part_event['category']

            # получаем вторую часть информации о событии в script: image, title, address, link 
            try:
                second_part_event = json.loads(str(soup_event.find('script', type="application/ld+json").string))
            except:
                continue
            # ссылка на изображения события
            img = second_part_event['image']
            # название события
            title = second_part_event['name']
            discounted = 0
            # адрес проведения события
            address_place = second_part_event['location']['address']
            # проверяем наличие годода Санк-Петербург в адресе
            if address_place.startswith('Санкт'):
                # если есть убираем
                address_spb = address_place.split(', ')
                address_place = ', '.join(address_spb[1:])
            # добавляем перед адресом название места проведения события
            address = second_part_event['location']['name'] + ", " + address_place
            # МЕТРО В РАЗРАБОТКЕ
            metro = None
            # ссылка на событие
            full_link = second_part_event['url']
            # добавляем мероприятие в список
            event.append((id_parse, type_event, img, title, date_start, date_stop, cost, discounted, address, metro, full_link))
            print(id_parse, type_event, img, title, date_start, date_stop, cost, discounted, address, metro, full_link)
        print(event)
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
            elif (key == 'kassir_koncert') or (key == 'kassir_teatr') or (key == 'kassir_detyam'):
                event, new_last_post = self.parse_kassir(last_post, html)
            elif key == 'fiesta':
                event, new_last_post = self.parse_fiesta(last_post, html)
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

            

       
       




