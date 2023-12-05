from aiogram import Dispatcher

from .Throttling import Throttling

from .DB import DB
from loader import daemon_storage

from .Game import Game

async def init(dp: Dispatcher) -> None:
	Throttling(storage=daemon_storage).setup(router=dp)
	DB().setup(router=dp)
	Game().setup(router=dp)