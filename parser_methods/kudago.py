import format

def parser(last_post, info, event):
    # список словарей всех мероприятий 
    ads = info['results']
    # сохраняем id первого мероприятия в полученном списке
    new_last_post = ads[0]['id']
    for ad in ads:
        # производим сравнение id каждого мероприятия с последним обработанным (записанным)
        if ad['id'] == last_post: break
        # производим получение данных из json для БД
        id_parse  = ad['id']
        print(id_parse)
        type_event_kudago = ad['categories'][0]
        type_event = format.event_kudago.get(type_event_kudago, 'Разное')
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