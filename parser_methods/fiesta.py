import format


def parser(last_post, info, event):
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
        cost_html_event = format.get_info(full_link, 'bs4')
        cost = cost_html_event.find('div', class_='article_details').find_all('dd', class_='grid_i grid_i__desktop-grid-5-6 grid_i__tablet-grid-5-6 grid_i__phone-grid-1-1')[-1].get_text().strip()
        # если чтоимости нет -> то в cost попадает дата события, необходимо проверить ее наличие
        if any(x in cost for x in format.list_month):
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
        img_html = format.get_info(full_link, 'bs4')
        img_link = img_html.find('img', itemprop = 'image').get('src')
        img = 'https://www.fiesta.ru' + img_link

        event.append((id_parse, type_event, img, title, date_start, date_stop, cost, address, metro, full_link))

    return event, new_last_post