import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from generate import generate_document

TOKEN = "8757393669:AAGIlXLrHM2Hh5Sf6r3W_LGxkrFlZlZzqyA"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📄 Создание документа")]
    ],
    resize_keyboard=True
)

doc_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📄 Шаблон 1")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)

class DocForm(StatesGroup):
    day = State()
    month = State()
    year = State()
    number = State()
    subject = State()
    text = State()
    position = State()
    rank = State()
    name = State()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Выбери раздел", reply_markup=main_menu)

@dp.message(F.text == "📄 Создание документа")
async def create_doc_handler(message: Message):
    await message.answer("Выбери шаблон", reply_markup=doc_menu)

@dp.message(F.text == "📄 Шаблон 1")
async def template_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(DocForm.day)
    await message.answer("Введите число:")

@dp.message(DocForm.day)
async def get_day(message: Message, state: FSMContext):
    await state.update_data(day=message.text)
    await state.set_state(DocForm.month)
    await message.answer("Введите месяц:")

@dp.message(DocForm.month)
async def get_month(message: Message, state: FSMContext):
    await state.update_data(month=message.text)
    await state.set_state(DocForm.year)
    await message.answer("Введите год:")

@dp.message(DocForm.year)
async def get_year(message: Message, state: FSMContext):
    await state.update_data(year=message.text)
    await state.set_state(DocForm.number)
    await message.answer("Введите номер:")

@dp.message(DocForm.number)
async def get_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await state.set_state(DocForm.subject)
    await message.answer("Введите тему/название:")

@dp.message(DocForm.subject)
async def get_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(DocForm.text)
    await message.answer("Введите основной текст:")

@dp.message(DocForm.text)
async def get_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(DocForm.position)
    await message.answer("Введите должность:")

@dp.message(DocForm.position)
async def get_position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    await state.set_state(DocForm.rank)
    await message.answer("Введите звание:")

@dp.message(DocForm.rank)
async def get_rank(message: Message, state: FSMContext):
    await state.update_data(rank=message.text)
    await state.set_state(DocForm.name)
    await message.answer("Введите ФИО:")

@dp.message(DocForm.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()

    result_path = generate_document(data)

    photo = FSInputFile(result_path)
    await message.answer_photo(photo, caption="Готово")
    await state.clear()

@dp.message(F.text == "🔙 Назад")
async def back_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню", reply_markup=main_menu)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())