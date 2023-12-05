from aiogram import Dispatcher, F
from aiogram.filters.command import Command
from filters.isAdmin import AdminFIlter

from .help import help
from stats import stats
# from set_admin import set_admin
# from give_money import give_money

async def init(dp: Dispatcher) -> None:
    dp.message.register(help, Command('ahelp'), AdminFIlter())
    dp.message.register(help, Command('astats'), AdminFIlter())