from aiogram import Router, types, F , Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from io import BytesIO
import qrcode

from src.logger import get_logger
from src.keyboards.inline.start import main_menu_keyboard
from src.keyboards.inline.qrcode import payment_types_keyboard , cancel_keyboard

router = Router()
log = get_logger()


class PaymentQR(StatesGroup):
    waiting_for_payment_type = State()
    waiting_for_bank_info = State()
    waiting_for_crypto_info = State()
    waiting_for_link_info = State()


@router.callback_query(F.data == "qr_payment")
async def choose_payment_type(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Select the type of payment you want to create a QR for:",
        reply_markup=await payment_types_keyboard()
    )
    await state.update_data(last_bot_message_id=callback.message.message_id)
    await state.set_state(PaymentQR.waiting_for_payment_type)
    
@router.callback_query(F.data == "back")
async def cancel_qr_handler(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text("Sure! \n You back to main menu " , reply_markup=await main_menu_keyboard())
        await state.clear()
    except Exception as e:
        log.error(f"Error in cancel gernate QRCode: {e}")
        
@router.callback_query(F.data == "pay_crypto")
async def get_crypto_address(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Enter your crypto address or URI (e.g., `bitcoin:address?amount=0.01`):" , reply_markup= await cancel_keyboard())
    await state.set_state(PaymentQR.waiting_for_crypto_info)    


@router.message(PaymentQR.waiting_for_crypto_info)
async def process_crypto_payment(message: types.Message, state: FSMContext , bot : Bot):

    try:
        data = await state.get_data()
        await bot.delete_message(message.chat.id, data.get("last_bot_message_id"))
        qr_data = message.text.strip()

        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, "PNG")
        buffer.seek(0)

        await message.answer_photo(
            photo=types.BufferedInputFile(buffer.read(), filename="crypto_qr.png"),
            caption="Your crypto QR Code is ready 🪙"
        )

        await state.clear()
    except Exception as e:
        await message.answer(f"Error generating QR: {e}")

@router.callback_query(F.data == "pay_link")
async def get_payment_link(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Send your payment link (for example, https://zarinp.al/example):" ,reply_markup= await cancel_keyboard())
    await state.update_data(last_bot_message_id=callback.message.message_id)
    await state.set_state(PaymentQR.waiting_for_link_info)
    
@router.message(PaymentQR.waiting_for_link_info)
async def process_payment_link(message: types.Message, state: FSMContext , bot : Bot):
    try:
        data = await state.get_data()
        await bot.delete_message(message.chat.id, data.get("last_bot_message_id"))
        qr_data = message.text.strip()

        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, "PNG")
        buffer.seek(0)

        await message.answer_photo(
            photo=types.BufferedInputFile(buffer.read(), filename="payment_link_qr.png"),
            caption="Your payment link QR Code is ready 🔗"
        )

       
        await state.clear()
    except Exception as e:
        await message.answer(f"Error generating QR: {e}")

    
@router.callback_query(F.data == "pay_bank")
async def get_bank_payment(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Please enter your card number or payment info:" ,reply_markup= await cancel_keyboard())
    await state.set_state(PaymentQR.waiting_for_bank_info)
    await state.update_data(last_bot_message_id=callback.message.message_id)


@router.message(PaymentQR.waiting_for_bank_info)
async def process_bank_payment(message: types.Message, state: FSMContext , bot : Bot):
    try:
        data = await state.get_data()
        await bot.delete_message(message.chat.id, data.get("last_bot_message_id"))
        qr_data = message.text.strip()

        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, "PNG")
        buffer.seek(0)

        await message.answer_photo(
            photo=types.BufferedInputFile(buffer.read(), filename="bank_payment_qr.png"),
            caption="Here is your payment QR Code 💳"
        )

        await state.clear()
    except Exception as e:
        await message.answer(f"Error generating QR: {e}")


