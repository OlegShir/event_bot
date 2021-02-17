import requests
import csv
import constant

# получаем адрес расположение мероприятия
def location_adress(id):
    url = 'https://speterburg.biglion.ru/deal-offer/'+ str(id) + '/places/'
    r = requests.get(url).json()
    
    long_adres = r['places'][0]['title']

    # убираем г. Санкт-Петербург из адреса
    if long_adres.find('Санкт'):
        short_adres = long_adres.replace('г. Санкт-Петербург,', '')
    else:
        short_adres = long_adres
            
    return short_adres.lstrip()

# запись в csv данных о мероприятиях
def write_csv(data):
    with open('event_list.csv', 'a', newline = '') as f:
        writer = csv.writer(f, delimiter = ',')

        writer.writerow( (data['id'],
                         data['image_post'],
                         data['title_post'],
                         data['url_post'],
                         data['price_discounted'],
                         data['price_post'],
                         data['discount_post'],
                         data['adres'],
                         data['metro_post'],
                         data['disc']) )

# получаем словарь данных с биглиона 
def get_json(url):
    r = requests.get(url)
    return r.json()

# получаем данные по каждому мероприятию
def get_data(json_text):
    # получаем id последнего проверенного мероприятия
    # потом надо через with

    last_post = open('last_post_biglion.txt', 'r+')
    id_last_post = int(last_post.read()) 
    
    # список словарей всех мероприятий 
    ads = json_text['data']['dealOffers']
    
    # сохраняем id первого мероприятия в полученном списке
     
    new_last_post = ads[0]['id']

    # print(type(new_last_post),type(id_last_post))

    for ad in ads:
        if ad['id'] == id_last_post:
            break
        id  = ad['id']
        image_post = ad['image']
        title_post = ad['title']
        url_post = ad['url'] 
        price_discounted = ad['priceDiscounted']
        price_post = ad['price']
        discount_post = ad['discount']
        try:
            adres = location_adress(id)
        except:
            adres = 'None'

        metro_post = ad['locations'][0]['metro'] 
        
        try: 
            disc = constant.tuple_district[constant.dictonary_metro[metro_post]]  
        except:
            metro_post = ad['locations'][0]['address'] 
            if metro_post == "РФ":
                disc = 'Онлаин'
            else:
                disc = 'None'

        data_post = {'id': id, 'image_post': image_post, 'title_post': title_post, 'url_post': url_post, \
            'price_discounted': price_discounted, 'price_post': price_post, 'discount_post': discount_post, \
            'adres': adres, 'metro_post': metro_post, 'disc': disc}

        write_csv(data_post) 

    last_post.seek(0)
    last_post.write(str(new_last_post))
    last_post.close()
        



def main():
    # в url возможно необходимо добавить фильтр
    url = 'https://speterburg.biglion.ru/api/v4/search/getSearchResults/?show_free=1&city=c_18&category=131&page=1&per_page=60&sort_type=start_date&sort_direction=desc'
    json_text = get_json(url)
    get_data(json_text) 


if __name__ == '__main__':
    main()