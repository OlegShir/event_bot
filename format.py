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
'''string = 'г. Санкт-Петербург, ул. Советская, 5'
print(delete_SPB(string))'''

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
'''name_place = 'Сити-мол'
   address_place = 'Коломяжский пр., 17к'
   print(connect_full_address(name_place, address_place))'''

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
'''date = '1 апреля – 3 мая'
print(fiesta_date_format(date))'''

#_______________________________________________________
# метод форматирования даты события сайта kudago, kassir, kuda spb:
#
# 2021-03-01          -> 1 марта 2021
# 2021-03-01 19:00:00 -> 1 марта 2021
def kudago_and_kassir_date_format(date):
    # обрезаем длинный формат даты события (кассир)
    if len(date) > 10:
        # '2021-04-28 20:00:00' -> '2021-04-28'
        date =  date[0:10]
    list_date = date.split('-')
    # удаление нуля в числе 
    number = int(list_date[2])
    formated_date = f'{str(number)} {constant.date_format_kudago[int(list_date[1])-1]} {list_date[0]}'

    return formated_date

# ТЕСТ
'''date = '2021-04-28 20:00:00'
print(kudago_and_kassir_date_format(date))'''