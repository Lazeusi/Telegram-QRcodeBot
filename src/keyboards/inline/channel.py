from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.logger import get_logger
from src.database.models.admins import Admin
from src.database.models.channels import Channel

log = get_logger()

async def channel_keyboard():
    try:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Add channel", callback_data="add_channel") , InlineKeyboardButton(text="Remove channel", callback_data="remove_channel")],
                [InlineKeyboardButton(text="Channel list", callback_data="channel_list")],
                [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_admin_panel")]
            ]
        )
    except Exception as e:
        log.error(f"We got an error: {e}")
        
async def back_to_force_join_panel_keyboard():
    try:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back", callback_data="force_join")],
            ]
        )
    except Exception as e:
        log.error(f"We got an error: {e}")
        
async def confirm_add_force_channel_keyboard():
    
    try:
        return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="✅ Confirm", callback_data="confirm_add"),
                        InlineKeyboardButton(text="❌ Cancel", callback_data="back_to_admin_panel")
                    ]
                ]
            )
    except Exception as e:
        log.error(f"We got an error: {e}")
async def ch_remove_keyboard():
    try:
        builder = InlineKeyboardBuilder()
        channels = await Channel.get_all()
        
        if not channels:
            builder.button(text="❌ No channels found", callback_data="none")
            builder.button(text="🔙 Back" , callback_data="back_to_admin_panel")
            return builder.as_markup()
        
        for channel in channels:
            builder.button(
                text=f"{channel['title']}",
                callback_data=f"remove_channel_{channel['channel_id']}"
            )
        builder.button(text="🔙 Back" , callback_data="force_join")
        builder.adjust(1)
        return builder.as_markup()
    except Exception as e:
        log.error(f"We got an error: {e}")
        
async def accept_remove_channel_keyboard():
    try:
        
        return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="✅ Confirm", callback_data="confirm_remove"),
                        InlineKeyboardButton(text="❌ Cancel", callback_data="back_to_admin_panel")
                    ]
                ]
            )
    except Exception as e:
        log.error(f"We got an error: {e}")
        