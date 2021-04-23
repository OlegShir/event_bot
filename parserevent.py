import requests
import constant, format
from sqlighter import SQLighter
from bs4 import BeautifulSoup as bs
import json
import re

# декоратор контроя парсинга событий
def control_parse_events(func):
    def wrapper(self, key, last_post, info):
        event = []
        new_last_post = last_post
        print('\nПарсинг сайта: ', key)
        try:
            event, new_last_post = func(self, last_post, info, event)
            print(f"Найдено: {len(event)} новых событий")

        except Exception as error:
            print(f'При парсенге {key} возникла ошибка:\n{error.__class__.__name__}: {error}')

        return event, new_last_post

    return wrapper

# get-запрос на сайты 
def get_info(url, type_parse):
    '''в зависимости от типа парсинга определяется его метод type_parse:
       - BeautifulSoup при поиске на страницах событий;
       - json при взаимодействии с API'''

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    r = requests.get(url, headers = headers)
    r.encoding = 'utf-8'

    if type_parse == 'bs4':
        # варим суп текста страницы
        info = bs(r.text, 'html.parser')
        
    elif type_parse == 'json':
        # преобразуем в словарь
        info = r.json()

    return info

class ParserEvent:
    # начальные свойства сайтов событий 'название метода парсинга: [адрес парсинга, тип парсинга]'
    def __init__(self):
        self.web_sites = {'kudago':          ['https://kudago.com/public-api/v1.4/events/?page_size=100&order_by=-publication_date&location=spb&expand=price,place,images,categories,dates,site_url&fields=id,title,price,place,images,dates,categories,site_url', 'json'], \
                          'biglion':         ['https://speterburg.biglion.ru/api/v4/search/getSearchResults/?show_free=1&city=c_18&category=131&page=1&per_page=60&sort_type=start_date&sort_direction=desc', 'json'], \
                          'kassir_koncert':  ['https://spb.kassir.ru/bilety-na-koncert?sort=1', 'bs4'], \
                          'kassir_teatr' :   ['https://spb.kassir.ru/bilety-v-teatr?sort=1' , 'bs4'], \
                          'kassir_detyam':   ['https://spb.kassir.ru/detskaya-afisha?sort=1', 'bs4'],
                          'fiesta':          ['https://www.fiesta.ru/spb/novelty/events/', 'bs4'],
                          'kuda_spb':        ['https://kuda-spb.ru/event/', 'bs4'],
                          'peterburg_center':['https://peterburg.center/events-next', 'bs4']\
                          
        }
    # выбор метода парсинга в main_parse в завизимости от ключа self.web_sites
    def dispatch(self, key, last_post, info):
        
        method = getattr(self, key)

        return method(key, last_post, info)
       
    # получаем адрес расположение мероприятия для биглиона
    def data_event(self, url):
        info = get_info(url, 'bs4')
        # производим поиск меток в html начала и окончания мероприятия
        info_data = info.find_all('p', class_='info__text')
        data_start = info_data[0].get_text()
        data_stop = info_data[1].get_text()

        return data_start, data_stop
    
    @control_parse_events
    def peterburg_center(self, last_post, info, event):
        main_url = 'https://peterburg.center'
        # получаем список div-ов, содержащих ссылки на страницы событий
        soup_hrefs = info.find('div', class_ = 'views-responsive-grid').find_all('div', class_ = 'card_bottom_right')
        new_last_post = last_post
        for number, soup_href in enumerate(soup_hrefs[1:5]):
            # получаем ссылки на страницу событий
            href = soup_href.find('a').get('href')
            full_href = main_url + href
            html_event = get_info(full_href, 'bs4')
            soup_event = html_event.find('article')
            # id события содержит буквы и цифры
            id_parse_with_letter = soup_event.attrs['id']
            # удаляем буквы
            id_parse = re.findall("\d+", id_parse_with_letter)[0]

            if int(id_parse) == int(last_post): break
            if number == 0: new_last_post = id_parse

            type_event_site = soup_event.find('div', class_ = 'field-name-field-event-category').find('a').get_text()
            type_event = constant.dictonary_event_peterburg_center[type_event_site]
            title = soup_event.find('h1').get_text()
            img = soup_event.find('div', class_ = 'image-center').find('a').get('href')
            date_start_parse = soup_event.find('div', class_ = 'field-name-field-date-from').find('span').get_text()
            date_stop_parse = soup_event.find('div', class_ = 'field-name-field-date-till').find('span').get_text()
            date_start = format.date_format(date_start_parse, '.')
            date_stop = format.date_format(date_stop_parse, '.')
            if date_start == date_stop: date_stop = None
            try:
                cost = soup_event.find('div', class_ = 'field-name-field-cost').find('div', class_ = 'field-item even').get_text()
                cost = format.rub_to_ruble(cost)
            except:
                cost = None
            address = format.delete_SPB(soup_event.find('div', class_ = 'field-name-field-place').find('div', class_ = 'field-item even').get_text())
            metro = None
       
            event.append((id_parse, type_event, img, title, date_start, date_stop, cost, address, metro, full_href))

        return event, new_last_post

    @control_parse_events
    def kuda_spb(self, last_post, info, event):
        # на сайте события хранятся в классе "events_list", но он разделен рекламой. Поэтому надо найти все эти классы
        soup_divide = info.find_all('div', class_="events_list")
        # затем объединить
        soup_events = []
        for divide in soup_divide:
            soup_events.extend(divide.find_all('div', class_ = 'event'))
        new_last_post = last_post
        
        for number, soup_event in enumerate(soup_events):
            type_event_unformat = soup_event.find('div', class_= 'event_type').text.strip()
            type_event = constant.dictonary_event_kuda_spb.get(type_event_unformat, 'Разное')
            img = soup_event.find('img').get('src')
            title = soup_event.find('a', itemprop="url").get('title')
            date_start = format.date_format(soup_event.find('span', itemprop='startDate').text.strip(), '-')
            date_stop = format.date_format(soup_event.find('span', itemprop='endDate').text.strip(), '-')
            if date_start == date_stop:
                date_stop = None
            cost_data = soup_event.find('span', itemprop= 'price').text.strip()
            if int(cost_data) == 0:
                cost = 'Бесплатно'
            else:
                cost = f'от {cost_data} рублей'            
            name_place = format.delete_SPB(soup_event.find('div', itemprop='location').find('span', itemprop = 'name').text.strip())
            address_place = format.delete_SPB(soup_event.find('div', itemprop='location').find('span', itemprop = 'address').text.strip())
            address = format.connect_full_address(name_place, address_place)
            metro = None
            full_link = soup_event.find('a', itemprop='url').get('href')
            # на сайте kuda_spb отсутствует id события -> вычисляем его по длине других значений
            id_parse = 2 * len(title) - len(img)

            if int(id_parse) == int(last_post): break
            if number == 0: new_last_post = id_parse
            
            event.append((id_parse, type_event, img, title, date_start, date_stop, cost, address, metro, full_link))

        return event, new_last_post

    @control_parse_events
    def fiesta(self, last_post, info, event):
        soup_events = info.find_all('div', class_="grid_i grid_i__desktop-grid-1-3 grid_i__tablet-grid-1-2 grid_i__phone-grid-1-1")
        new_last_post = last_post
        for number, soup_event in enumerate(soup_events):
            id_parse = soup_event.find('footer').attrs['data-calendar-item']

            if int(id_parse) == int(last_post): break
            if number == 0: new_last_post = id_parse

            type_event = 'Развлечения' # !!!!!!!!!!
            title = soup_event.find('a', class_='unit_t_a double-hover').get_text()
            # получаем дату события
            date = soup_event.find('p', class_='unit_date').get_text()
            date_start, date_stop = format.fiesta_date_format(date)
            full_link = 'https://www.fiesta.ru' + soup_event.find('a', class_='unit_t_a double-hover').get('href')
            
            # получение цены
            cost_html_event = get_info(full_link, 'bs4')
            cost = cost_html_event.find('div', class_='article_details').find_all('dd', class_='grid_i grid_i__desktop-grid-5-6 grid_i__tablet-grid-5-6 grid_i__phone-grid-1-1')[-1].get_text().strip()
            # если чтоимости нет -> то в cost попадает дата события, необходимо проверить ее наличие
            if any(x in cost for x in constant.list_month):
                cost = None             
            try:
                full_address = soup_event.find('p', class_='unit_place').get_text()
                # адрес может содержать название метро
                if full_address.find(';') != -1:
                    full_address = full_address.split(';')[0]
                if full_address.startswith('м.'):
                    sep_full_address = full_address.split(',')
                    address = ''.join(sep_full_address[1:]).strip()
                    metro_long = sep_full_address[0].split(' ')
                    metro = ' '.join(metro_long[1:]).strip()
                else:
                    address = full_address
                    metro = None
            except:
                address = None
                metro = None
            # картинки на событий в главном окне имеют низкое расширение -> парсим каждую страницу события
            img_html = get_info(full_link, 'bs4')
            img_link = img_html.find('img', itemprop = 'image').get('src')
            img = 'https://www.fiesta.ru' + img_link

            event.append((id_parse, type_event, img, title, date_start, date_stop, cost, address, metro, full_link))

        return event, new_last_post

    @control_parse_events       
    def kudago(self, last_post, info, event):
        # список словарей всех мероприятий 
        ads = info['results']
        # сохраняем id первого мероприятия в полученном списке
        new_last_post = ads[0]['id']
        for ad in ads:
            # производим сравнение id каждого мероприятия с последним обработанным (записанным)
            if ad['id'] == last_post: break
            # производим получение данных из json для БД
            id_parse  = ad['id']
            type_event_kudago = ad['categories'][0]
            type_event = constant.dictonary_event_kudago.get(type_event_kudago, 'Разное')
            img = ad['images'][0]['thumbnails']['640x384']
            title = ad['title']
            cost = ad.get('price', None)
            place = ad.get('place', None)
            if place:
                address_place = place.get('address', None)
                name_place = place.get('title', None)
                address = format.connect_full_address(name_place, address_place)
                metro = place.get('subway', None)
                if metro:
                    metro = metro.split(', ')[0]
            else:
                address = None
                metro = None

            link = ad['site_url'] 
            try:
                date_start_info = ad['dates'][0]['start_date']
                date_start = format.date_format(date_start_info, '-')
            except:
                date_start = None
            try:
                count_date_length = len(ad['dates'])
                if count_date_length == 1:
                    date_stop_info =  ad['dates'][0]['end_date'] 
                else:
                    date_stop_info =  ad['dates'][count_date_length-1]['start_date']
                date_stop = format.date_format(date_stop_info, '-')
            except:
                date_stop = None
            if date_start == date_stop:
                date_stop = None
            # добавляем мероприятие в список
            event.insert(0, (id_parse, type_event, img, title, date_start, date_stop, cost, address, metro, link))

        return event, new_last_post

    @control_parse_events
    def biglion(self, last_post, info, event):
        # список словарей всех мероприятий 
        ads = info['data']['dealOffers']
        # сохраняем id первого мероприятия в полученном списке
        new_last_post = ads[0]['id']
        # создаем пустой список для дальшейшего добавления в него мероприятий
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
            type_event = constant.dictonary_event_kudago.get(type_event_biglion, 'Разное')
            img = ad['image']
            title = ad['title']
            priceDiscounted = ad['priceDiscounted']
            price = ad['price']
            cost = f'<s>{price}</s> {priceDiscounted} рублей'
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
            event.append((id_parse, type_event, img, title, data_start, data_stop, cost, address, metro, full_link))

        return event, new_last_post

    @control_parse_events
    def kassir(self, last_post, info, event):
        ''' парсинг сайта KASSIR.RU осуществляется через библиотеку BeautifulSoup. Парсятся четыре веб-страницы: концерты,
            театр, спорт и детям. Нужная информация содержится в div с классом "col-xs-2" и 'event', а также в script от  
            https://schema.org с аттрибутом "application/ld+json" '''
        # находим в супе дивы с классом "col-xs-2", содержащие события
        soup_events = info.find_all('div', class_="col-xs-2")
        # сохраняем id первого мероприятия в полученном списке
        # создаем пустой список для дальшейшего добавления в него мероприятий
        new_last_post = last_post
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
                cost = f'{str(max_cost)} рублей'
            else:
                cost = f'от {str(min_cost)} до {str(max_cost)} рублей'
            # дата события
            date = first_part_event['date']
            # если дата события не один день, то она хранится в виде словаря
            if type(date) == dict:
                date_start = format.date_format(first_part_event['date']['start_min'], '-')
                date_stop = format.date_format(first_part_event['date']['start_max'], '-')
            # если один день
            else:
                date_start = format.date_format(date, '-')
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
            # адрес проведения события b наличие годода Санк-Петербур
            address_place, metro = format.sep_address_metro(format.delete_SPB(second_part_event['location']['address']))
            # добавляем перед адресом название места проведения события
            name_place = second_part_event['location']['name'].replace('\"', '')
            address = f"{name_place}, {address_place}"
            # ссылка на событие
            full_link = second_part_event['url']
            # добавляем мероприятие в список
            event.append((id_parse, type_event, img, title, date_start, date_stop, cost, address, metro, full_link))

        return event, new_last_post

    def main_parse(self):
        db = SQLighter('event_parse.db')
        events= []
        # производим перебор названия сайтов и их url-адресов
        for key, value in self.web_sites.items():
            # получаем последнее проверенное мероприятие
            last_post = db.get_last_post(key)
            # определяем метод парсинга сайта
            if (key == 'kassir_koncert') or (key == 'kassir_teatr') or (key == 'kassir_detyam'):
                key = 'kassir'
            # получаем данные с очередного сайта
            info = get_info(value[0], value[1])
            event, new_last_post = self.dispatch(key, last_post, info)
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

            

       
       




