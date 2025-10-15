from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def cancel_keyboard():

    builder = InlineKeyboardBuilder()
    builder.button(text="Cancel" , callback_data="cancel_qr")

    cancel = builder.as_markup()
    return cancel


async def payment_types_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪙 Crypto Payment", callback_data="pay_crypto") , InlineKeyboardButton(text="🔗 Custom Link", callback_data="pay_link")],
        [InlineKeyboardButton(text="💳 Bank / Card Payment", callback_data="pay_bank")],
        [InlineKeyboardButton(text="↩️ Back", callback_data="back")]
    ])
    return keyboard
        

