import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.connection.row_factory = lambda cursor, row: row[0]
        self.cursor = self.connection.cursor()
        
    def get_last_post(self, website):
        """Получение последнего обработанного поста с сайта"""
        with self.connection:
            result = self.cursor.execute("SELECT id_post FROM last_post WHERE website = ?", (website,)).fetchone()
            print(result, type(result))
            return int(result)
    
    def update_last_post(self, new_last_post, website):
        """Обновление значения последнего обработанного поста с сайта"""
        with self.connection:
            self.cursor.execute("UPDATE last_post SET id_post = ? WHERE website = ?", (new_last_post, website))
            return self.connection.commit()

    def write_events(self, events):
        """Записываем список мероприятий в БД"""
        with self.connection:
            return self.cursor.executemany("INSERT INTO event(id_parse, type, img, title, cost, discounted, address, metro, district, link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", events)

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()