from aiogram.filters import CommandStart 
from aiogram import Router, F , types

# from src.keyboards.inline import start_keyboard
from src.logger import get_logger

log = get_logger()
router = Router()

@router.message(CommandStart())
async def start_handler(msg: types.Message):
    try:
        await msg.answer(f"Hi {msg.from_user.first_name} What I can do for you?", 
                         reply_markup=types.ReplyKeyboardRemove()
                         )
    except Exception as e:
        log.error(f"We got an error: {e}")
