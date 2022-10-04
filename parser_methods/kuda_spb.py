import format

def parser(last_post, info, event):
    # на сайте события хранятся в классе "events_list", но он разделен рекламой. Поэтому надо найти все эти классы
    soup_divide = info.find_all('div', class_="events_list")
    # затем объединить
    soup_events = []
    for divide in soup_divide:
        soup_events.extend(divide.find_all('div', class_ = 'event'))
    # создаем временные хранилища
    temporary_id = []
    temporary_event = []
    new_last_post = last_post
    
    for soup_event in soup_events:
        type_event_unformat = soup_event.find('div', class_= 'event_type').text.strip()
        type_event = format.event_kuda_spb.get(type_event_unformat, 'Разное')
        img = soup_event.find('img').get('src')
        title = soup_event.find('a', itemprop="url").get('title')
        date_start = format.date_format(soup_event.find('span', itemprop='startDate').text.strip(), '-')
        date_stop = format.date_format(soup_event.find('span', itemprop='endDate').text.strip(), '-')
        if date_start == date_stop:
            date_stop = None
        cost_data = soup_event.find('span', itemprop= 'price').text.strip()
        if not cost_data or int(cost_data) == 0:
            cost = 'Бесплатно'
        else:
            cost = f'от {cost_data} рублей'
        try:       
            name_place = format.delete_SPB(soup_event.find('div', itemprop='location').find('span', itemprop = 'name').text.strip())
            address_place = format.delete_SPB(soup_event.find('div', itemprop='location').find('span', itemprop = 'address').text.strip())
            address = format.connect_full_address(name_place, address_place)
        except Exception as error: 
            print(error)
            address = None
        metro = None
        full_link = soup_event.find('a', itemprop='url').get('href')
        # на сайте kuda_spb отсутствует id события -> вычисляем его по длине других значений
        id_parse = 2 * len(title) - len(img)

        temporary_id.append(id_parse)
        temporary_event.append((id_parse, type_event, img, title, date_start, date_stop, cost, address, metro, full_link))

    new_events_index = [temporary_id.index(x) for x in list(set(temporary_id)-set(last_post))] 
    event = [temporary_event[x] for x in new_events_index]
    if new_events_index:
        for x in new_events_index:
            new_last_post.append(temporary_id[x])

    return event, new_last_post