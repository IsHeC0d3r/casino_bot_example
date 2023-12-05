from typing import Any, Awaitable, Callable, Dict, Optional, Set
from aiogram import BaseMiddleware, Dispatcher
from misc.DaemonThrottlingStorage import DaemonThrottlingStorage
from aiogram.types import TelegramObject, Update
from time import time

class Throttling(BaseMiddleware):
    def __init__(self, storage: DaemonThrottlingStorage):
        self.storage = storage

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
        user = f'user_{event.from_user.id}'
        check_user = self.storage.get(user)

        # print(f'USER: {check_user}')

        # if 0 <= check_user <= 1:
        #     if check_user == 1:
        #         return
        #     self.storage.set(user)
        #     if self.storage.get(user):
        #         return await event.answer('Мы обнаружили подозрительную активность! Пожалуйста, подождите некоторое время перед отправкой новых сообщений.')
        # else:
        #     self.storage.set(user)

        if check_user == 1:
            return
        self.storage.set(user)
        if self.storage.get(user):
            return await event.answer('Мы обнаружили подозрительную активность! Пожалуйста, подождите некоторое время перед отправкой новых сообщений.')

        return await handler(event, data)