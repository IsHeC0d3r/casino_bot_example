from aiogram.fsm.state import StatesGroup, State

class GameState(StatesGroup):
    waiting_move = State()