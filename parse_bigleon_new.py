import requests
import csv

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
                         data['metro_post']) )


# получаем словарь данных с биглиона 
def get_json(url):
    r = requests.get(url)
    return r.json()

# получаем данные по каждому мероприятию
def get_data(json_text):
    # получаем id последнего проверенного мероприятия
    # потом надо через with
    last_post = int(open('last_post_biglion.txt').read())
    ads = json_text['data']['dealOffers']
    
    new_last_post = ads[0]['id']
    print(type(new_last_post),type(last_post))

    for ad in ads:
        if ad['id'] == last_post:
            break
        id  = ad['id']
        image_post = ad['image']
        title_post = ad['title']
        url_post = ad['url'] 
        price_discounted = ad['priceDiscounted']
        price_post = ad['price']
        discount_post = ad['discount']
        metro_post = ad['locations'][0]['metro']          

        data_post = {'id': id, 'image_post': image_post, 'title_post': title_post, 'url_post': url_post, \
            'price_discounted': price_discounted, 'price_post': price_post, 'discount_post': discount_post, \
            'metro_post': metro_post}

        write_csv(data_post)  
 
        



def main():
    # в url возможно необходимо добавить фильтр
    url = 'https://speterburg.biglion.ru/api/v4/search/getSearchResults/?show_free=1&city=c_18&per_page=60&category=131'
    json_text = get_json(url)
    get_data(json_text) 


if __name__ == '__main__':
    main()