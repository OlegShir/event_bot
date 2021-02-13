import requests
from bs4 import BeautifulSoup
import csv

# определяем новый ли пост
def biglion_find_new_post(post, last_post):
    # преобразование входных номеров постов в строку для их дальнейшего разделения: 4173332 -> 417  3332
    post_string = str(post)
    last_post_string = str(last_post)
    # получаем длину номера поста, если в будущем увеличется разряд
    post_length = len(post_string) 
    last_post_length = len(last_post_string)
    if (int(post_string[0:post_length-4]) >= int(last_post_string[0:last_post_length-4])) & \
        (int(post_string[post_length-4:post_length+1]) < int(last_post_string[last_post_length-4:last_post_length+1])):
        print('Yes')
    else: 
        print('No')

# получаем текст парсируемой страницы 
def get_html(url):
    r = requests.get(url)
    return r.text

# получаем данные по каждому мероприятию на странице
def get_html_data(html):
    soup = BeautifulSoup(html, 'lxml')

    ads = soup.find('div', class_='catalog__deals').find_all('div', class_ = 'card-item')

    for ad in ads:


def main():
    url = 'https://speterburg.biglion.ru/services/?category=131&pageNum=1&perPage=30&sortType=start_date&sortDirection=desc'
    html = get_html(url)
    get_html_data(html) 


if __name__ == '__main__':
    main()