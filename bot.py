import logging, asyncio, json
from typing import Text
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as fmt

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# внутренние модули 
import constant
from sqlighter import SQLighter
from parserevent import ParserEvent
from beauty_caption import BeautyCaption

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# создаем ячейку памяти для машины состояний
#storage = MemoryStorage()

# инициализируем соединение с БД
db = SQLighter('event_parse.db')
parse = ParserEvent()

# инициализируем бота
bot = Bot(token=constant.API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# создаем класс состояний для общения с пользователем
class Form(StatesGroup):
    feedback_want = State()  # в памяте как 'Form:feedback_want'

# команда подписки - start
@dp.message_handler(commands=['start'])
async def subscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id, message.from_user.first_name)
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

# команда отзыва - /feedback
@dp.message_handler(commands=['feedback'])
async def ready_get_feedback(message: types.Message):
	await Form.feedback_want.set()
	await bot.send_message(message.chat.id, 'Отправьте отзыв')

# декоратор состояния ожидания отзыва
@dp.message_handler(state=Form.feedback_want)
async def get_feedback(message: types.Message, state: FSMContext):
	
	await bot.send_message(constant.ADMIN, f'{message.text}\n||{message.from_user}')
	
	await state.finish()

	await message.answer('Ваш отзыв отправлен')
	

# команда получения количества подписчиков - subscr
@dp.message_handler(commands=['subscr'])
async def get_subscr(message: types.Message):
	# если юзер является админом
	if message.from_user.id == constant.ADMIN:
		count = len(db.get_subscriptions())
		await message.answer(f'Количество активных подписчиков: {count}')

@dp.message_handler()
async def all_message(message: types.Message):
	if message.reply_to_message and message['from'].id == constant.ADMIN:
		user_data_json= message.reply_to_message.text.split('||')[1]
		user_data = json.loads(user_data_json)
		user_id = int(user_data['id'])
		user_name = user_data.get('first_name', '')
		await bot.send_message(user_id, f'{user_name}, спасибо за отзыв.\n{message.text}')
	# filter print(message.text)
	else:
		name_user = message.from_user.first_name
		await message.answer(f'{name_user}, я пока еще не умею разговаривать,\nтолько выполняю команды')

async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)
		# получаем список событий
		new_events = parse.main_parse()
		# если мероприятия есть  	
		if (new_events):
			print(f'Всего найдено {len(new_events)} новых событий. Производится рассылка ...')
			# для каждого мероприятия
			for event in new_events:
				try:
					# в будущем здесь реализуется фильтр по типу мероприятия -> тип события
					subscriptions = db.get_subscriptions()
					# получаем ссылку на фотографию события
					photo_url = event[2]
					# загружаем фотографию события на сервер Телеграмма
					photo_info = dict(await bot.send_photo(constant.ADMIN, photo_url))
					# получаем id фото на сервере Телеграмма -> ссылка
					file_id = photo_info['photo'][0]['file_id']
					photo_size_width = photo_info['photo'][0]['width']
					photo_size_height = photo_info['photo'][0]['height']
					# форматирование сообщения
					beauty = BeautyCaption(event)
					caption_event = beauty.get_caption()
					if photo_size_height >= photo_size_width:
						for user in subscriptions:
							await bot.send_message(user[1], f"{fmt.hide_link(photo_url)}{caption_event}", parse_mode=types.ParseMode.HTML)
					else:
						for user in subscriptions:
							await bot.send_photo(user[1], file_id, caption = f"{caption_event}", parse_mode=types.ParseMode.HTML)
				except Exception as error: 
					print(f'При рассылке возникла ошибка:\n{error.__class__.__name__}: {error}\nСобытие содержало:\n{event}\nОписание:\n{caption_event}\n')
					continue
					
			print(f'\nСобытия разосланы {len(subscriptions)} пользователям')
		else:
			print(f'\nНовых событий не найдено')
 

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(scheduled(5))


	executor.start_polling(dp, skip_updates=True)
	
