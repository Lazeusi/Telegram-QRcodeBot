from aiogram.utils.keyboard import InlineKeyboardBuilder



async def main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Plain Text", callback_data="qr_text")
    builder.button(text="🔗 Link / URL", callback_data="qr_url")
    builder.button(text="📞 Contact Info", callback_data="qr_vcard")
    builder.button(text="📶 Wi-Fi", callback_data="qr_wifi")
    builder.button(text="💰 Payment", callback_data="qr_payment")
    builder.button(text="📍 Location", callback_data="qr_location")
    builder.button(text="⚙️ JSON / Data", callback_data="qr_json")
    builder.adjust(2)

    qr_keyboard = builder.as_markup()

    return qr_keyboard



