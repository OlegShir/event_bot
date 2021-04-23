#(  0         1               2               3            4              5         6     7      8     9)
#(номер, тип события, ссылка на картинку, заголовок, дата начала, дата оканчания, цена, адрес, метро, ссылка) 

import constant
import re
from geocoderMetro import geocoderMetro

g_m = geocoderMetro()

class BeautyCaption:

    def __init__(self, event):
        self.event = event
        self.caption = ''

    def delete_spec_symbol(self, string):
        if string: new_string = re.sub(r'\"', '', string)
        else:  new_string  = string
        return new_string
    
    def get_caption(self):
        # выбор значка эмодзи для события
        icon_event = constant.dictonary_icon_event[self.event[1]]
        
        # установка названия события с большой буквы
        title = self.event[3][0].upper() + self.event[3][1:]
        
        # форматирования даты события: если есть конец -> то 'с ... по ...', иначе только начало, либо ''
        if self.event[4] and self.event[5]:
            date = f'{constant.data} с {self.event[4]} по {self.event[5]}\n' 
        elif self.event[4] and not self.event[5]:
            date = f'{constant.data} {self.event[4]}\n' 
        else:
            date = ''
        
        # форматирование стоимости события: если она отсутствует -> 'подродности в описании'
        price = self.event[6] if self.event[6] else 'подродности в описании'
        
        # если отсутствует адрес
        address_for_link = self.delete_spec_symbol(self.event[7])
        address = f'{constant.address} <a href=\"https://maps.google.com/?q={address_for_link}\">{self.event[7]}</a>\n' if {self.event[7]} else ''

        # если отсутствует метро
        if not self.event[8]:
            metro_station = g_m.get_metro(address_for_link)
        metro = f'{constant.metro}{metro_station}\n' if metro_station else ''
                
        link =  f'{constant.link} {self.event[9]}'
        
        caption = f'{icon_event} {title}\n\n{date}{constant.price} {price}\n{address}{metro}{link}'

        return caption

#

if __name__ == '__main__':
    event = ('37265', 'Обучение', 'https://peterburg.center/sites/default/files/img/event_m/2021-03/len-zoo.jpg', 'Библионочь-2021: От зверинца – к зоопарку', '24 апреля 2021', None, None, 'Никольская пл., 2 (Библиотека "Старая Коломна")', None, 'https://peterburg.center/event/biblionoch-2021-ot-zverinca-k-zooparku.html')
    bc = BeautyCaption(event)
    caption = bc.get_caption()
    print(caption)