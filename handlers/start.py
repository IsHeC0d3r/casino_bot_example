from aiogram import Bot

from aiogram.types import Message

from sqlalchemy import select
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio.session import AsyncSession
from database.models.User import User
from time import time

from keyboards.reply import kb_start
from keyboards.builder import Mode, simple_keyboard_builder

async def start(msg: Message, db: AsyncSession) -> None:
	user = await db.scalar(select(User).where(User.telegram == msg.from_user.id))
	if user:
		await msg.answer(
			text='🙋 <b>Рад видеть тебя снова!</b>\n\n'
			'👇 <i>Выбери нужную кнопку в меню ниже</i>',
			reply_markup=simple_keyboard_builder(
				[
					[
						['Click_me', 'callback_data_0']
						['Or me', 'callback_data_1']
					],
					[
						['No, click me!', 'callback_data_2']
					]
				],
				Mode.INLINE
			)
		)
	else:
		await msg.answer(
			text=f'🙋 <b>Добро пожаловать, {msg.from_user.first_name}!</b>\n\n'
			'👇 <i>Выбери нужную кнопку в меню ниже</i>',
			reply_markup=kb_start
		)
		await db.add(
			User(
				telegram = msg.from_user.id
			)
		)