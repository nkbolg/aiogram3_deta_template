from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=["start"]))
async def start_handler(message: types.Message):
    msg_id = message.message_id
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    await message.answer(f"Hello, {full_name}!\n"
                         f"Your id is {user_id}\n"
                         f"Message id is {msg_id}")
