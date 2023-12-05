from aiogram.fsm.state import StatesGroup, State

class Game(StatesGroup):
    waiting_move = State()