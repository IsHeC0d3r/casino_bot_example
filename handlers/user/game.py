from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio.session import AsyncSession

from misc.game import insert_winner

from asyncio import sleep

async def game(msg: Message, bot: Bot, db: AsyncSession, state: FSMContext) -> None:
    await state.clear()

    bot_dice = await bot.send_dice(
        chat_id=msg.chat.id,
        emoji=msg.dice.emoji
    )
    await sleep(5)
    if msg.dice.value > bot_dice.dice.value:
        await msg.answer(
            text=f'🥳 <b>Поздравляю, ты выиграл!</b>\n'
            f'💰 Сумма выигрыша состявила <b>85</b>₽\n'
            f'🔢 Количество очков у тебя - <b>{msg.dice.value}</b>\n'
            f'🔢 Количество очков у бота - <b>{bot_dice.dice.value}</b>\n\n'
            '💁 <i>Подсказка: деньги были зачислены на баланс.</i>'
        )
        await insert_winner(db=db, id=msg.from_user.id, winner=msg.from_user.id)
    elif msg.dice.value < bot_dice.dice.value:
        await msg.answer(
            text=f'😔 К сожалению, ты проиграл.\n'
            f'💰 Сумма проигрыша состявила <b>100</b>₽\n'
            f'🔢 Количество очков у бота - <b>{bot_dice.dice.value}</b>\n'
            f'🔢 Количество очков у тебя - <b>{msg.dice.value}</b>\n\n'
            '💁 <i>Подсказка: деньги были списаны с баланса.</i>'
        )
        await insert_winner(db=db, id=msg.from_user.id, winner=0)
    else:
        await msg.answer(
            text=f'😮 Ничья!\n'
            f'🔢 Количество очков у тебя - <b>{msg.dice.value}</b>\n'
            f'🔢 Количество очков у бота - <b>{bot_dice.dice.value}</b>\n\n'
            '💁 <i>Подсказка: ты ничего не заработал, но и не потерял.</i>'
        )
        await insert_winner(db=db, id=msg.from_user.id, winner=2)