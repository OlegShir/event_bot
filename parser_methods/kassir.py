import format, json, re


def parser(last_post, info, event):
    ''' парсинг сайта KASSIR.RU осуществляется через библиотеку BeautifulSoup. Парсятся четыре веб-страницы: концерты,
        театр, спорт и детям. Нужная информация содержится в div с классом "col-xs-2" и 'event', а также в script от  
        https://schema.org с аттрибутом "application/ld+json" '''
    # создаем временные хранилища
    temporary_id = []
    temporary_event = []
    new_last_post = last_post
    # находим в супе дивы с классом "col-xs-2", содержащие события
    soup_events = info.find_all('div', class_="col-xs-2")
    # обрабатываем каждое событие с второго - нулевого нет, первое - реклама
    for soup_event in soup_events:
        try:
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
            if type_event == 'Другое':
                type_event = 'Разное'
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
            temporary_id.append(id_parse)
            temporary_event.append((id_parse, type_event, img, title, date_start, date_stop, cost, address, metro, full_link))
        except:
            continue
    new_events_index = [temporary_id.index(x) for x in list(set(temporary_id)-set(last_post))] 
    event = [temporary_event[x] for x in new_events_index]
    if new_events_index:
        new_last_post = temporary_id

    return event, new_last_post