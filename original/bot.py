import logging
import asyncio
import emoji
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram import Bot, Dispatcher, executor, types

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token='1535163103:AAG-Xv6Wki6pT878EPe6xNapmWoQ8jeL5n8')
dp = Dispatcher(bot)

# иницилизация картинок эмодзи в описании события 
price = emoji.emojize(":moneybag: ", use_aliases=True)
metro = emoji.emojize(":metro: м. ", use_aliases=True)
adress = emoji.emojize(":world_map: ", use_aliases=True)
raiting = emoji.emojize(":star: :", use_aliases=True)
link = emoji.emojize(":link: ", use_aliases=True)

link_event = 'https://speterburg.biglion.ru/deals/spa-programma-vibiray2-54/'
title_event = 'SPA-программа «Май», «Пляж», «Сила камня», «Восточная сказка», «Сладкие грезы», «Тайский шепот» в салоне Simmetria SPA'

@dp.message_handler()
async def echo(message: types.Message):
	print(message)
	with open('original/a.jpg', 'rb') as photo:
		await message.answer_photo(photo, caption=bold(title_event) + '\n\n' + \
			price + '1800'+'\n' + metro + 'Просвещение'+'\n'+ adress +'Просвещение 23'+'\n' + \
			link + link_event, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)