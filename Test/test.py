import logging
import asyncio
from datetime import datetime

import aiogram.utils.markdown as fmt

from beauty_caption import BeautyCaption

from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram import Bot, Dispatcher, executor, types
import constant
# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token='1784660311:AAFZmMz58ww3p_fWghToqyWg5EYI4eFHR8M')
dp = Dispatcher(bot)

# иницилизация картинок эмодзи в описании события 
'''
price = emoji.emojize(":moneybag: ", use_aliases = True)
metro = emoji.emojize(":metro: м. ", use_aliases = True)
adress = emoji.emojize(":world_map: ", use_aliases = True)
raiting = emoji.emojize(":star: ", use_aliases = True)
link = emoji.emojize(":link: ", use_aliases = True)



@dp.message_handler()
async def echo(message: types.Message):
	with open('a.jpg', 'rb') as photo:
		await message.answer_photo(photo, caption=bold(title_event) + '\n\n' + \
			price + '1800'+'\n' + metro + 'Просвещение'+'\n'+ adress +'Просвещение 23'+'\n' + \
			link + link_event, parse_mode=ParseMode.MARKDOWN)
'''

link_event = 'https://speterburg.biglion.ru/deals/spa-programma-vibiray2-54/'
title_event = 'SPA-программа «Май», «Пляж», «Сила камня», «Восточная сказка», «Сладкие грезы», «Тайский шепот» в салоне Simmetria SPA'
photo ='https://cdn.kassir.ru/spb/poster/8a/8a0ed139c7751a67fe424bd9485252e7.jpg'

async def scheduled(wait_for):
	while True:
		'''
		await asyncio.sleep(wait_for)
		photo ='https://cdn.kassir.ru/spb/poster/8a/8a0ed139c7751a67fe424bd9485252e7.jpg'
		await bot.send_photo(435001186, photo, \
			caption= '<b>' + title_event + '</b>' +  '\n\n' + \
			constant.price + '1800'+'\n' + constant.metro + 'Просвещение'+'\n'+ constant.address +'Просвещение 23'+'\n' + \
			constant.link + '<a href="https://vk.com/id41732290">VK</a>', parse_mode="HTML")'''
		event = (191321, 'Детям', 'https://kudago.com/media/thumbs/640x384/images/event/cb/f8/cbf8e4ea908f15a154a84f9f854b90b4.jpg', 'Всероссийская историческая интеллектуальная онлайн-игра', '17 марта 2021', None, '', 0, None, None, 'https://kudago.com/online/event/detyam-vserossijskaya-istoricheskaya-intellektualnaya-onlajn-igra/')
		
		bc = BeautyCaption(event)
		caption = bc.get_caption()


		photos =['https://cdn.kassir.ru/spb/poster/8a/8a0ed139c7751a67fe424bd9485252e7.jpg', \
			    'https://kudago.com/media/thumbs/640x384/images/event/cb/f8/cbf8e4ea908f15a154a84f9f854b90b4.jpg']
		
		
		for photo in photos:

			photo_info = dict(await bot.send_photo(435001186, photo))
			photo_size_width = photo_info['photo'][0]['width']
			photo_size_height = photo_info['photo'][0]['height']
			if photo_size_height >= photo_size_width:
				await bot.send_message(435001186, f"{fmt.hide_link(photo)}"+ caption, parse_mode=types.ParseMode.HTML)
			else:
				file_id = photo_info['photo'][0]['file_id']
				await bot.send_photo(435001186, file_id, caption = caption, parse_mode=types.ParseMode.HTML)


'''
		await bot.send_message(435001186, \
			f"{fmt.hide_link(photo)}"+"gg",
        	parse_mode=types.ParseMode.HTML)
			'''
	


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(scheduled(1))
	executor.start_polling(dp, skip_updates=True)