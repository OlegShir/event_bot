###########################################
###########################################
###########################################
###########################################
###########################################
###########################################
###########################################
###########################################
###########################################
#(  0         1               2               3            4              5         6     7       8      9      10)
#(номер, тип события, ссылка на картинку, заголовок, дата начала, дата оканчания, цена, скидка, адрес, метро, ссылка) 

import constant

class BeautyCaption:

    def __init__(self, event):
        self.event = event
        self.caption = ''
    
    def get_caption(self):
        # значек мероприятия
        icon_event = constant.dictonary_icon_event[self.event[1]]
        # заголовок
        title = self.event[3][0].upper() + self.event[3][1:] 
        # время проведения 
        # если даты окончания нет -> один день
        if self.event[5] == None:
            date = self.event[4] 
        else:
            array = ['с', self.event[4], 'по', self.event[5]]
            date = ' '.join(array)
        # если отсутствует стоимость
        if (self.event[6] == '') | (self.event[6] == None):
            price = 'подродности в описании'
        else:
            price = self.event[6]
        # если отсутствует адрес
        if self.event[8] == None:
            address = ''
        else:
            address = constant.address + ' ' + self.event[8] + '\n' 
        # если отсутствует метро
        if (self.event[9] == '') | (self.event[9] == None):
            metro = ''
        else:
            metro = constant.metro + ' ' + self.event[9] + '\n'
        link =  constant.link + self.event[10]
        
        caption = icon_event + ' ' + title + '\n\n' + \
				  constant.data + ' ' + date + '\n' + \
				  constant.price + ' ' + price + '\n' + \
				  address + \
				  metro + \
				  link

        return caption

        '''
if __name__ == '__main__':
    event = (191321, 'Детям', 'https://kudago.com/media/thumbs/640x384/images/event/cb/f8/cbf8e4ea908f15a154a84f9f854b90b4.jpg', 'Всероссийская историческая интеллектуальная онлайн-игра', '17 марта 2021', None, '', 0, None, None, 'https://kudago.com/online/event/detyam-vserossijskaya-istoricheskaya-intellektualnaya-onlajn-igra/')
    bc = Beauty_caption(event)
    caption = bc.get_caption()
    print(caption)'''