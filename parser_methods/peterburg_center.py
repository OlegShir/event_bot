import format, re

def parser(last_post, info, event):
    main_url = 'https://peterburg.center'
    # получаем список div-ов, содержащих ссылки на страницы событий
    soup_hrefs = info.find('div', class_ = 'views-responsive-grid').find_all('div', class_ = 'card_bottom_right')
    # создаем временные хранилища
    temporary_id = []
    temporary_event = []
    new_last_post = last_post
    for soup_href in soup_hrefs[0:50]:
        # получаем ссылки на страницу событий
        href = soup_href.find('a').get('href')
        full_href = main_url + href
        html_event = format.get_info(full_href, 'bs4')
        soup_event = html_event.find('article')
        # id события содержит буквы и цифры
        id_parse_with_letter = soup_event.attrs['id']
        # удаляем буквы
        id_parse = int(re.findall("\d+", id_parse_with_letter)[0])
        
        type_event_site = soup_event.find('div', class_ = 'field-name-field-event-category').find('a').get_text()
        type_event = format.event_peterburg_center[type_event_site]
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

        temporary_id.append(id_parse)
        temporary_event.append((id_parse, type_event, img, title, date_start, date_stop, cost, address, metro, full_href))
    
    new_events_index = [temporary_id.index(x) for x in list(set(temporary_id)-set(last_post))] 
    event = [temporary_event[x] for x in new_events_index]
    
    if new_events_index:
        for x in new_events_index:
            new_last_post.append(temporary_id[x])

    return event, new_last_post