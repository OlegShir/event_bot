import requests
import csv

# получаем текст парсируемой страницы 
def get_html(url):
    r = requests.get(url)
    return r.text

# получаем общее количество страниц
def get_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    total_pages = soup.find('div', class_='catalog__pagination').find('a', class_ = 'btn-arrow').get('href')[-1]

    return int(total_pages)

# запись в csv данных о мероприятиях
def write_csv(data):
    with open('event_list.csv', 'a', newline = '') as f:
        writer = csv.writer(f, delimiter = ',')

        writer.writerow( (data['title'],
                         data['place'],
                         data['price'],
                         data['discount'],
                         data['href_img'],
                         data['href_event']) )

# получаем данные по каждому мероприятию на странице
def get_html_data(html):
    soup = BeautifulSoup(html, 'lxml')

    ads = soup.find('div', class_='catalog__deals').find_all('div', class_ = 'card-item')

    for ad in ads:
        # return название - title, место - place, цена - price, скидка - discount, 
        # ссылка на картинку - href_img, ссылка на мероприятие - href_event
        try:
            title_list = ad.find('a', class_='card-item__title').text.strip().split()
            title = ' '.join(title_list)
        except:
            continue

        try:
            place= ad.find('span', class_ = 'address__text').text
        except:
            place = ''

        try:
            price_list = ad.find('span', class_ = 'price__new').text.strip().split()
            price = ' '.join(price_list)
        except:
            price = ''

        try:
            discount = ad.find('span', class_ = 'card-item__discount').text
        except:
            discount = ''
        
        try:
            href_img = ad.find('img', class_ = 'card-item__img').get('src')
        except:
            href_img = ''

        try:
            href_end_url = ad.find('a', class_ = 'card-item__box').get('href')
            href_event = 'https://speterburg.biglion.ru' + href_end_url
        except:
            href_event = ''
        
        # создание словаря

        date_event = {'title': title, 'place': place, 'price': price, 'discount': discount, 'href_img': href_img, 'href_event': href_event}

        write_csv(date_event)



def main():
    url = 'https://speterburg.biglion.ru/services/entertainment/?page=1'
    base_url = 'https://speterburg.biglion.ru/services/entertainment/?page='
    
    total_pages = get_pages(get_html(url))
    
    for i in range(1, total_pages+1):
        url_gen = base_url + str(i)
        html = get_html(url_gen)
        get_html_data(html) 


if __name__ == '__main__':
    main()
