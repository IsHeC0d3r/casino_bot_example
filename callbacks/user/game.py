from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from misc.misc import get_admin_link

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, delete, update
from database.models.User import User
from database.models.Stats import Stats

from states.GameState import GameState

from misc.game import insert_winner

from keyboards.builder import simple_keyboard_builder, Mode

import GameLogic

async def game(callback: CallbackQuery, bot: Bot, db: AsyncSession, state: FSMContext) -> None:
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    await state.clear()
    game = '_'.join(callback.data.split('_')[1:-1])
    key = callback.data.split('_')[-1]
    match game:
        case 'numbers':
            out = GameLogic.numbers(key)
            if out[1]:
                await bot.send_message(
                    chat_id=callback.from_user.id,
                    text=f'🥳 <b>Поздравляю, ты выиграл!</b>\n'
                    f'💰 Сумма выигрыша состявила <b>85</b>₽\n'
                    f'🔢 Выпавшее число - <b>{out[0]}</b>\n\n'
                    '💁 <i>Подсказка: деньги были зачислены на баланс.</i>'
                )
                await insert_winner(db=db, id=callback.from_user.id, winner=callback.from_user.id)
            else:
                await bot.send_message(
                    chat_id=callback.from_user.id,
                    text=f'😔 К сожалению, ты проиграл.\n'
                    f'💰 Сумма проигрыша состявила <b>100</b>₽\n'
                    f'🔢 Выпавшее число - <b>{out[0]}</b>\n\n'
                    '💁 <i>Подсказка: деньги были списаны с баланса.</i>'
                )
                await insert_winner(db=db, id=callback.from_user.id, winner=callback.from_user.id)
        case 'heads_and_tails':
            out = GameLogic.heads_and_tails(key)
            if out:
                await bot.send_message(
                    chat_id=callback.from_user.id,
                    text=f'🥳 <b>Поздравляю, ты выиграл!</b>\n'
                    f'💰 Сумма выигрыша состявила <b>85</b>₽\n\n'
                    '💁 <i>Подсказка: деньги были зачислены на баланс.</i>'
                )
                await insert_winner(db=db, id=callback.from_user.id, winner=callback.from_user.id)
            else:
                await bot.send_message(
                    chat_id=callback.from_user.id,
                    text=f'😔 К сожалению, ты проиграл.\n'
                    f'💰 Сумма проигрыша состявила <b>100</b>₽\n\n'
                    '💁 <i>Подсказка: деньги были списаны с баланса.</i>'
                )
                await insert_winner(db=db, id=callback.from_user.id, winner=callback.from_user.id)
        case _:
            await db.execute(delete(Stats).where(
                    (Stats.participant_1 == callback.from_user.id) |
                    (Stats.participant_2 == callback.from_user.id) &
                    (Stats.winner == -1)
                )
            )
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=f'Произошла ошибка! Пожалуйста, обратитесь к {get_admin_link("администратору")} со следующим текстом -\n\n'
                f'<code>[CALLBACK] game data invalid! {callback.data}</code>'
            )