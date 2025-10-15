from aiogram import Router, types, F , Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from io import BytesIO
import qrcode

from src.logger import get_logger
from src.keyboards.inline.qrcode import cancel_keyboard

log = get_logger()
router = Router()


class LocationQR(StatesGroup):
    waiting_for_latitude = State()
    waiting_for_longitude = State()


@router.callback_query(F.data == "qr_location")
async def ask_latitude(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "📍 Please enter the **latitude** (e.g., `35.6892`):" ,
        reply_markup=await cancel_keyboard()
    )
    await state.update_data(last_bot_message_id=callback.message.message_id)
    await state.set_state(LocationQR.waiting_for_latitude)

@router.message(LocationQR.waiting_for_latitude)
async def get_latitude(message: types.Message, state: FSMContext , bot : Bot):

    try:
        data = await state.get_data()
        await bot.delete_message(message.chat.id, data.get("last_bot_message_id"))
        lat = float(message.text.strip())
        await state.update_data(latitude=lat)
        await message.answer("Now send the **longitude** (e.g., `51.3890`):" , reply_markup=await cancel_keyboard())
        await state.set_state(LocationQR.waiting_for_longitude)
        await state.update_data(last_bot_message_id=message.message_id)

    except ValueError:
        await message.answer("❌ Invalid latitude. Please enter a number like `35.6892`.")
        
@router.message(LocationQR.waiting_for_longitude)
async def get_longitude_and_generate_qr(message: types.Message, state: FSMContext , bot : Bot):

    try:
        data = await state.get_data()
        await bot.delete_message(message.chat.id, data.get("last_bot_message_id"))
        lon = float(message.text.strip())
        data = await state.get_data()
        lat = data.get("latitude")

        qr_data = f"geo:{lat},{lon}"
        qr = qrcode.make(qr_data)

        buffer = BytesIO()
        qr.save(buffer, "PNG")
        buffer.seek(0)

        await message.answer_photo(
            photo=types.BufferedInputFile(buffer.read(), filename="location_qr.png"),
            caption=f"📍 Location QR Code created!\nLatitude: `{lat}`\nLongitude: `{lon}`"
        )

        await state.clear()

    except ValueError:
        await message.answer("❌ Invalid longitude. Please enter a valid number like `51.3890`.")

