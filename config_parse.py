import parser_methods.kudago as kudago
import parser_methods.kassir as kassir
import parser_methods.fiesta as fiesta
import parser_methods.kuda_spb as kuda_spb
import parser_methods.peterburg_center as peterburg_center
import parser_methods.afisha_kino_primer as afisha_kino_primer 
import parser_methods.yandex_afisha as yandex_afisha


config = {
    'Куда ГО':          [kudago, 'https://kudago.com/public-api/v1.4/events/?page_size=100&order_by=-publication_date&location=spb&expand=price,place,images,categories,dates,site_url&fields=id,title,price,place,images,dates,categories,site_url', 'json', False, {'day': [], 'hour': []}], \

    'Кассир Концерты':  [kassir, 'https://spb.kassir.ru/bilety-na-koncert?sort=1', 'bs4', True, {'day': [], 'hour': []}], \

    'Кассир Театр' :    [kassir, 'https://spb.kassir.ru/bilety-v-teatr?sort=1' , 'bs4', True], \

    'Кассир Детям':     [kassir, 'https://spb.kassir.ru/detskaya-afisha?sort=1', 'bs4', True], \

    'Фиеста':           [fiesta, 'https://www.fiesta.ru/spb/novelty/events/', 'bs4', False, {'day': [], 'hour': []}], \

    'Куда СПБ':         [kuda_spb, 'https://kuda-spb.ru/event/', 'bs4', True , {'day': [], 'hour': []}], \

    'Кино-примьеры':    [afisha_kino_primer, 'https://afisha.yandex.ru/saint-petersburg/cinema?source=menu&filter=week-premiere', 'bs4', False, {'day': [4], 'hour': [17]}], \

    'Петербург-центр':  [peterburg_center, 'https://peterburg.center/events-next', 'bs4', True, {'day': [], 'hour': []}], \

    'Яндекс.Афиша':  [yandex_afisha, 'https://afisha.yandex.ru/api/events/selection/nearest-events?limit=20&offset=0&hasMixed=0&city=saint-petersburg', 'json', True, {'day': [], 'hour': []}]
    
} 