import logging
import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token='1535163103:AAG-Xv6Wki6pT878EPe6xNapmWoQ8jeL5n8')
dp = Dispatcher(bot)


'''
# Команда активации подписки
@dp.message_handler(commands=['ss'])
async def subscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, True)
	
	await message.answer("Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")

# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber(message.from_user.id, False)
		await message.answer("Вы итак не подписаны.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, False)
		await message.answer("Вы успешно отписаны от рассылки.")
'''


@dp.message_handler()
async def echo(message: types.Message):
	with open('/1.jpg', 'rb') as photo:
		await message.reply_photo(photo, caption='Cats are here 😺')
				


# запускаем лонг поллинг
if __name__ == '__main__':
	
	executor.start_polling(dp, skip_updates=True)