import emoji

API_TOKEN = '1773806846:AAGrojRK_Z5BOc00NW5gfdAb4didLqFrFLc'
ADMIN = 435001186


dictonary_metro = {'Пушкинская': 0, 'Технологический институт': 0, 'Балтийская': 0, 'Сенная площадь': 0, 'Технологический институт': 0,
                   'Фрунзенская': 0, 'Спасская': 0, 'Садовая': 0, 'Звенигородская': 0, 'Приморская': 1, 'Василеостровская': 1,
                   'Лесная': 2, 'Выборгская': 2, 'Парнас': 2, 'Проспект Просвещения': 2, 'Озерки': 2, 'Удельная': 2, 'Девяткино': 3,
                   'Гражданский проспект': 3, 'Академическая': 3, 'Политехническая': 3, 'Площадь Мужества': 3, 'Площадь Ленина': 3,
                   'Нарвская': 4, 'Кировский завод': 4, 'Автово': 4, 'Ленинский проспект': 4, 'Проспект Ветеранов': 4, 'Новочеркасская': 5,
                   'Ладожская': 5, 'Московские ворота': 6, 'Электросила': 6, 'Парк Победы': 6, 'Московская': 6, 'Звёздная': 6, 'Купчино':  6,
                   'Елизаровская': 7, 'Ломоносовская': 7, 'Пролетарская': 7, 'Обухово': 7, 'Рыбацкое': 7, 'Проспект Большевиков': 7,
                   'Улица Дыбенко': 7, 'Петроградская': 8, 'Горьковская': 8, 'Зенит': 8, 'Крестовский остров': 8, 'Чкаловская': 8, 'Спортивная': 8,
                   'Пионерская': 9, 'Чёрная речка': 9, 'Беговая': 9, 'Комендантский проспект': 9, 'Старая Деревня': 9, 'Шушары': 9,
                   'Обводный канал': 10, 'Волковская': 10, 'Бухарестская': 10, 'Международная': 10, 'Проспект Славы': 10, 'Дунайская': 10,
                   'Чернышевская': 11, 'Площадь Восстания': 11, 'Владимирская': 11, 'Невский проспект': 11, 'Гостиный двор': 11, 'Маяковская': 11,
                   'Достоевская': 11, 'Лиговский проспект': 11, 'Площадь Александра Невского': 11, 'Адмиралтейская': 11
                   }

dictonary_district = ('Адмиралтейский', 'Василеостровский', 'Выборгский', 'Калининский', 'Кировский', 'Красногвардейский', 'Московский', 'Невский',
                      'Петроградский', 'Приморский', 'Фрунзенский', 'Центральный'
                      )

dictonary_event_kudago = {
    "business-events": "Разное",
    "cinema": "Развлечения",
    "concert": "Концерт",
    "education": "Обучение",
    "entertainment": "Развлечения",
    "exhibition": "Выставки",
    "fashion": "Красота",
    "festival": "Развлечения",
    "holiday": "Развлечения",
    "kids": "Детям",
    "other": "Разное",
    "party": "Развлечения",
    "photo": "Разное",
    "quest": "Развлечения",
    "recreation": "Отдых",
    "shopping": "Товары",
    "social-activity": "Разное",
    "stock": "Товары",
    "theater": "Театр",
    "tour": "Экскурсии",
    "yarmarki-razvlecheniya-yarmarki": "Развлечения"
}

dictonary_event_biglion = {
    'Красота': 'Красота',
    'Здоровье': 'Здоровье',
    'Рестораны': 'Рестораны',
    'Развлечения': 'Развлечения',
    'Обучение': 'Обучение',
    'Авто': 'Товары',
    'Фитнес': 'Спорт',
    'Концерты': 'Концерт',
    'Дети': 'Детям',
    'Разное': 'Разное'
}

date_format_kudago = ("января", "февраля", "марта", "апреля", "мая", "июня", "июля",
                      "августа", "сентября", "октября", "ноября", "декабря")

# emoji
data = emoji.emojize(":calendar: ", use_aliases=True)  # 📅
price = emoji.emojize(":moneybag: ", use_aliases=True)  # 💰
metro = emoji.emojize(":metro:  м. ", use_aliases=True)  # 🚇
address = emoji.emojize(":world_map: ", use_aliases=True)  # 🗺️
raiting = emoji.emojize(":star: ", use_aliases=True)  # 🌟
link = emoji.emojize(":link: ", use_aliases=True)  # 🔗


dictonary_icon_event = {
             'Развлечения': emoji.emojize(":ferris_wheel:", use_aliases=True), # 🎡
             'Обучение': emoji.emojize(":mortar_board:", use_aliases=True), # 🎓
             'Концерт': emoji.emojize(":ticket:", use_aliases=True), # 🎫
             'Детям': emoji.emojize(":boy:" + ":girl:", use_aliases=True), # 👦👧
             'Разное': emoji.emojize(":cyclone:", use_aliases=True), # 🌀
             'Товары': emoji.emojize(":shopping_bags:", use_aliases=True), # 🛍️
             'Красота': emoji.emojize(":nail_care:", use_aliases=True), # 💅
             'Здоровье': emoji.emojize(":hospital:", use_aliases=True), # 🏥
             'Рестораны': emoji.emojize(":ice_cream:", use_aliases=True), # 🍨
             'Отдых': emoji.emojize(":desert_island:", use_aliases=True), # 🏝️
             'Выставки': emoji.emojize(":frame_with_picture:", use_aliases=True), # 🖼️
             'Экскурсии': emoji.emojize(":classical_building:", use_aliases=True), # 🏛️
             'Театр': emoji.emojize(":dolls:", use_aliases=True), # 🎎
             'Спорт': emoji.emojize(":first_place_medal:", use_aliases=True), # 🥇
             'Туристам': emoji.emojize(":man_walking:", use_aliases=True) # 🚶‍♂️
}

