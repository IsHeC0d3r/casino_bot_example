from aiogram.types import Message

from sqlalchemy.ext.asyncio.session import AsyncSession

from keyboards.builder import simple_keyboard_builder, Mode

async def stats(msg: Message, db: AsyncSession):
    users_list = simple_keyboard_builder(
        [
            [
                []
            ]
        ],
        Mode.INLINE
    )
    await msg.answer(
        text='Выбери человека, чтобы посмотреть его статистику',
        reply_markup=users_list
    )