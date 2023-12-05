from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from misc.misc import get_admin_link

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, delete
from database.models.User import User
from database.models.Stats import Stats

from states.GameState import GameState

from keyboards.builder import simple_keyboard_builder, Mode

from loader import msg_games

async def choose_game(callback: CallbackQuery, bot: Bot, db: AsyncSession, state: FSMContext) -> None:
    await bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id
    )
    balance = await db.scalar(select(User.balance).where(User.telegram == callback.from_user.id))
    if balance < 100:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text='😔 Сожалею, но на твоем балансе недостаточно средств!\n\n'
            f'💁 <i>Подсказка: пополнить баланс можно через {get_admin_link("администратора")}</i>'
        )
        
    is_playing_now = await db.scalars(select(Stats).where(
            (Stats.participant_1 == callback.from_user.id) |
            (Stats.participant_2 == callback.from_user.id) &
            (Stats.winner == -1)
        )
    )
    if len(is_playing_now.all()) > 0:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text='☝️ На данный момент вы уже находитесь в игре!\n\n'
            '💁 <i>Подсказка: дождитесь окончания игры и попробуйте снова.</i>'
        )
        # return
    db.add(
        Stats(
            participant_1 = callback.from_user.id,
            participant_2 = 0,
            game = callback.data,
            bet = 100
        )
    )
    hint = ''
    if callback.data in msg_games:
        match callback.data:
            case 'cube':
                hint = 'брось кубик ( нажми, чтобы скопировать - <code>🎲</code> )'
            case 'darts':
                hint = 'отправь мишень ( нажми, чтобы скопировать - <code>🎯</code> )'
            case 'basketball':
                hint = 'брось баскетбольный мячик ( нажми, чтобы скопировать - <code>🏀</code> )'
            case 'football':
                hint = 'брось футбольный мячик ( нажми, чтобы скопировать - <code>⚽️</code> )'
            case 'bouling':
                hint = 'отправь стикер боулинга ( нажми, чтобы скопировать - <code>🎳</code> )'
            case 'slot_machine':
                hint = 'отправь стикер игрового автомата ( нажми, чтобы скопировать - <code>🎰</code> )'
        await bot.send_message(
            chat_id=callback.from_user.id,
            text='🎮 Игра началась!\n\n'
            f'💁 <i>Подсказка: {hint}</i>'
        )
        await state.set_state(GameState.waiting_move)
    else:
        match callback.data:
            case 'numbers':
                await bot.send_message(
                    chat_id=callback.from_user.id,
                    text='🎮 Игра началась!\n\n'
                    '💁 <i>Подсказка: загадано число от 1 до 100, тебе необходимо угадать, либо оно больше/равно 50, либо меньше 50.</i>',
                    reply_markup=simple_keyboard_builder(
                        [
                            [
                                ['<', 'game_numbers_less'], ['50', '_'], ['⩽', 'game_numbers_more']
                            ]
                        ],
                        Mode.INLINE
                    )
                )
                await state.set_state(GameState.waiting_move)
            case 'heads_and_tails':
                await bot.send_message(
                    chat_id=callback.from_user.id,
                    text='🎮 Игра началась!\n\n'
                    '💁 <i>Подсказка: угадай, что выпало, орёл или решка.</i>',
                    reply_markup=simple_keyboard_builder(
                        [
                            [
                                ['Орёл', 'game_heads_and_tails_head'], ['Решка', 'game_heads_and_tails_tail']
                            ]
                        ],
                        Mode.INLINE
                    )
                )
                await state.set_state(GameState.waiting_move)
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
                    f'<code>choose_game data invalid! {callback.data}</code>'
                )