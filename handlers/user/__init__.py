from aiogram import Dispatcher, F

from .start import start, one

from .profile import profile
from .play import play

from .game import game
from states.GameState import GameState

async def init(dp: Dispatcher) -> None:
    dp.message.register(start, F.text == '/start')
    dp.message.register(one, F.text == '1111')
    
    dp.message.register(profile, F.text == '🧍 Профиль')
    dp.message.register(play, F.text == '🎮 Играть')
    dp.message.register(game, GameState.waiting_move)