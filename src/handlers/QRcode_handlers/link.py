from aiogram import Router, types, F , Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile
import qrcode
from io import BytesIO

from src.logger import get_logger
from src.keyboards.inline.start import main_menu_keyboard 
from src.keyboards.inline.qrcode import cancel_keyboard

log = get_logger()
router = Router()


class QRLinkState(StatesGroup):
    waiting_for_link = State()
    
@router.callback_query(F.data == "qr_url")
async def qr_link_handler(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text(
            "✏️ Please send the link you want to convert into a QR code: \n Example: https://example.com",
            reply_markup=await cancel_keyboard()
        )
        await state.update_data(prompt_message_id=call.message.message_id)
        await state.set_state(QRLinkState.waiting_for_link)
        await call.answer()
    except Exception as e:
        log.error(f"Error in qr_link_handler: {e}")
        await call.answer("Something went wrong.")

@router.callback_query(F.data == "cancel_qr")
async def cancel_qr_handler(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text("Sure! \n You back to main menu " , reply_markup=await main_menu_keyboard())
        await state.clear()
    except Exception as e:
        log.error(f"Error in cancel gernate QRCode: {e}")
@router.message(QRLinkState.waiting_for_link)
async def process_qr_link(message: types.Message, state: FSMContext , bot: Bot):
    try:

        data = await state.get_data()
        prompt_message_id = data.get("prompt_message_id")
        await bot.delete_message(message.from_user.id, prompt_message_id)
        
        link = message.text.strip()
        qr = qrcode.make(link)
        image_stream = BytesIO()
        qr.save(image_stream, "PNG")
        image_stream.seek(0)
        input_file = BufferedInputFile(file=image_stream.getvalue(), filename="qrcode.png")
        await message.answer_photo(
            photo=input_file,
            caption="✅ Here is your QR code!",
        )
        await state.clear()
    except Exception as e:
        log.error(f"Error generating QR code: {e}")
        await message.answer("❌ Failed to generate QR code. Try again.")