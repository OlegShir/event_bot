#(  0         1               2               3            4              5         6     7      8     9)
#(номер, тип события, ссылка на картинку, заголовок, дата начала, дата оканчания, цена, адрес, метро, ссылка) 

import constant

class BeautyCaption:

    def __init__(self, event):
        self.event = event
        self.caption = ''
    
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
        address = f'{constant.address} {self.event[7]} <a>https://maps.google.com/?q={self.event[7]}</a>\n' if self.event[7] else ''

        # если отсутствует метро
        metro = f'{constant.metro} {self.event[8]}\n' if self.event[8] else ''
                
        link =  f'{constant.link} {self.event[9]}'
        
        caption = f'{icon_event} {title}\n\n{date}{constant.price} {price}\n{address}{metro}{link}'

        return caption

#
'''
if __name__ == '__main__':
    event = (191648, 'Отдых', 'https://kudago.com/media/thumbs/640x384/images/event/5d/6f/5d6fe7d5640cd4a513c4d108c3dfb4fe.jpg', 'забеги Parkrun', None, None, '', 0, None, None, 'https://kudago.com/spb/event/recreation-zabegi-parkrun/')
    bc = BeautyCaption(event)
    caption = bc.get_caption()
    print(caption)'''