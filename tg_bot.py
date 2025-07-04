from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from sqlalchemy.future import select

from project_models import Users_in_telegram, async_session



BOT_TOKEN = "7786410391:AAGen2ygv6dHZW-bhCJww0j7bHbHJ6NDXY0"
bot = Bot(token=BOT_TOKEN)
router = Router()
dp = Dispatcher()

async def send_msg(user_site_id, message):
    async with async_session() as session:
        user_tg_info = await session.execute(select(Users_in_telegram).filter_by(user_in_site=user_site_id))
        user_tg_info = user_tg_info.scalars().one_or_none()
        if user_tg_info.user_tg_id:
            await bot.send_message(chat_id=user_tg_info.user_tg_id, text=message)


@router.message(Command('start'))
async def get_chat_id(message: types.Message):
    await message.answer(f"Вітаємо! Для отримки сповіщень з приводу зміни статусу ваших заявок напишіть код який Ви отримати на сайті")

@router.message()
async def get_chat_id(message: types.Message):
    user_code = message.text.strip()
    user_tg_id = message.chat.id
    async with async_session() as session:
        user_check = await session.execute( select(Users_in_telegram).filter_by(tg_code = user_code))
        user_check = user_check.scalars().one_or_none()
        if user_check:
            user_check.user_tg_id = user_tg_id
            session.add(user_check)
            await session.commit()
            await message.answer("Дякуємо! Будемо тримати Вас в курсі усіх подій!)")
        else:
            await message.answer("Щось пішло не так.\nПереконайтеся що код написано вірно, або спробуйте утворити новий  на сайті {{ПОСИЛАННЯ}}")

async def start():
    dp.include_router(router)
    await dp.start_polling(bot)


