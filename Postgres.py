import psycopg2, os
from psycopg2.extras import execute_values

DATABASE_URL = os.environ['DATABASE_URL']

class Postgres:

    def __init__(self):
        """Инициализация подключение к БД через окружение"""
        self.connection = psycopg2.connect(DATABASE_URL)
        self.cursor = self.connection.cursor()
        
    def get_last_post(self, website, is_array_value):
        """Получение последнего обработанного поста с сайта"""
        table = 'last_post'
        if is_array_value:
            table = 'last_post_array'
        with self.connection:
            self.cursor.execute("SELECT id_post FROM %s WHERE website = %%s;" % table, (website,))
            result = self.cursor.fetchone()
            return result[0]
    
    def update_last_post(self, website, new_last_post, is_array_value):
        """Обновление значения последнего обработанного поста с сайта"""
        table = 'last_post'
        if is_array_value:
            table = 'last_post_array'
        with self.connection:
            self.cursor.execute("UPDATE %s SET id_post = %%s WHERE website = %%s;" % table, (new_last_post, website,))
            return self.connection.commit()

    def write_events(self, events):
        """Записываем список мероприятий в БД"""
        with self.connection:
            insert_query = 'INSERT INTO event(id_parse, type, img, title, data_start, data_stop, cost, address, metro,  link) VALUES %s'
            execute_values(self.cursor, insert_query, events, template=None, page_size=100)

    def add_website_parse(self, website, start_post, is_array_value):
        """Добавляем новый сайт для пассинга. Возможно два варианта:
           1. Для парсинга используется массив ключей array_value = True, count - длина массива.
           2. Для парсинга используется целое число"""
        table = 'last_post'
        if is_array_value:
            table = 'last_post_array'
            start_post = [start_post]
        with self.connection:
                return self.cursor.execute("INSERT INTO %s (website, id_post) VALUES(%%s, %%s);" % table,  (website, start_post,))
    
    def export_table_to_csv(self, table, file_name = 'out_file.csv'):
        """Экспорт таблицы из PostgreSQL в CSV-фаил.
           table - название таблицы"""
        with open(file_name, 'w', errors='backslashreplace') as out_file:
            self.cursor.copy_expert(f'COPY {table} TO STDOUT WITH CSV HEADER', out_file)

    def clear_table_event(self):
        """Очистка базы данных событий"""
        with self.connection:
            self.cursor.execute("TRUNCATE event RESTART IDENTITY;")
            self.update_last_post('last_event', 0, False)
            return self.connection.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()


