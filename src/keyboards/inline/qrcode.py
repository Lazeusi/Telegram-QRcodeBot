from aiogram.utils.keyboard import InlineKeyboardBuilder



async def cancel_keyboard():

    builder = InlineKeyboardBuilder()
    builder.button(text="Cancel" , callback_data="cancel_qr")

    cancel = builder.as_markup()
    return cancel