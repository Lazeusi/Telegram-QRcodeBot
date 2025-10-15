from aiogram.filters import CommandStart 
from aiogram import Router, F , types

from src.logger import get_logger
from src.keyboards.inline.start import main_menu_keyboard

log = get_logger()

router = Router()

@router.message(CommandStart() , F.chat.type == "private")
async def start_handler(msg: types.Message):
    try:
        
        await msg.answer(f"📲 Select the type of QR Code you want to generate.\n You can create one from text, a link, contact info, Wi-Fi data, or even payments." ,
                         reply_markup= await main_menu_keyboard()       
                            )
    except Exception as e:
        log.error(f"We got an error: {e}")

