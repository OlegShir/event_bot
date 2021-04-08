import constant
import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as fmt

from sqlighter import SQLighter
from parserevent import ParserEvent
from beauty_caption import BeautyCaption
# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем соединение с БД
db = SQLighter('event_parse.db')
parse = ParserEvent()

# инициализируем бота
bot = Bot(token=constant.API_TOKEN)
dp = Dispatcher(bot)

# команда подписки - start
@dp.message_handler(commands=['start'])
async def subscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, True)
	
	await message.answer("Вы успешно подписались на рассылку!")

# команда отписки - stop
@dp.message_handler(commands=['stop'])
async def unsubscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если пользователя нет в базе, добавляем его с неактивной подпиской (запоминаем)
		# db.add_subscriber(message.from_user.id, False)
		await message.answer("Вы еще подписаны.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")

@dp.message_handler()
async def all_message(message: types.Message):
		
    await message.answer('Я пока еще не умею разговаривать,\nтолько выполняю команды')


async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)
		# получаем список событий
		new_events = parse.main_parse()
		print(len(new_events))
		# если мероприятия есть
		if (new_events):
			# для каждого мероприятия
			for event in new_events:
				print(len(event)) 
				# в будущем здесь реализуется фильтр по типу мероприятия -> тип события
				subscriptions = db.get_subscriptions()
				# получаем ссылку на фотографию события
				photo_url = event[2]
				# загружаем фотографию события на сервер Телеграмма
				photo_info = dict(await bot.send_photo(435001186, photo_url))
				# получаем id фото на сервере Телеграмма -> ссылка
				file_id = photo_info['photo'][0]['file_id']
				photo_size_width = photo_info['photo'][0]['width']
				photo_size_height = photo_info['photo'][0]['height']
				# форматирование сообщения
				beauty = BeautyCaption(event)
				caption_event = beauty.get_caption()
				if photo_size_height >= photo_size_width:
					for user in subscriptions:
						await bot.send_message(user[1], f"{fmt.hide_link(photo_url)}"+ caption_event, parse_mode=types.ParseMode.HTML)
				else:
					for user in subscriptions:
						await bot.send_photo(user[1], file_id, caption = caption_event, parse_mode=types.ParseMode.HTML)
 

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(scheduled(5))
	executor.start_polling(dp, skip_updates=True)
	