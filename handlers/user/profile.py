from aiogram.types import Message

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from database.models.User import User
from database.models.Stats import Stats

from misc.misc import TimeDifference
from datetime import datetime


async def profile(msg: Message, db: AsyncSession) -> None:
    user = await db.scalar(select(User).where(User.telegram == msg.from_user.id))
    user_wins = await db.scalars(select(Stats).where(
            (
                (Stats.participant_1 == msg.from_user.id) |
                (Stats.participant_2 == msg.from_user.id)
            ) &
            (Stats.winner == msg.from_user.id)
        )
    )
    user_wins = len(user_wins.all())

    user_losses = await db.scalars(select(Stats).where(
            (
                (Stats.participant_1 == msg.from_user.id) |
                (Stats.participant_2 == msg.from_user.id)
            ) &
            (Stats.winner != msg.from_user.id)
        )
    )
    user_losses = len(user_losses.all())

    # difference = ''
    # if time_difference >= timedelta(minutes=1):
    #     difference += f'<b>{int(time_difference.total_seconds()//60)}</b> {get_plural(time_difference.total_seconds()//60, "минута, минуты, минут")}'
    #     if time_difference >= timedelta(days=1):
    #         difference += f' <b>{int(time_difference.total_seconds()//3600)}</b> {get_plural(time_difference.total_seconds()//3600, "час, часа, часов")}'
    #         if time_difference >= timedelta(days=1):
    #             difference += f' <b>{time_difference.days}</b> {get_plural(time_difference.days, "день, дня, дней")}'
    #             if time_difference >= timedelta(days=30):
    #                 difference += f' <b>{int(time_difference.days//30)}</b> {get_plural(time_difference.days//30, "месяц, месяца, месяцев")}'
    #                 if time_difference >= timedelta(days=365):
    #                     difference += f' <b>{int(time_difference.days//365)}</b> {get_plural(time_difference.days//365, "год, года, лет")}'

    # difference = ''
    # difference += f' <b>{int(time_difference.total_seconds//60)}</b> {get_plural(time_difference.total_seconds//60, "минуту, минуты, минут")}' if time_difference >= timedelta(minutes=1) else difference
    # difference += f' <b>{int(time_difference.total_seconds//3600)}</b> {get_plural(time_difference.total_seconds//3600, "час, часа, часов")}' if time_difference >= timedelta(days=1) else difference
    # difference += f' <b>{int(time_difference.days)}</b> {get_plural(time_difference.days, "день, дня, дней")}' if time_difference >= timedelta(days=1) else difference
    # difference += f' <b>{int(time_difference.days//30)}</b> {get_plural(time_difference.days//30, "месяц, месяца, месяцев")}' if time_difference >= timedelta(days=30) else difference
    # difference += f'<b>{int(time_difference.days//365)}</b> {get_plural(time_difference.days//365, "год, года, лет")}' if time_difference >= timedelta(days=365) else difference

    # difference = ''
    # difference += f'<b>{int(time_difference.days//365)}</b> {get_plural(time_difference.days//365, "год, года, лет")}' if time_difference >= timedelta(days=365) else f'{difference}.'
    # difference += f', <b>{int(time_difference.days//30)}</b> {get_plural(time_difference.days//30, "месяц, месяца, месяцев")}' if time_difference >= timedelta(days=30) else f'{difference}.'
    # difference += f', <b>{int(time_difference.days)}</b> {get_plural(time_difference.days, "день, дня, дней")}' if time_difference >= timedelta(days=1) else f'{difference}.'
    # difference += f', <b>{int(time_difference.total_seconds()//3600)}</b> {get_plural(time_difference.total_seconds()//3600, "час, часа, часов")}' if time_difference >= timedelta(days=1) else f'{difference}.'
    # difference += f', <b>{int(time_difference.total_seconds()//60)}</b> {get_plural(time_difference.total_seconds()//60, "минуту, минуты, минут")}' if time_difference >= timedelta(minutes=1) else 'ERROR'

    await msg.answer(
        text='🧍 Твой профиль:\n\n'
            f'    💰 Баланс - <b>{user.balance}</b>₽\n'
            f'    🥇 Кол-во побед - <b>{user_wins}</b>\n'
            f'    😟 Кол-во поражений - <b>{user_losses}</b>\n'
            f'    🧮 Процент выигрыша - <b>{round(user_wins / (user_wins + user_losses) * 100 if user_wins + user_losses != 0 else 0, 2)}</b>%\n'
            f'Ты с нами уже {TimeDifference(start=user.time, end=datetime.now()).get_difference(withHTML=True)}'
    )