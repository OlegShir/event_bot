import logging
import asyncio
from datetime import datetime

from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram import Bot, Dispatcher, executor, types
import constant
# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=constant.API_TOKEN)
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

async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)
		photo ='https://st.biglion.ru/cfs13/deal_offer/cd/2f/cd2fa1c4d6296e18de7c174158076beb.jpg'
		await bot.send_photo(435001186, photo, \
			caption= '<b>' + title_event + '</b><' +  '\n\n' + \
			constant.price + '1800'+'\n' + constant.metro + 'Просвещение'+'\n'+ constant.address +'Просвещение 23'+'\n' + \
			constant.link + '<a href="https://vk.com/id41732290">VK</a>', parse_mode="HTML")

		


		
		


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(scheduled(1))
	executor.start_polling(dp, skip_updates=True)