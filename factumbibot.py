from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging

API_TOKEN = '7633080886:AAG5KX0GQi1fUz4es2mO13HZ2NRZSJJmT0k'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# --- FSM для сбора заявки ---
class Form(StatesGroup):
    name = State()
    company = State()
    contact = State()
    interest = State()

# --- Главное меню ---
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add("\U0001F4CA BI-продукты", "\U0001F4C2 Примеры дашбордов")
main_kb.add("\U0001F50D Заказать аудит", "\U0001F4EC Оставить заявку")
main_kb.add("\u2753 Частые вопросы", "\U0001F4AC Связаться")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Я — бот FACTUM BI.\n\nПомогаю бизнесу превращать данные в понятные дашборды и управленческие решения.\n\nЧто вас интересует?",
        reply_markup=main_kb
    )

@dp.message_handler(lambda message: message.text == "\U0001F4CA BI-продукты")
async def show_products(message: types.Message):
    await message.answer(
        "У нас 6 BI-продуктов:\n\n"
        "🔧 Операционный дашборд\n"
        "📊 Аналитический дашборд\n"
        "🧭 Стратегический дашборд\n"
        "🧱 Улучшение встроенных отчётов\n"
        "🧰 BI с нуля\n"
        "🔎 Аудит текущей системы"
    )

@dp.message_handler(lambda message: message.text == "\U0001F4C2 Примеры дашбордов")
async def show_examples(message: types.Message):
    await message.answer("Примеры дашбордов: [ссылка на портфолио или PDF]")

@dp.message_handler(lambda message: message.text == "\U0001F50D Заказать аудит")
async def audit_start(message: types.Message):
    await Form.name.set()
    await message.answer("Как вас зовут?")

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await Form.next()
    await message.answer("Название компании (если есть)?")

@dp.message_handler(state=Form.company)
async def process_company(message: types.Message, state: FSMContext):
    await state.update_data(company=message.text)
    await Form.next()
    await message.answer("Как с вами связаться? (телефон или почта)")

@dp.message_handler(state=Form.contact)
async def process_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await Form.next()
    await message.answer("Что вас интересует?")

@dp.message_handler(state=Form.interest)
async def process_interest(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msg = (
        f"\U0001F4DD Новая заявка на аудит:\n"
        f"Имя: {data['name']}\n"
        f"Компания: {data['company']}\n"
        f"Контакт: {data['contact']}\n"
        f"Интересует: {message.text}"
    )
    await message.answer("Спасибо! Мы свяжемся с вами в ближайшее время.")
    await bot.send_message(chat_id=message.chat.id, text=msg)
    await state.finish()

@dp.message_handler(lambda message: message.text == "\U0001F4EC Оставить заявку")
async def leave_request(message: types.Message):
    await audit_start(message)

@dp.message_handler(lambda message: message.text == "\u2753 Частые вопросы")
async def faq(message: types.Message):
    await message.answer("\u2022 Сколько стоит? — от 30 тыс. рублей.\n\u2022 Сроки? — от 3–5 рабочих дней.\n\u2022 Форматы? — Power BI, Looker Studio, др.\n\u2022 Как передаёте данные? — через API, безопасно.")

@dp.message_handler(lambda message: message.text == "\U0001F4AC Связаться")
async def contact(message: types.Message):
    await message.answer("Пишите: @твой_ник или нажмите 👉 t.me/твой_ник")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)