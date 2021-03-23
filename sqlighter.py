import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        
    def get_last_post(self, website):
        """Получение последнего обработанного поста с сайта"""
        with self.connection:
            result = self.cursor.execute("SELECT id_post FROM last_post WHERE website = ?", (website,)).fetchone()
            return int(result[0])
    
    def update_last_post(self, new_last_post, website):
        """Обновление значения последнего обработанного поста с сайта"""
        with self.connection:
            self.cursor.execute("UPDATE last_post SET id_post = ? WHERE website = ?", (new_last_post, website))
            return self.connection.commit()

    def write_events(self, events):
        """Записываем список мероприятий в БД"""
        with self.connection:
            return self.cursor.executemany("INSERT INTO event(id_parse, type, img, title, data_start, data_stop, cost, discounted, address, metro,  link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", events)

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже пользователь в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM user WHERE user_id = ?', (user_id,)).fetchall()
            print(result)
            return bool(len(result))

    def add_subscriber(self, user_id, status = True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO user(user_id, status) VALUES(?,?)", (user_id, status))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE user SET status = ? WHERE user_id = ?", (status, user_id))

    def get_subscriptions(self, status = True):
            """Получаем всех активных подписчиков бота"""
            with self.connection:
                return self.cursor.execute("SELECT * FROM user WHERE status = ?", (status,)).fetchall() 
    
    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()