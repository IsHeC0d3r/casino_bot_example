from aiogram.types import Message

async def help(msg: Message):
    await msg.answer(
        text='<code>/ahelp</code> - <b>узнать команды</b>\n'
        '<code>/astats</code> - <b>статистика пользователей</b>\n'
        '<code>/aset (id)</code> - <b>установить нового администратора</b>\n'
        '<code>/agivemoney</code> (id) (money) - <b>выдать деньги пользователю</b>'
    )