from aiogram import Dispatcher, F

from .choose_game import choose_game
from .game import game

from states.GameState import GameState

from loader import msg_games

async def init(dp: Dispatcher) -> None:
    dp.callback_query.register(choose_game, F.data.in_(list(msg_games)))
    dp.callback_query.register(game, GameState.waiting_move)