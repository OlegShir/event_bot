import format


def parser(last_post, info, event):  
    ads = info['data']
    # создаем временные хранилища
    temporary_id = []
    temporary_event = []
    new_last_post = last_post
    for ad in ads:
        try:
            id_event = ad['event']['id']
            id_parse = int(''.join([x for x in id_event[0:7] if x.isdigit()]))
            type_event = format.event_yandex.get(ad['event']['type']['code'], 'Разное')
            img = ad['event']['image']['sizes']['eventCoverL']['url']
            title = ad['event']['title']
            argument = ad['event'].get('argument', None)
            if argument:
                title = f'{title}. <i>{argument}</i>'
            date_start = format.date_format(ad['scheduleInfo']['dateStarted'], '-')
            date_stop = format.date_format(ad['scheduleInfo']['dateEnd'], '-')
            if date_start == date_stop: date_stop = None
            cost_min = ad['event']['tickets'][0]['price']['min']
            cost = f'от {round(int(cost_min)/100)} рублей'
            address_title = ad['scheduleInfo']['oneOfPlaces'].get('title', None)
            address = ad['scheduleInfo']['oneOfPlaces'].get('address', None)
            if address_title and address: address = f'{address_title}, {address}'
            metro = None
            full_link = f"https://afisha.yandex.ru{ad['event']['url']}"
            temporary_id.append(id_parse)
            temporary_event.append((id_parse, type_event, img, title, date_start, date_stop, cost, address, metro, full_link))
        except:
            print('В цикле Яндекс.Афиша произошла ошибка')
            continue
    new_events_index = [temporary_id.index(x) for x in list(set(temporary_id)-set(last_post))] 
    event = [temporary_event[x] for x in new_events_index]
    if new_events_index:
        for x in new_events_index:
            new_last_post.append(temporary_id[x])
        
    return event, new_last_post