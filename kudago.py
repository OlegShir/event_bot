import requests
import csv
import constant

# запись в csv данных о мероприятиях
def write_csv(data):
    with open('event_kudago.csv', 'a', newline = '') as f:
        writer = csv.writer(f, delimiter = ',')

        writer.writerow( (data['id'],
                         data['image_post'],
                         data['title_post'],
                         data['url_post'],
                         data['price_discounted'],
                         data['price_post'],
                         data['discount_post'],
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

    last_post = open('last_post_kudago.txt', 'r+')
    id_last_post = int(last_post.read()) 

    ads = json_text['results']
    
    new_last_post = ads[0]['id']

    # print(type(new_last_post),type(id_last_post))

    for ad in ads:
        if ad['id'] == id_last_post:
            break
        id  = ad['id']
        image_post = ad['images'][0]['thumbnails']['640x384']
        title_post = ad['title']
        url_post = ad['site_url'] 
        price_discounted = 0
        price_post = ad['price']
        discount_post = 0
        try:
            metro_post = ad['place']['subway'] 
        except:
            metro_post = 'None'
        
        try: 
            disc = constant.tuple_district[constant.dictonary_metro_lower[metro_post.lower()]]  
        except:
            disc = 'None'

        data_post = {'id': id, 'image_post': image_post, 'title_post': title_post, 'url_post': url_post, \
            'price_discounted': price_discounted, 'price_post': price_post, 'discount_post': discount_post, \
            'metro_post': metro_post, 'disc': disc}

        write_csv(data_post) 

    last_post.seek(0)
    last_post.write(str(new_last_post))
    last_post.close()




def main():
    # в url
    url = 'https://kudago.com/public-api/v1.4/events/?page_size=100&order_by=-publication_date&location=spb&expand=price,place,images,,dates,site_url&fields=id,title,price,place,images,dates,site_url'
    json_text = get_json(url)
    get_data(json_text) 


if __name__ == '__main__':
    main()