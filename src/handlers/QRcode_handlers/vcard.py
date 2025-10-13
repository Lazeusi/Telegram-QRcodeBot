from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import BufferedInputFile
from io import BytesIO
import qrcode

from src.logger import get_logger
from src.keyboards.inline.start import main_menu_keyboard
from src.keyboards.inline.qrcode import cancel_keyboard

log = get_logger()
router = Router()

class QRVCardState(StatesGroup):
    waiting_for_name = State()
    waiting_for_number = State()
    waiting_for_email = State()

# --------------------- Callback Handler ---------------------
@router.callback_query(F.data == "qr_vcard")
async def qr_vcard_handler(call: types.CallbackQuery, state: FSMContext , bot: Bot):
    try:
        msg = await call.message.edit_text("Please enter the name:", reply_markup=await cancel_keyboard())
        await state.set_state(QRVCardState.waiting_for_name)
        await state.update_data(prompt_message_id=msg.message_id)
        await call.answer()
    except Exception as e:
        log.error(f"Error in qr_vcard_handler: {e}")
        await call.answer("Something went wrong.")

# --------------------- Name ---------------------
@router.message(QRVCardState.waiting_for_name)
async def process_qr_vcard_name(message: types.Message, state: FSMContext , bot: Bot):
    try:
        data = await state.get_data()
        prompt_message_id = data.get("prompt_message_id")
        if prompt_message_id:
            await bot.delete_message(chat_id=message.chat.id, message_id=prompt_message_id)

        await state.update_data(name=message.text)
        msg = await message.answer("Please enter the phone number:")
        await state.update_data(prompt_message_id=msg.message_id)
        await state.set_state(QRVCardState.waiting_for_number)
    except Exception as e:
        log.error(f"Error in process_qr_vcard_name: {e}")
        await message.answer("Something went wrong.")

# --------------------- Number ---------------------
@router.message(QRVCardState.waiting_for_number)
async def process_qr_vcard_number(message: types.Message, state: FSMContext , bot: Bot):
    try:
        data = await state.get_data()
        prompt_message_id = data.get("prompt_message_id")
        if prompt_message_id:
            await bot.delete_message(chat_id=message.chat.id, message_id=prompt_message_id)

        await state.update_data(number=message.text)
        msg = await message.answer("Please enter the email (or type 'skip'):")
        await state.update_data(prompt_message_id=msg.message_id)
        await state.set_state(QRVCardState.waiting_for_email)
    except Exception as e:
        log.error(f"Error in process_qr_vcard_number: {e}")
        await message.answer("Something went wrong.")

# --------------------- Email ---------------------
@router.message(QRVCardState.waiting_for_email)
async def process_qr_vcard_email(message: types.Message, state: FSMContext , bot: Bot):
    try:
        data = await state.get_data()
        prompt_message_id = data.get("prompt_message_id")
        if prompt_message_id:
            await bot.delete_message(chat_id=message.chat.id, message_id=prompt_message_id)

        email = message.text.strip()
        if email.lower() == "skip":
            email = ""

        data = await state.get_data()
        name = data.get("name")
        number = data.get("number")

        vcard = f"""BEGIN:VCARD
VERSION:3.0
N:{name}
TEL:{number}
EMAIL:{email}
END:VCARD"""

        qr = qrcode.make(vcard)
        buf = BytesIO()
        qr.save(buf, "PNG")
        buf.seek(0)
        input_file = BufferedInputFile(file=buf.getvalue(), filename="qrcode.png")

        await message.answer_photo(photo=input_file, caption="✅ Here is your QR code!")
        await state.clear()
    except Exception as e:
        log.error(f"Error in process_qr_vcard_email: {e}")
        await message.answer("Something went wrong.")

# --------------------- Cancel ---------------------
@router.callback_query(F.data == "cancel_qr")
async def cancel_callback(call: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        prompt_message_id = data.get("prompt_message_id")
        if prompt_message_id:
            await call.message.delete()
        await state.clear()
        await call.answer("Cancelled ✅")
    except Exception as e:
        log.error(f"Error in cancel_callback: {e}")
        await call.answer("Something went wrong.")
