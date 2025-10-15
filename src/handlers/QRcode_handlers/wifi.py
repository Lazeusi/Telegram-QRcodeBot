from aiogram import Router, F, types , Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile
from io import BytesIO
import qrcode
from src.logger import get_logger


log = get_logger()
router = Router()


class QRWiFiState(StatesGroup):
    waiting_for_ssid = State()
    waiting_for_password = State()
    waiting_for_encryption = State()


@router.callback_query(F.data == "qr_wifi")
async def wifi_qr_start(call: types.CallbackQuery, state: FSMContext):
    sent = await call.message.edit_text("📶 Please enter your Wi-Fi network name (SSID):")
    await call.answer()
    await state.update_data(last_bot_message_id=sent.message_id)
    await state.set_state(QRWiFiState.waiting_for_ssid)


@router.message(QRWiFiState.waiting_for_ssid)
async def wifi_get_ssid(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()

    try:
        await bot.delete_message(message.chat.id, data.get("last_bot_message_id"))
    except Exception:
        pass

    ssid = message.text.strip()
    sent = await message.answer("🔑 Please enter your Wi-Fi password (or type `none` if open network):")

    await state.update_data(ssid=ssid, last_bot_message_id=sent.message_id)
    await state.set_state(QRWiFiState.waiting_for_password)


@router.message(QRWiFiState.waiting_for_password)
async def wifi_get_password(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    try:
        await bot.delete_message(message.chat.id, data.get("last_bot_message_id"))
    except Exception:
        pass

    password = message.text.strip()
    sent = await message.answer(
        "⚙️ Choose your encryption type:\n\n"
        "`WPA` - Most common\n"
        "`WEP` - Old\n"
        "`nopass` - Open network"
    )

    await state.update_data(password=password, last_bot_message_id=sent.message_id)
    await state.set_state(QRWiFiState.waiting_for_encryption)


@router.message(QRWiFiState.waiting_for_encryption)
async def wifi_generate_qr(message: types.Message, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()


        try:
            await bot.delete_message(message.chat.id, data.get("last_bot_message_id"))
        except Exception:
            pass

        ssid = data.get("ssid")
        password = data.get("password")
        encryption = message.text.strip().upper()

        if encryption not in ["WPA", "WEP", "NOPASS"]:
            sent = await message.answer("❌ Invalid encryption type. Please type WPA, WEP, or nopass.")
            await state.update_data(last_bot_message_id=sent.message_id)
            return

        qr_text = f"WIFI:T:{encryption};S:{ssid};P:{'' if password.lower() == 'none' else password};;"

        qr = qrcode.make(qr_text)
        image_stream = BytesIO()
        qr.save(image_stream, "PNG")
        image_stream.seek(0)

        input_file = BufferedInputFile(
            file=image_stream.getvalue(),
            filename="wifi_qrcode.png"
        )

        await message.answer_photo(
            photo=input_file,
            caption=f"✅ Wi-Fi QR code generated!\n\n📶 SSID: `{ssid}`",

        )

        await state.clear()

    except Exception as e:
        log.error(f"Error generating Wi-Fi QR code: {e}")
        await message.answer("❌ Failed to generate Wi-Fi QR code. Try again.")
