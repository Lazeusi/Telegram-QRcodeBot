from aiogram import Router, types, F , Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from io import BytesIO
import qrcode
import json

from src.keyboards.inline.qrcode import cancel_keyboard

router = Router()


class JSONQR(StatesGroup):
    waiting_for_json = State()


@router.callback_query(F.data == "qr_json")
async def ask_for_json(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "⚙️ Please send your JSON data.\n\n"
        "Example:\n```json\n{\n  \"name\": \"Shayan\",\n  \"age\": 19\n}\n```",
        parse_mode="Markdown" ,
        reply_markup= await cancel_keyboard()
    )
    await state.update_data(last_bot_message_id=callback.message.message_id)
    await state.set_state(JSONQR.waiting_for_json)

@router.message(JSONQR.waiting_for_json)
async def process_json_data(message: types.Message, state: FSMContext , bot : Bot):

    try:
        data = await state.get_data()
        await bot.delete_message(message.chat.id, data.get("last_bot_message_id"))
        text = message.text.strip()
        parsed_json = json.loads(text)  # validate JSON

        qr_data = json.dumps(parsed_json, ensure_ascii=False, indent=2)
        qr = qrcode.make(qr_data)

        buffer = BytesIO()
        qr.save(buffer, "PNG")
        buffer.seek(0)

        await message.answer_photo(
            photo=types.BufferedInputFile(buffer.read(), filename="json_qr.png"),
            caption="✅ JSON QR Code created successfully!"
        )

        await state.clear()

    except json.JSONDecodeError:
        await message.answer("❌ Invalid JSON format. Please check your syntax and try again.")
