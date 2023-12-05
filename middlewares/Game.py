from typing import Any, Awaitable, Callable, Dict, Optional, Set
from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject, Update, Message, CallbackQuery
from time import time

from states.GameState import GameState

from loader import msg_games_emojies

class Game(BaseMiddleware):
    def setup(
        self: BaseMiddleware, router: Dispatcher, exclude: Optional[Set[str]] = None
    ) -> BaseMiddleware:
        """
        Register middleware for all events in the Router

        :param router:
        :param exclude:
        :return:
        """
        if exclude is None:
            exclude = set()
        exclude_events = {"update", *exclude}
        for event_name, observer in router.observers.items():
            if event_name in exclude_events:
                continue
            observer.outer_middleware(self)
        return self

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:
        state = data['state']
        if await state.get_state() == GameState.waiting_move:
            if isinstance(event, Message):
                if event.dice:
                    if not event.dice.emoji in msg_games_emojies:
                        await event.answer('Вы находитесь в игре! На данный момент вам не доступны эти функции.')
                        return
                else:
                    if event.text == '1111':
                        return await handler(event, data)
                    await event.answer('Вы находитесь в игре! На данный момент вам не доступны эти функции.')
                    return
            elif isinstance(event, CallbackQuery):
                if not event.data.startswith('game_'):
                    await event.answer('Вы находитесь в игре! На данный момент вам не доступны эти функции.')
                    return
        return await handler(event, data)