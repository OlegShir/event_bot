''' Данный модуль предназначен для хранения методов форматирования данных, полученных с сайтов.
    Форматируются к единому виду: 
    1. Данные о дате проведения событий -> Дата Месяц Год.
    2. Адрес проведения мероприятия -> Место, Улица, Дом '''

import re, constant

#________________________________________________________________
# метод удаления из строки адреса регулярного выражения "Санкт-Петербург", "г. Санкт-Петербург" и т.д.
# г. Санкт-Петербург, ул. Советская, 5 -> ул. Советская, 5
# г. Санкт-Петербург -> ''
def delete_SPB(string):
    match = re.sub(r'\D*Санкт-Петербург([^\w]|$)', '', string).strip()
    
    return match

# ТЕСТ
'''
string = 'г. Санкт-Петербург, ул. Советская, 5'
print(delete_SPB(string))
'''

#_________________________________________________________________
# метод конкатенации названия площадки и адреса проведения события
# Сити-мол + '' -> Сити-мол
# Сити-мол + Коломяжский пр., 17к -> Сити-мол, Коломяжский пр., 17к
# '' + Коломяжский пр., 17к -> Коломяжский пр., 17к
# '' + '' -> ''
# 
#
def connect_full_address(name_place, address_place):
    if name_place and address_place:
        name_place += ', '
    full_address = name_place + address_place
    
    return full_address if full_address else None

# ТЕСТ
'''
name_place = 'Сити-мол'
address_place = 'Коломяжский пр., 17к'
print(connect_full_address(name_place, address_place))
'''

#____________________________________________________
# метод форматирования даты события сайта fiesta: 
# 
# 1 апреля, 2 апреля, 3 апреля -> 1 апреля | 3 апреля
# 1 апреля - 3 апреля          -> 1 апреля | 3 апреля
def fiesta_date_format(date):
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

# ТЕСТ
'''
date = '1 апреля – 3 мая'
print(fiesta_date_format(date))
'''

#_______________________________________________________
# метод форматирования даты события сайта kudago, kassir, kuda spb, peterburg_center:
#
# 2021-03-01          -> 1 марта 2021
# 2021-03-01 19:00:00 -> 1 марта 2021
# 18.04.2021          -> 18 апреля 2021
def date_format(date, type_sep):
    
    # обрезаем длинный формат даты события (кассир)
    if len(date) > 10:
        # '2021-04-28 20:00:00' -> '2021-04-28'
        date =  date[0:10]
    list_date = date.split(type_sep)
    month = int(list_date[1])-1
    # для КудаGo и Кассира разделение '-'
    if type_sep == '-':
            # удаление нуля в числе 
        day = int(list_date[2])
        year = list_date[0]
    # для Петербург Центра разделение '.'
    elif type_sep == '.':
        day = int(list_date[0])
        year = list_date[2]
        
    formated_date = f'{str(day)} {constant.list_month[month]} {year}'
        
    return formated_date

# ТЕСТ
'''
date = '2021-04-28 20:00:00'
print(date_format(date, '-'))

date2 = '18.04.2021'
print(date_format(date2, '.'))
'''

#_______________________________________________________
# метод разделения адреса события на сайте kassir
#
# 'БКЗ Октябрьский, Лиговский пр., д.6. ст.м. "Пл. Восстания"' -> 'БКЗ Октябрьский, Лиговский пр., д.6.', 'Пл. Восстания'
def sep_address_metro(address):
    # убираем html тэг &quot; из строки адреса
    address = address.replace('&quot;', '')
    metro = None
    result = re.search(r'м\.|метро|ст\.\s*метро|ст\.\s*м\.|ст\.\s*м', address, flags = re.IGNORECASE)
    if result:
        start_symbol = result.span()[0]
        end_symbol = result.span()[1]
   
        metro = address[end_symbol:].replace('\"', '').strip()
        if metro.find('.'):
            try:
                metro = metro.split('.')
                # ищем совпадение в списке станций
                metro = [x for x in constant.list_metro if re.findall(metro[-1].strip() , x)][0]
            except:
                metro = None

        address = address[0:start_symbol].strip()
      
    return address, metro

# ТЕСТ
'''
address = 'БКЗ Октябрьский, Лиговский пр., д.6. ст.м. "Пл. Восстания"'
print(sep_address_metro(address))
'''

#_______________________________________________________
# метод руб. -> 'рублей'
def rub_to_ruble(cost):
    new_cost = cost.replace('руб.', 'рублей')
    if len(re.findall(r'\—', new_cost)) == 1:
        cost_split = new_cost.split('—')
        new_cost = f'от {cost_split[0]}до{cost_split[1]}'
    
    return new_cost

# ТЕСТ
'''
cost = 'Взрослые — 550 руб. Учащиеся — 300 руб. Пенсионеры — 250 руб.'
cost2 = '150 — 550 руб.'
print(rub_to_ruble(cost), '\n', rub_to_ruble(cost2))
'''
