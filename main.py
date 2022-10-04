#import schedule, time
import config_parse, format
from Postgres import Postgres


# словарь для парсинга сайтов
web_sites = config_parse.config

# декоратор контроя парсинга событий
def control_parse_events(func) -> list:
    def wrapper(parse_method, key, last_post, info):
        event = []
        new_last_post = last_post
        try:
            method = func(parse_method)
            event, new_last_post = method(last_post, info, event)
            print(f"При парсенге {key} найдено: {len(event)} новых событий")

        except Exception as error:
            print(f'При парсенге {key} возникла ошибка:\n{error.__class__.__name__}: {error}')

        return event, new_last_post

    return wrapper

@control_parse_events                      
def dispatch(parse_method):
    '''Возвращает метод парсинга в зависимости от ключа в web_sites'''
    method = getattr(parse_method, 'parser')
    return method

def main_parse() -> None:

    db = Postgres()
        # производим перебор названия сайтов и их url-адресов
    for key, value in web_sites.items():
        try:
            # проверяем нужно ли парсить сейчас
            if format.do_need_to_parse_now(key, value[4]):
                # получаем последнее проверенное мероприятие
                last_post = db.get_last_post(key, value[3])
                # определяем метод парсинга сайта
                info = format.get_info(value[1], value[2])
                event, new_last_post = dispatch(value[0], key, last_post, info)
                # если есть новые мероприятия на сайте 
                if event:
                    try:
                        # записываем id последнего мероприятия
                        db.update_last_post(key, new_last_post, value[3])
                        # записываем мероприятия в БД
                        db.write_events(event)
                        db.connection.commit()
                    except Exception as error:
                        print(f'При записи данных из {key} возникла ошибка:\n{error.__class__.__name__}: {error}')
        except Exception as error:
            print(f'При выполнении основной функции парсинга {key}:\n{error.__class__.__name__}: {error}')  
        
    if db.connection:
        db.cursor.close()
        db.close()
        
if __name__ == '__main__':
    pass