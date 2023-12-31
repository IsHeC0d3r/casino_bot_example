from aiogram.types import Message

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from database.models.User import User

from keyboards.reply import kb_start
from keyboards.builder import Mode, simple_keyboard_builder

from aiogram.fsm.context import FSMContext
from states.GameState import GameState

async def start(msg: Message, db: AsyncSession) -> None:
	user = await db.scalar(select(User).where(User.telegram == msg.from_user.id))
	if user:
		await msg.answer(
			text='🙋 <b>Рад видеть тебя снова!</b>\n\n'
			'👇 <i>Выбери нужную кнопку в меню ниже</i>',
			reply_markup=kb_start
		)
	else:
		await msg.answer(
			text=f'🙋 <b>Добро пожаловать, {msg.from_user.first_name}!</b>\n\n'
			'👇 <i>Выбери нужную кнопку в меню ниже</i>',
			reply_markup=kb_start
		)
		db.add(
			User(
				telegram = msg.from_user.id
			)
		)

async def one(msg: Message, state: FSMContext):
    await state.set_state(Game.waiting_move)
    print('+')