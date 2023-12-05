from aiogram.types import Message
from keyboards.inline import kb_choose_game

async def play(msg: Message) -> None:
    await msg.answer(
        text='Выбери игру и нажми на кнопку ниже!',
        reply_markup=kb_choose_game
    )