import json, emoji


kino_genre = {
    'action': emoji.emojize(":bomb:", use_aliases=True), # 💣
    'detective': emoji.emojize(":man_detective:", use_aliases=True), # 🕵️‍♂️
    'drama': emoji.emojize(":performing_arts:", use_aliases=True), # 🎭
    'comedy': emoji.emojize(":smile:", use_aliases=True), # 😄
    'romance': emoji.emojize(":heart:", use_aliases=True), # ❤️
    'adventure': emoji.emojize(":face_with_cowboy_hat:", use_aliases=True), # 🤠
    'tragicomedy': emoji.emojize(":performing_arts:", use_aliases=True), # 🎭
    'thriller': emoji.emojize(":eyes:", use_aliases=True), # 👀
    'horror': emoji.emojize(":scream:", use_aliases=True), # 😱
    'fiction': emoji.emojize(":crystal_ball:", use_aliases=True), # 🔮
    'cartoon': emoji.emojize(":carousel_horse:", use_aliases=True), # 🎠
    'documentary': emoji.emojize(":notebook:", use_aliases=True), # 📓
    'family_movie': emoji.emojize(":family:", use_aliases=True), # 👪
    'short-films': emoji.emojize(":stopwatch:", use_aliases=True), # ⏱️
    'other': emoji.emojize(":performing_arts:", use_aliases=True), # 🎥
}

def parser(last_post, info, event):
    new_last_post = last_post
    title = 'Премьеры в кино на этой недели\n\n'
    kinos = info.find_all('div', class_ = 'event events-list__item yandex-sans')
    for kino in kinos:
        description = kino.find('div', class_="i-react event-card-react i-bem").attrs['data-bem']
        description_json = json.loads(description)
        gennre_kino = description_json['event-card-react']['props']['statEntry']['event_tags'][0]
        kino_icon = kino_genre.get(gennre_kino, kino_genre['other'])
        title_kino = description_json.get('event-card-react', '').get('props', '').get('title', '')
        title_kino_icon = f'{kino_icon} {title_kino}'
        annotation = description_json.get('event-card-react', '').get('props', '').get('argument', '') 
        description_json.get('event-card-react', '').get('props', '').get('title', '')
        rating_val = description_json.get('event-card-react', '').get('props', '').get('rating', '')
        if rating_val:
            rating = f"Рейтинг: {rating_val.get('value', '')}\n"
        else:
            rating = ''
        title = f'{title}<b>{title_kino_icon}</b>\n<i>{annotation}</i>\n{rating}\n'
        if len(title) > 800:
            break
    # маячек
    id_parse = 0
    type_event = 'Кино'
    img = '' 
    date_start = date_stop = cost = address = metro = ''
    full_link = 'https://afisha.yandex.ru/saint-petersburg/cinema?source=menu&filter=week-premiere'

    event.append((id_parse, type_event, img, title, date_start, date_stop, cost, address, metro, full_link))
        
    return event, new_last_post